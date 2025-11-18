import pytest
import numpy as np
import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from ai.embeddings import get_embedding
from ai.scorer import compute_similarity, best_match
from ai.reasoning import explain_alignment
from db.db_utils import (
    insert_strategy,
    fetch_strategies,
    insert_content,
    insert_chunk,
    fetch_content
)
from utils.chunker import agentic_chunk


@pytest.mark.integration
class TestFullWorkflow:
    """Test complete workflow from end to end."""

    def test_complete_text_analysis_workflow(
        self,
        patch_db_path,
        mock_openai_embedding,
        mock_openai_chat,
        mock_embedding
    ):
        """Test complete workflow: create strategy, analyze text, store results."""
        # Step 1: Create a strategy
        insert_strategy("Innovation", "AI and automation", mock_embedding)

        # Step 2: Get embedding for text
        text = "We are building AI-powered products"
        text_embedding = get_embedding(text)

        # Step 3: Fetch strategies and compute similarity
        strategies = fetch_strategies()
        assert len(strategies) == 1

        strategies_dicts = [
            {"id": s[0], "name": s[1], "description": s[2], "embedding": s[3]}
            for s in strategies
        ]
        similarities = compute_similarity(text_embedding, strategies_dicts)

        # Step 4: Get best match
        strategy_name, score = best_match(similarities)
        assert strategy_name == "Innovation"
        assert 0 <= score <= 1

        # Step 5: Generate explanation
        explanation = explain_alignment(text, strategy_name, score)
        assert isinstance(explanation, str)
        assert len(explanation) > 0

        # Step 6: Store results
        content_id = insert_content(text, strategy_name, score)
        insert_chunk(content_id, text, strategy_name, score, explanation, text_embedding)

        # Step 7: Verify storage
        df = fetch_content()
        assert len(df) == 1
        assert df.iloc[0]['best_match'] == "Innovation"

    def test_document_chunking_and_analysis(
        self,
        patch_db_path,
        mock_openai_embedding,
        mock_openai_chat,
        mock_embedding
    ):
        """Test document chunking and analysis workflow."""
        # Create strategies
        insert_strategy("Innovation", "AI and automation", mock_embedding)
        insert_strategy("Sustainability", "Environmental focus", mock_embedding * 0.9)

        # Create a multi-paragraph document
        document = """AI Innovation Project.

        We are developing new AI-powered products to automate business processes.

        Our sustainability goals include reducing carbon emissions."""

        # Chunk the document
        chunks = agentic_chunk(document)
        assert len(chunks) >= 2

        # Analyze each chunk
        strategies = fetch_strategies()
        strategies_dicts = [
            {"id": s[0], "name": s[1], "description": s[2], "embedding": s[3]}
            for s in strategies
        ]

        content_id = insert_content("Test Document", None, None)

        for chunk in chunks:
            chunk_embedding = get_embedding(chunk)
            similarities = compute_similarity(chunk_embedding, strategies_dicts)
            strategy_name, score = best_match(similarities)
            explanation = explain_alignment(chunk, strategy_name, score)

            insert_chunk(content_id, chunk, strategy_name, score, explanation, chunk_embedding)

        # Verify all chunks were analyzed
        df = fetch_content()
        assert len(df) == 1

    def test_multiple_strategies_comparison(
        self,
        patch_db_path,
        mock_openai_embedding,
        mock_embedding
    ):
        """Test comparing text against multiple strategies."""
        # Create multiple strategies
        strategies_data = [
            ("Innovation", "AI and automation", mock_embedding),
            ("Sustainability", "Environmental focus", mock_embedding * 0.8),
            ("Excellence", "Quality and efficiency", mock_embedding * 0.6),
        ]

        for name, desc, emb in strategies_data:
            insert_strategy(name, desc, emb)

        # Get strategies and analyze text
        text = "AI-powered automation"
        text_embedding = get_embedding(text)

        strategies = fetch_strategies()
        assert len(strategies) == 3

        strategies_dicts = [
            {"id": s[0], "name": s[1], "description": s[2], "embedding": s[3]}
            for s in strategies
        ]

        similarities = compute_similarity(text_embedding, strategies_dicts)

        # Should have similarity scores for all strategies
        assert len(similarities) == 3

        # Scores should be in descending order
        scores = [s["score"] for s in similarities]
        assert scores == sorted(scores, reverse=True)

    def test_empty_database_handling(self, patch_db_path, mock_openai_embedding, mock_embedding):
        """Test handling of empty database."""
        strategies = fetch_strategies()
        assert len(strategies) == 0

        df = fetch_content()
        assert df is None or len(df) == 0


@pytest.mark.integration
class TestDataPersistence:
    """Test data persistence across operations."""

    def test_strategy_persistence(self, patch_db_path, mock_embedding):
        """Test that strategies persist correctly."""
        # Insert multiple strategies
        insert_strategy("Strategy 1", "Description 1", mock_embedding)
        insert_strategy("Strategy 2", "Description 2", mock_embedding * 0.9)

        # Fetch and verify
        strategies = fetch_strategies()
        assert len(strategies) == 2

        # Fetch again to ensure persistence
        strategies2 = fetch_strategies()
        assert len(strategies2) == 2
        assert strategies[0][1] == strategies2[0][1]

    def test_content_persistence(self, patch_db_path):
        """Test that content persists correctly."""
        # Insert content
        id1 = insert_content("Text 1", "Innovation", 0.9)
        id2 = insert_content("Text 2", "Sustainability", 0.8)

        # Fetch and verify
        df = fetch_content()
        assert len(df) == 2

        # Verify order (should be DESC by created_at)
        assert df.iloc[0]['text'] == "Text 2"  # Most recent first

    def test_chunk_relationships(self, patch_db_path, mock_embedding):
        """Test that chunk-content relationships are maintained."""
        # Insert content and chunks
        content_id = insert_content("Parent document", "Innovation", 0.9)

        insert_chunk(content_id, "Chunk 1", "Innovation", 0.9, "Explanation 1", mock_embedding)
        insert_chunk(content_id, "Chunk 2", "Sustainability", 0.8, "Explanation 2", mock_embedding * 0.9)

        # Verify chunks are linked to content
        from db.db_utils import connect
        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM chunks WHERE content_id=?", (content_id,))
        count = cur.fetchone()[0]
        conn.close()

        assert count == 2


@pytest.mark.integration
@pytest.mark.slow
class TestPerformance:
    """Test performance-related aspects."""

    def test_bulk_embedding_caching(self, mock_openai_embedding, mock_embedding):
        """Test that embedding caching works for multiple calls."""
        with patch('ai.embeddings.load_cache') as load_mock, \
             patch('ai.embeddings.save_cache') as save_mock:

            cache = {}
            load_mock.return_value = cache

            # First call should save to cache
            text = "Test text"
            get_embedding(text)
            assert save_mock.called

            # Simulate cache being populated
            import hashlib
            key = hashlib.sha256(text.encode()).hexdigest()
            cache[key] = mock_embedding
            load_mock.return_value = cache

            # Second call should use cache (no new API call)
            result = get_embedding(text)
            assert np.allclose(result, mock_embedding)

    def test_large_document_chunking(self):
        """Test chunking of large documents."""
        # Create a large document
        large_doc = "\n\n".join([f"Paragraph {i}" for i in range(100)])
        chunks = agentic_chunk(large_doc)

        # Should create multiple chunks
        assert len(chunks) > 1
        assert len(chunks) <= 100

    def test_many_strategies_similarity(self, mock_embedding):
        """Test similarity computation with many strategies."""
        # Create many strategies
        strategies = [
            {
                "id": i,
                "name": f"Strategy {i}",
                "description": f"Description {i}",
                "embedding": mock_embedding * (1 - i * 0.01)
            }
            for i in range(20)
        ]

        # Compute similarity
        similarities = compute_similarity(mock_embedding, strategies)

        assert len(similarities) == 20
        assert all(0 <= s["score"] <= 1 for s in similarities)
