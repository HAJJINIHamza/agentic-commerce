"""Build a local SQLite full-text index from PDF documents."""

from pathlib import Path
import sqlite3
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

from src.logger import get_logger

logger = get_logger(__name__)

DEFAULT_DATABASE_PATH = Path("term_knowledge_base.sqlite3")
CHUNK_SIZE = 2000
CHUNK_OVERLAP = 150


def build_term_knowledge_base(
    pdf_path: str | Path,
    database_path: str | Path = DEFAULT_DATABASE_PATH,
    *,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> int:
    """Extract a PDF, split each page into chunks, and index them in SQLite FTS5.

    Each indexed chunk retains the PDF filename, full path, and 1-based page
    number. Rebuilding the same PDF replaces its existing chunks. Returns the
    number of chunks added.
    """
    pdf_path = Path(pdf_path).expanduser().resolve()
    database_path = Path(database_path).expanduser()
    if not pdf_path.is_file():
        raise FileNotFoundError(f"PDF does not exist: {pdf_path}")
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")
    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be >= 0 and smaller than chunk_size")

    database_path.parent.mkdir(parents=True, exist_ok=True)
    reader = PdfReader(str(pdf_path))
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    rows = []
    logger.info("Chunking and indexing PDF")
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        rows.extend(
            (pdf_path.name, str(pdf_path), page_number, chunk)
            for chunk in splitter.split_text(text)
            if chunk.strip()
        )

    _add_rows_to_sql_database(pdf_path, database_path, rows)
    logger.info("Finished indexing %d chunks from %s into %s", len(rows), pdf_path, database_path)

    return len(rows)

def _add_rows_to_sql_database(
        pdf_path: str | Path, 
        database_path: str | Path, 
        rows: list[tuple[str, str, int, str]]
        ) -> None:
    with sqlite3.connect(database_path) as connection:
        connection.execute(
            """CREATE VIRTUAL TABLE IF NOT EXISTS pdf_chunks USING fts5(
                pdf_name UNINDEXED,
                pdf_path UNINDEXED,
                page_number UNINDEXED,
                content
            )"""
        )
        # Keep indexing idempotent when the same PDF is processed again.
        connection.execute("DELETE FROM pdf_chunks WHERE pdf_path = ?", (str(pdf_path),))
        logger.info("Adding %d chunks to SQLite database at %s", len(rows), database_path)
        connection.executemany(
            "INSERT INTO pdf_chunks (pdf_name, pdf_path, page_number, content) VALUES (?, ?, ?, ?)",
            rows,
        )

class TermKnowledgeBaseBuilder:
    """Convenience wrapper for callers that prefer the builder class API."""

    def build_term_knowledge_base(self, pdf_path: str | Path, **kwargs) -> int:
        return build_term_knowledge_base(pdf_path, **kwargs)


# Preserve the original class name while existing imports migrate.
termKnowledgeBaseBuilder = TermKnowledgeBaseBuilder

if __name__ == "__main__":
    # Example usage:
    pdf_path = Path("ressources/rag_documents/principles_of_marketing_book.pdf")
    database_path = Path("term_knowledge_base.sqlite3")
    num_chunks = build_term_knowledge_base(pdf_path, database_path)
    print(f"Finished indexing {num_chunks} chunks from {pdf_path} into {database_path}")
