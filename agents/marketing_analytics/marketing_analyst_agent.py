
import os
import hashlib

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
        logger.info("Read and formatted prompt")


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
        vector_store.add_documents(documents=chunks, ids=ids)

        logger.info(
            "Added %s chunks from %s to the knowledge base",
            len(chunks),
            data_source_path,
        )

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
    marketing_analytics_agent.build_knowledge_base()
    
