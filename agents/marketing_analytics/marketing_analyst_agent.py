
import os

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

# 1. Configuration
os.environ["OPENAI_API_KEY"] = "your-api-key"

# 2. Load documents (replace with your document loader)
documents = [
    Document(
        page_content="RAG combines information retrieval with language generation.",
        metadata={"source": "rag_intro.txt"},
    ),
]

# 3. Split documents into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)
chunks = splitter.split_documents(documents)

# 4. Create vector store
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="rag_collection",
    persist_directory="./chroma_db",
)

# 5. Configure retriever
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3},
)

# 6. Configure LLM and prompt
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

prompt = ChatPromptTemplate.from_template("""
Answer the question using ONLY the context below.
If the answer is not in the context, say you don't know.

Context:
{context}

Question:
{question}
""")

# 7. RAG pipeline
def answer_question(question: str) -> str:
    retrieved_docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content for doc in retrieved_docs
    )

    messages = prompt.invoke({
        "context": context,
        "question": question,
    })

    response = llm.invoke(messages)
    return response.content


# 8. Run
if __name__ == "__main__":
    question = "What is RAG?"
    print(answer_question(question))