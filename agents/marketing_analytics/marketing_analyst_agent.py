
import os
import hashlib
from pyexpat.errors import messages
import sqlite3

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
from src.utils import split_query_into_terms

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
        marketing_report : dict : {"relevant_observations" : List[str],"relevant_query": str }
        
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


        # Invoke LLM, output should be : {{"relevant_observations" : List[str],"relevant_query": str }}
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
        logger.info(f"Relevant query : {marketing_report['relevant_query']}")

        return marketing_report
        
    ##############################################################################################
    # STAGE 2: Give queries and knowledge base to LLM, 
    # let it search and provide actions to improve listings and marketing performance 
    ##############################################################################################

    def embeddings_based_retriever(self, queries: str | list[str], relevant_observations: list[str]):
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

        logger.info(f"Queries to give to retriever are : {queries}")

        retrieved_docs = retriever.batch(queries)

        total_docs = sum(len(docs) for docs in retrieved_docs)
        logger.info(
            "Retrieved %s documents across %s queries",
            total_docs,
            len(retrieved_docs),
        )

        return retrieved_docs

    def term_based_retrieve_one_query(self, query: str):
        """
        Retrieve relevant documents using the query and the term-based knowledge base.
        
        Input :
            query : str : the query to search for
        
        Output :
            docs : list[dict] : example : [{"metadata": "pdf_name, page 2 (score: 0.123)", "content": "text of the chunk"}, ...]
        """

        fts_query = split_query_into_terms(query)
        logger.info("Retrieving documents for query: %s", fts_query)

        with sqlite3.connect("term_knowledge_base.sqlite3") as conn:
            rows = conn.execute(
                """
                SELECT pdf_name, page_number, content, bm25(pdf_chunks) AS score
                FROM pdf_chunks
                WHERE content MATCH ?
                ORDER BY score
                LIMIT 3
                """,
                (fts_query,),
            ).fetchall()
        docs = []
        for pdf_name, page_number, content, score in rows:
            doc = {
                "metadata": f"{pdf_name}, page {page_number} (score: {score:.3f})",
                "content" : content
                }
            docs.append(doc)
        return docs

    def term_based_retriever(self, queries: str | list[str]):
        """
        Retrieve relevant documents using the queries and the term-based knowledge base.
        
        Input :
            queries : str | list[str] : one query or multiple queries to search for
        
        Output :
            list_of_docs : list[list[dict]] : one list of matching documents per query
        """
        if isinstance(queries, str):
            queries = [queries]
        elif not isinstance(queries, list) or not all(
            isinstance(query, str) for query in queries
        ):
            raise TypeError("queries must be a string or a list of strings")

        list_of_docs = []
        for query in queries:
            docs = self.term_based_retrieve_one_query(query)
            list_of_docs.append(docs)

        return list_of_docs

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

        context = "\nNew document :\n".join(
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

    def analyse_marketing_performance_pipeline(
        self,
        marketing_data_path: str,
        retriever: str = "embedding",
    ):
        """
        Analyze marketing data, retrieve supporting documents, and return solutions.

        Input : 
        marketing_data_path : str : path to the marketing data file (csv)
                                example : 'data/marketing/shopee_ads/overall_data/Shopee-Ads-Overall-Data-01_09_2026-21_09_2026.csv'
        retriever : str : retrieval method, either "embedding" or "term"
        
        Solutions : list[{"relevant_decisions": List[str] }] : 
        """
        if retriever not in {"embedding", "term"}:
            raise ValueError('retriever must be either "embedding" or "term"')

        print ("#################################### STAGE 1 : report and queries ################################################")
        marketing_report = self.get_observations_and_queries(marketing_data_path)
        relevant_observations = marketing_report["relevant_observations"]
        relevant_query = marketing_report["relevant_query"]

        if not relevant_query:
            raise ValueError("The marketing report did not contain any relevant queries")

        print ("#################################### Retrieval ################################################")
        if retriever == "embedding":
            retrieved_docs = self.embeddings_based_retriever(
                relevant_query,
                relevant_observations,
            )
        else:
            retrieved_docs = self.term_based_retrieve_one_query(relevant_query) #list[dict]

        print ("#################################### STAGE 2 : Solutions to improve marketing ################################################")

        solution = self.answer_query_with_context( # { "relevant_decisions": List[str] }
            query=relevant_query,
            relevant_observations=relevant_observations, 
            retrieved_docs=retrieved_docs,
        )

        return solution



# 8. Run
if __name__ == "__main__":
    marketing_analytics_agent = marketingAnalyticsAgent()

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

    #Test term-based retriever
    #queries = ["How to imporve click through rate", "Why is conversion rate so low"]
    #query = "Click Through Rate"
    #retrieved_docs = marketing_analytics_agent.term_based_retriever(queries)
    #print ("Retrieved documents:")
    #print (retrieved_docs)
    
