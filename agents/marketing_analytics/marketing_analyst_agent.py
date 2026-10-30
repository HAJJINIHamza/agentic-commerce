
import os
import hashlib
from pyexpat.errors import messages

from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter, TokenTextSplitter
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import json
from pypdf import PdfReader

from agents.embeddings.openrouter_embeddings import OpenRouterEmbeddings
from agents.marketing_analytics.marketing_agent import marketingAgent
from agents.listing_generation.listing_generator import listingGenerationAgent
from src.logger import get_logger

logger = get_logger(__name__)

load_dotenv()

# 1. Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Multi stage RAG

class marketingAnalyticsAgent:
    def __init__(self):
        pass

    ##############################################################################################
    # STAGE 1: Give marketing data to LLM, 
    # Let it analyze it and provide a report and queries 
    ##############################################################################################

    def get_observations_and_queries(self, marketing_data_path):
        """
        This LLM anayzes marketing data from marketing_data_path and generated a reports with oservations and queries.
        Queries are questions to look for in the Marketing Knowledge base

        input :
        marketing_data_path : str : path to the marketing data file (csv)
                                example : 'data/marketing/shopee_ads/overall_data/Shopee-Ads-Overall-Data-01_09_2026-21_09_2026.csv'
        
        output :
        marketing_report : dict : {"relevant_observations" : List[str],"relevant_queries": List[str] }
        
        """

        # Prompt
        with open("agents/prompts/marketing_analyst_stage_1_prompt.txt", "r") as f:
            marketing_analytics_prompt = f.read()

        # Data
        #data_file = "data/marketing/shopee_ads/overall_data/Shopee-Ads-Overall-Data-01_09_2026-21_09_2026.csv"
        marketing_data = marketingAgent().read_shopee_ads_data(marketing_data_path)
        marketing_data_json = marketing_data.to_json(orient="records", indent=2)

        # Put data into prompt
        marketing_analytics_prompt = marketing_analytics_prompt.format(
            marketing_data=marketing_data_json,
        )
        logger.info(f"Marketing analytics prompt stage 1 : {marketing_analytics_prompt}")


        # Invoke LLM, output should be : {{"relevant_observations" : List[str],"relevant_queries": List[str] }}
        marketing_report = listingGenerationAgent().get_completion_from_model(
                            prompt=marketing_analytics_prompt)[0]

        #Make sure the output is a valid JSON
        try:
            marketing_report = json.loads(marketing_report)

        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
            logger.error(f"Marketing report: {marketing_report}")
            raise ValueError(f"Error decoding JSON: {e}. Marketing report: {marketing_report}")

        logger.info("Got marketing report from LLM")
        logger.info(f"Relevant observations : {marketing_report['relevant_observations']}")
        logger.info(f"Number of queries : {len(marketing_report['relevant_queries'])}")
        logger.info(f"Relevant queries : {marketing_report['relevant_queries']}")

        return marketing_report
        
    ##############################################################################################
    # STAGE 2: Give queries and knowledge base to LLM, 
    # let it search and provide actions to improve listings and marketing performance 
    ##############################################################################################

    def retrieve_relevant_docs(self, queries: str | list[str], relevant_observations: list[str]):
        """
        Retrieve relevant documents using the queries combined with the marketing observations.
        
        Input :
            queries : str | list[str] : one query or multiple queries to search for
            relevant_observations : list[str] : marketing observations that will be added to each query
        
        Output :
            retrieved_docs : List[Document] : the relevant documents retrieved from the knowledge base
                                                
        Example output :[
                            [Document(id='', 
                                    metadata={'page': , 'source': ''}, 
                                    page_content=''), 
                            Document(id='', 
                                        metadata={'page': , 'source': ''}, 
                                        page_content='')
                                        ], 
                            [Document(id='', 
                                        metadata={'page': , 'source': ''}, 
                                        page_content=''), 
                            Document(id='', 
                                        metadata={'page': , 'source': ''}, 
                                        page_content='')]
                        ]
        """
        vector_store = Chroma(
            collection_name="principles_of_marketing_docs",
            embedding_function=OpenRouterEmbeddings(),
            persist_directory="./chroma_db",
        )

        retriever = vector_store.as_retriever (
            search_type="similarity", #mmr : Balance similarity with diversity. "similarity_score_threshold": considers the embeddings only if they verify a certain similarity score threshold.
            search_kwargs={"k": 3},
        )

        if isinstance(queries, str):
            queries = [queries]
        elif not isinstance(queries, list) or not all(
            isinstance(query, str) for query in queries
        ):
            raise TypeError("queries must be a string or a list of strings")

        # Join observations with queires
        relevant_observations = " ".join(relevant_observations)
        queries = [relevant_observations + ". " + query for query in queries] 

        logger.info(f"Queries to give to retriever are : {queries}")

        retrieved_docs = retriever.batch(queries)

        total_docs = sum(len(docs) for docs in retrieved_docs)
        logger.info(
            "Retrieved %s documents across %s queries",
            total_docs,
            len(retrieved_docs),
        )

        return retrieved_docs

    def answer_query_with_context(self, query : str,
                                  relevant_observations : list[str], 
                                  retrieved_docs : list[Document]):

        """
        Give model query, relevant observations and retrieved documents,
        let it provide actions to improve marketing performance.

        Input :
        - query : str : the query to answer
        - relevant_observations : List[str] : the relevant observations from the marketing data
        - retrieved_docs : List[Document] : the relevant documents retrieved from the knowledge base

        Output :
        - solutions : { "relevant_decisions": List[str] }
        """

        with open("agents/prompts/marketing_analyst_stage_2_prompt.txt", "r") as f:
            marketing_analytics_prompt = f.read()

        context = "\n\n".join(
            doc.page_content for doc in retrieved_docs
        )

        marketing_analytics_prompt = marketing_analytics_prompt.format(query=query,
                                                                    relevant_observations=relevant_observations,
                                                                    principales_of_marketing=context
        )

        logger.info(f"Marketing analytics prompt stage 2 : {marketing_analytics_prompt}")

        solutions, _ = listingGenerationAgent().get_completion_from_model(marketing_analytics_prompt)

        logger.info("Got solutions from model.")

        return solutions

    def analyse_marketing_performance_pipeline(self, marketing_data_path: str):
        """
        Analyze marketing data, retrieve supporting documents, and return solutions.

        Input : 
        marketing_data_path : str : path to the marketing data file (csv)
                                example : 'data/marketing/shopee_ads/overall_data/Shopee-Ads-Overall-Data-01_09_2026-21_09_2026.csv'
        
        Solutions : list[{"relevant_decisions": List[str] }] : 
        """
        print ("#################################### STAGE 1 : report and queries ################################################")
        marketing_report = self.get_observations_and_queries(marketing_data_path)
        relevant_observations = marketing_report["relevant_observations"]
        relevant_queries = marketing_report["relevant_queries"]

        if not relevant_queries:
            raise ValueError("The marketing report did not contain any relevant queries")

        print ("#################################### Retrieval ################################################")
        retrieved_docs_by_query = self.retrieve_relevant_docs(
            relevant_queries,
            relevant_observations,
        )

        print ("#################################### STAGE 2 : Solutions to improve marketing ################################################")
        solutions = []
        for i in (len(relevant_queries)):
            solution = self.answer_query_with_context(
                query=relevant_queries[i],
                relevant_observations=relevant_observations,
                retrieved_docs=retrieved_docs_by_query[i],
            )
            solutions.append(solution)

        return solutions

####################################################################################
#Knowledge base builder
####################################################################################

class knowledgeBaseBuilder:
    def __init__(self):
        pass

    def build_knowledge_base(self):
        """Create an empty, persisted Chroma collection for marketing documents."""
        persist_directory = "./chroma_db"
        collection_name = "principles_of_marketing_docs"

        vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=OpenRouterEmbeddings(),
            persist_directory=persist_directory,
        )
        vector_store.reset_collection()

        logger.info(
            "Created empty vector store collection '%s' at %s",
            collection_name,
            persist_directory,
        )

    def add_doc_to_knowledge_base(self, data_source_path: str):
        """Split a PDF into chunks and add them to the persisted Chroma collection."""
        reader = PdfReader(data_source_path)
        documents = [
            Document(
                page_content=page.extract_text() or "",
                metadata={"source": data_source_path, "page": page_number},
            )
            for page_number, page in enumerate(reader.pages, start=1)
        ]
        logger.info("Loaded %s pages from %s", len(documents), data_source_path)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
        )
        chunks = splitter.split_documents(documents)
        logger.info("Split PDF into %s chunks", len(chunks))
        if not chunks:
            logger.warning("No text chunks found in %s; nothing was added", data_source_path)
            return

        embeddings = OpenRouterEmbeddings()
        logger.info("Calling vectore database for chunks")
        vector_store = Chroma(
            collection_name="principles_of_marketing_docs",
            embedding_function=embeddings,
            persist_directory="./chroma_db",
        )

        ids = [
            hashlib.sha256(
                f"{data_source_path}\0{chunk.metadata['page']}\0{index}\0{chunk.page_content}".encode("utf-8")
            ).hexdigest()
            for index, chunk in enumerate(chunks)
        ]
        # Chroma passes all chunk texts to embed_documents(); _embed() handles
        # splitting that list into API-sized batches internally.
        logger.info("Adding %s chunks to the knowledge base", len(chunks))
        vector_store.add_documents(documents=chunks, ids=ids)

        logger.info(
            "Added %s chunks from %s to the knowledge base",
            len(chunks),
            data_source_path,
        )

    def get_vector_store_information(self):
        """Get information about the persisted Chroma collection."""
        vector_store = Chroma(
            collection_name="principles_of_marketing_docs",
            embedding_function=OpenRouterEmbeddings(),
            persist_directory="./chroma_db",
        )
        count = vector_store._collection.count()
        sample = vector_store.get(limit=1, include=["embeddings"])["embeddings"]
        if count and len(sample):
            vector = sample[0]
            dimensions = len(vector)
            raw_vectors_bytes = count * dimensions * vector.dtype.itemsize 
            logger.info("Vectors: %s", count)
            logger.info("Dimensions per vector: %s", dimensions)
            logger.info("Approx. raw vector memory: %.2f MB", raw_vectors_bytes / 1024**2)
            print ("Sample vector :")
            print (vector_store.get(limit=1, include=["documents", "embeddings", "metadatas"]))
        else:
            logger.warning("The collection has no vectors.")

"""
# 5. Configure retriever
#retriever = vector_store.as_retriever(
#    search_type="similarity", #mmr : Balance similarity with diversity. "similarity_score_threshold": considers the embeddings only if they verify a certain similarity score threshold.
#    search_kwargs={"k": 3},
#)

# 6. Configure LLM and prompt
with open("agents/prompts/marketing_analyst_prompt.txt", "r") as f:
    marketing_analytics_prompt = f.read()

marketing_analytics_prompt = ChatPromptTemplate.from_template(marketing_analytics_prompt)

# 7. RAG pipeline
def answer_question(question: str) -> str:
    retrieved_docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content for doc in retrieved_docs
    )

    messages = marketing_analytics_prompt.invoke({
        "context": context,
        "question": question,
    })

    response = llm.invoke(messages)
    return response.content
"""

# 8. Run
if __name__ == "__main__":
    marketing_analytics_agent = marketingAnalyticsAgent()
    #vector_store_builder = knowledgeBaseBuilder()
    #marketing_analytics_agent.build_knowledge_base()

    #data_source_path_1 = "ressources/rag_documents/principles_of_marketing_book_part_1.pdf"
    #data_source_path_2 = "ressources/rag_documents/principles_of_marketing_book_part_2.pdf"
    #data_source_path_3 = "ressources/rag_documents/principles_of_marketing_book_part_3.pdf"
    #vector_store_builder.add_doc_to_knowledge_base(data_source_path_3)
    
    #vector_store_builder.get_vector_store_information()
    """
    print ("########################### Get observations and queries ##################################")
    data_path = "data/marketing/shopee_ads/overall_data/Shopee-Ads-Overall-Data-01_09_2026-21_09_2026.csv"
    relevant_observations, relevant_queries = marketing_analytics_agent.get_observations_and_queries(marketing_data_path = data_path)
    print ("Relevant observations : ")
    print (relevant_observations)
    
    print ("########################### Retrieving docs from knowledge base ##################################")
    
    #query = "What are the best practices for optimizing Shopee Ads campaigns?"
    query_1 = "look for ways to increase the click-through rate of the product"
    relevant_observations = ["The click-through rate (CTR) is 0.32%, which is below the industry average of 2.5%."]

    retrieved_docs = marketing_analytics_agent.retrieve_relevant_docs(query_1, relevant_observations)
    print ("Retrieved documents:")
    print (retrieved_docs)
    #for i in range(len(retrieved_docs)):
    #    print (retrieved_docs[i].page_content)
    #    print ("----------------------------------------")
    
    print ("########################### Marketing solutions from model ##################################")
    retrieved_docs = retrieved_docs[0]
    relevant_decisions = marketing_analytics_agent.answer_query_with_context(query=query_1,
                                                                            relevant_observations = relevant_observations,
                                                                            retrieved_docs = retrieved_docs)
    print ("Relevant decisions :")
    print (relevant_decisions)
    """
    data_path = "data/marketing/shopee_ads/overall_data/Shopee-Ads-Overall-Data-01_09_2026-21_09_2026.csv"
    relevant_decisions = marketing_analytics_agent.analyse_marketing_performance_pipeline(marketing_data_path = data_path)
    print ("Relevant decisions :")
    print (relevant_decisions)

    
