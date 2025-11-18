import pytest
import sqlite3
import pickle
import numpy as np
from unittest.mock import patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from db.db_utils import (
    connect,
    fetch_strategies,
    insert_strategy,
    delete_strategy,
    insert_content,
    insert_chunk,
    fetch_content
)


@pytest.mark.unit
@pytest.mark.db
class TestDatabase:
    """Test database operations."""

    def test_connect(self, patch_db_path):
        """Test database connection."""
        conn = connect()
        assert conn is not None
        assert isinstance(conn, sqlite3.Connection)
        conn.close()

    def test_insert_and_fetch_strategies(self, patch_db_path, mock_embedding):
        """Test inserting and fetching strategies."""
        # Insert a strategy
        insert_strategy("Test Strategy", "Test description", mock_embedding)

        # Fetch strategies
        strategies = fetch_strategies()
        assert len(strategies) == 1
        assert strategies[0][1] == "Test Strategy"
        assert strategies[0][2] == "Test description"
        assert np.allclose(strategies[0][3], mock_embedding)

    def test_delete_strategy(self, patch_db_path, mock_embedding):
        """Test deleting a strategy."""
        # Insert a strategy
        insert_strategy("Test Strategy", "Test description", mock_embedding)
        strategies = fetch_strategies()
        strategy_id = strategies[0][0]

        # Delete the strategy
        delete_strategy(strategy_id)
        strategies = fetch_strategies()
        assert len(strategies) == 0

    def test_insert_content(self, patch_db_path):
        """Test inserting content."""
        content_id = insert_content("Test content", "Innovation", 0.95)
        assert content_id is not None
        assert content_id > 0

    def test_insert_chunk(self, patch_db_path, mock_embedding):
        """Test inserting a chunk."""
        content_id = insert_content("Test content", "Innovation", 0.95)
        insert_chunk(
            content_id,
            "Test chunk",
            "Innovation",
            0.95,
            "Test explanation",
            mock_embedding
        )

        # Verify chunk was inserted
        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM chunks WHERE content_id=?", (content_id,))
        count = cur.fetchone()[0]
        conn.close()

        assert count == 1

    def test_fetch_content(self, patch_db_path):
        """Test fetching content."""
        # Insert some content
        insert_content("Test 1", "Innovation", 0.95)
        insert_content("Test 2", "Sustainability", 0.85)

        # Fetch content
        df = fetch_content()
        assert df is not None
        assert len(df) == 2
        assert "text" in df.columns
        assert "best_match" in df.columns
        assert "score" in df.columns

    def test_strategy_embedding_serialization(self, patch_db_path, mock_embedding):
        """Test that embeddings are properly serialized/deserialized."""
        insert_strategy("Test", "Description", mock_embedding)
        strategies = fetch_strategies()

        retrieved_embedding = strategies[0][3]
        assert isinstance(retrieved_embedding, np.ndarray)
        assert np.allclose(retrieved_embedding, mock_embedding)

    def test_multiple_strategies(self, patch_db_path, mock_embedding):
        """Test handling multiple strategies."""
        insert_strategy("Strategy 1", "Description 1", mock_embedding)
        insert_strategy("Strategy 2", "Description 2", mock_embedding * 0.9)
        insert_strategy("Strategy 3", "Description 3", mock_embedding * 0.8)

        strategies = fetch_strategies()
        assert len(strategies) == 3

    def test_content_with_none_values(self, patch_db_path):
        """Test inserting content with None values."""
        content_id = insert_content("Test", None, None)
        assert content_id > 0

        df = fetch_content()
        assert len(df) == 1
