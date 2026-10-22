import os
import pytest
from agents.embeddings.openrouter_embeddings import OpenRouterEmbeddings


TEXT_1 = (
    "I want you to analyze marketing data and provide insights and queries "
    "to improve marketing performance."
)
TEXT_2 = (
    "I am unable to analyze my marketing data that is why I am building a "
    "rag agent that will do that for me."
)
TEXT_3 = (
    "The lion is named the king of the jungle because of its strength and "
    "dominance in the animal kingdom."
)


@pytest.mark.skipif(
    not os.getenv("OPENROUTER_API_KEY"),
    reason="OPENROUTER_API_KEY is required for this live API integration test",
)
def test_openrouter_embeddings_rank_related_text_higher():
    embedder = OpenRouterEmbeddings()
    embeddings = embedder.embed_documents([TEXT_1, TEXT_2, TEXT_3])

    similarity_1 = embedder.embedding_similarity(embeddings[0], embeddings[1])
    similarity_2 = embedder.embedding_similarity(embeddings[0], embeddings[2])

    print("Embeddings length:", len(embeddings))
    print(f"Similarity between text_1 and text_2: {similarity_1}")
    print(f"Similarity between text_1 and text_3: {similarity_2}")

    assert len(embeddings) == 3
    assert similarity_1 > similarity_2, (
        "The marketing-related text should be more similar than the unrelated "
        "lion text."
    )
    print ("Test passed")

if __name__ == "__main__":
    test_openrouter_embeddings_rank_related_text_higher()

