import pytest
import numpy as np
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from ai.embeddings import get_embedding
from ai.scorer import compute_similarity, best_match
from ai.reasoning import explain_alignment


@pytest.mark.unit
@pytest.mark.ai
class TestEmbeddings:
    """Test embedding generation."""

    def test_get_embedding_returns_vector(self, mock_openai_embedding, mock_embedding):
        """Test that get_embedding returns a numpy array."""
        result = get_embedding("Test text")
        assert isinstance(result, np.ndarray)
        assert result.shape[0] > 0
        assert result.dtype == np.float32

    def test_get_embedding_caching(self, mock_openai_embedding, mock_embedding):
        """Test that embeddings are cached."""
        with patch('ai.embeddings.load_cache') as load_mock, \
             patch('ai.embeddings.save_cache') as save_mock:
            load_mock.return_value = {}

            # First call should create embedding
            get_embedding("Test text")
            assert save_mock.called

            # Mock cache hit
            import hashlib
            key = hashlib.sha256("Test text".encode()).hexdigest()
            load_mock.return_value = {key: mock_embedding}

            # Second call should use cache
            result = get_embedding("Test text")
            assert np.allclose(result, mock_embedding)

    def test_get_embedding_fallback(self, mock_embedding):
        """Test fallback to smaller model on error."""
        with patch('ai.embeddings.client.embeddings.create') as mock:
            # First call raises exception, second succeeds
            mock_response = MagicMock()
            mock_response.data = [MagicMock()]
            mock_response.data[0].embedding = mock_embedding.tolist()

            mock.side_effect = [Exception("API Error"), mock_response]

            with patch('ai.embeddings.load_cache', return_value={}), \
                 patch('ai.embeddings.save_cache'):
                result = get_embedding("Test text")
                assert isinstance(result, np.ndarray)
                assert mock.call_count == 2


@pytest.mark.unit
@pytest.mark.ai
class TestScorer:
    """Test similarity scoring."""

    def test_compute_similarity(self, mock_embedding, sample_strategies):
        """Test computing similarity scores."""
        strategies_dicts = [
            {"id": s[0], "name": s[1], "description": s[2], "embedding": s[3]}
            for s in sample_strategies
        ]

        results = compute_similarity(mock_embedding, strategies_dicts)

        assert len(results) == 3
        assert all("strategy" in r for r in results)
        assert all("score" in r for r in results)
        assert all(0 <= r["score"] <= 1 for r in results)

    def test_compute_similarity_sorted(self, mock_embedding, sample_strategies):
        """Test that results are sorted by score."""
        strategies_dicts = [
            {"id": s[0], "name": s[1], "description": s[2], "embedding": s[3]}
            for s in sample_strategies
        ]

        results = compute_similarity(mock_embedding, strategies_dicts)

        # Check descending order
        scores = [r["score"] for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_best_match(self, mock_embedding, sample_strategies):
        """Test getting the best match."""
        strategies_dicts = [
            {"id": s[0], "name": s[1], "description": s[2], "embedding": s[3]}
            for s in sample_strategies
        ]

        results = compute_similarity(mock_embedding, strategies_dicts)
        strategy, score = best_match(results)

        assert isinstance(strategy, str)
        assert isinstance(score, float)
        assert 0 <= score <= 1
        assert strategy in [s[1] for s in sample_strategies]

    def test_identical_vectors_high_score(self):
        """Test that identical vectors get high similarity."""
        vec = np.random.rand(100)
        strategies = [
            {"id": 1, "name": "Test", "description": "Test", "embedding": vec}
        ]

        results = compute_similarity(vec, strategies)
        assert results[0]["score"] > 0.99

    def test_orthogonal_vectors_low_score(self):
        """Test that orthogonal vectors get low similarity."""
        vec1 = np.array([1.0, 0.0, 0.0])
        vec2 = np.array([0.0, 1.0, 0.0])
        strategies = [
            {"id": 1, "name": "Test", "description": "Test", "embedding": vec2}
        ]

        results = compute_similarity(vec1, strategies)
        assert results[0]["score"] < 0.1


@pytest.mark.unit
@pytest.mark.ai
class TestReasoning:
    """Test GPT reasoning."""

    def test_explain_alignment(self, mock_openai_chat):
        """Test generating alignment explanation."""
        explanation = explain_alignment("Test text", "Innovation", 0.95)

        assert isinstance(explanation, str)
        assert len(explanation) > 0
        assert mock_openai_chat.called

    def test_explain_alignment_with_low_score(self, mock_openai_chat):
        """Test explanation with low score."""
        explanation = explain_alignment("Test text", "Innovation", 0.25)

        assert isinstance(explanation, str)
        assert mock_openai_chat.called

    def test_explain_alignment_prompt_formatting(self, mock_openai_chat):
        """Test that prompt is properly formatted."""
        text = "AI automation project"
        strategy = "Innovation"
        score = 0.87

        explain_alignment(text, strategy, score)

        # Check that the call was made with proper formatting
        assert mock_openai_chat.called
        call_args = mock_openai_chat.call_args
        messages = call_args.kwargs['messages']
        prompt = messages[0]['content']

        assert text in prompt
        assert strategy in prompt
        assert "0.87" in prompt
