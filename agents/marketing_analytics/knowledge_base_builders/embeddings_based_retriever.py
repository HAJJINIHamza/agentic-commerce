from langchain.chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.documents import Document
import hashlib
from pypdf import PdfReader


from agents.embeddings.openrouter_embeddings import OpenRouterEmbeddings
from src.logger import logger

logger = logger.get_logger(__name__)

####################################################################################
#Knowledge base builder
####################################################################################

class embeddingsknowledgeBaseBuilder:
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

#test
# 
#if __name__ == "__main__":
    #vector_store_builder = knowledgeBaseBuilder()
    #marketing_analytics_agent.build_knowledge_base()

    #data_source_path_1 = "ressources/rag_documents/principles_of_marketing_book_part_1.pdf"
    #data_source_path_2 = "ressources/rag_documents/principles_of_marketing_book_part_2.pdf"
    #data_source_path_3 = "ressources/rag_documents/principles_of_marketing_book_part_3.pdf"
    #vector_store_builder.add_doc_to_knowledge_base(data_source_path_3)
    
    #vector_store_builder.get_vector_store_information()