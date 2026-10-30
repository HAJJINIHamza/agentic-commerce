import os
import math
import random
import requests
import time
from dotenv import load_dotenv
from langchain_core.embeddings import Embeddings

from src.logger import get_logger

logger = get_logger(__name__)
load_dotenv()

class OpenRouterEmbeddings(Embeddings):
    batch_size = 64
    max_retries = 5
    initial_retry_delay = 2.0
    max_retry_delay = 30.0

    def __init__(self,
                 embedder="nvidia/nemotron-3-embed-1b:free"):

        self.embedder = embedder
        self.api_key = os.environ["OPENROUTER_API_KEY"]
        self.url = "https://openrouter.ai/api/v1/embeddings"

    def _embed(self, texts: list[str]) ->  list[list[float]]:
        embeddings = []
        for start in range(0, len(texts), self.batch_size):
            batch = texts[start : start + self.batch_size]
            embeddings.extend(self._embed_batch_with_retries(batch, start))
            logger.info(
                "Embedded batch %s to %s of %s texts",
                start,
                start + len(batch),
                len(texts),
            )

        return embeddings

    def _embed_batch_with_retries(
        self,
        batch: list[str],
        batch_start: int,
    ) -> list[list[float]]:
        for attempt in range(self.max_retries + 1):
            try:
                response = requests.post(
                    self.url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.embedder,
                        "input": batch,
                        "encoding_format": "float",
                    },
                    timeout=60,
                )
                response.raise_for_status()
                data = response.json()["data"]
                data.sort(key=lambda item: item["index"])
                return [item["embedding"] for item in data]
            except requests.HTTPError as error:
                status_code = error.response.status_code if error.response else None
                retryable = status_code == 429 or (
                    status_code is not None and 500 <= status_code < 600
                )
                if not retryable or attempt == self.max_retries:
                    raise

                retry_after = error.response.headers.get("Retry-After")
                delay = self._get_retry_delay(attempt, retry_after)
                logger.warning(
                    "Embedding API returned HTTP %s for batch %s-%s. "
                    "Retrying in %.1f seconds (attempt %s/%s).",
                    status_code,
                    batch_start,
                    batch_start + len(batch),
                    delay,
                    attempt + 1,
                    self.max_retries,
                )
                time.sleep(delay)
            except requests.RequestException:
                if attempt == self.max_retries:
                    raise

                delay = self._get_retry_delay(attempt)
                logger.warning(
                    "Embedding request failed for batch %s-%s. "
                    "Retrying in %.1f seconds (attempt %s/%s).",
                    batch_start,
                    batch_start + len(batch),
                    delay,
                    attempt + 1,
                    self.max_retries,
                )
                time.sleep(delay)

    def _get_retry_delay(self, attempt: int, retry_after: str | None = None) -> float:
        if retry_after:
            try:
                delay = float(retry_after)
            except ValueError:
                delay = self.initial_retry_delay * (2**attempt)
        else:
            delay = self.initial_retry_delay * (2**attempt)

        delay = min(delay, self.max_retry_delay)
        return delay + random.uniform(0, min(1.0, delay * 0.1))

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self._embed(texts)

    def embed_query(self, text:str) -> list[float]:
        return self._embed([text])[0]

    def embedding_similarity(
        self,
        vector1: list[float],
        vector2: list[float],
    ) -> float:
        """Return the cosine similarity between two embedding vectors."""
        if len(vector1) != len(vector2):
            raise ValueError("Embedding vectors must have the same dimensions")

        dot_product = sum(a * b for a, b in zip(vector1, vector2))
        norm1 = math.sqrt(sum(value * value for value in vector1))
        norm2 = math.sqrt(sum(value * value for value in vector2))
        if norm1 == 0 or norm2 == 0:
            raise ValueError("Cosine similarity is undefined for a zero vector")

        cosine_similarity = dot_product / (norm1 * norm2)
        # Floating-point rounding can put cosine similarity just outside [-1, 1].
        cosine_similarity = max(-1.0, min(1.0, cosine_similarity))
        return cosine_similarity
