import pytest
import tempfile
import os
import sys
import numpy as np
import pandas as pd
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from utils.file_loader import load_text_from_file, load_pdf, load_docx, load_txt
from utils.chunker import basic_paragraph_split, sanitize, merge_short_paragraphs, agentic_chunk
from utils.viz import radar_chart, pca_semantic_map, heatmap


@pytest.mark.unit
@pytest.mark.utils
class TestFileLoader:
    """Test file loading utilities."""

    def test_load_txt(self):
        """Test loading text file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Test content\nLine 2")
            temp_path = f.name

        try:
            content = load_txt(temp_path)
            assert content == "Test content\nLine 2"
        finally:
            os.unlink(temp_path)

    def test_load_text_from_file_txt(self):
        """Test loading via main function with .txt."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Test content")
            temp_path = f.name

        try:
            content = load_text_from_file(temp_path)
            assert content == "Test content"
        finally:
            os.unlink(temp_path)

    def test_load_text_from_file_unsupported(self):
        """Test error on unsupported file type."""
        with pytest.raises(ValueError, match="Unsupported file type"):
            load_text_from_file("test.xyz")

    def test_load_txt_with_encoding_errors(self):
        """Test handling encoding errors gracefully."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Test content")
            temp_path = f.name

        try:
            content = load_txt(temp_path)
            assert isinstance(content, str)
        finally:
            os.unlink(temp_path)


@pytest.mark.unit
@pytest.mark.utils
class TestChunker:
    """Test text chunking utilities."""

    def test_basic_paragraph_split(self):
        """Test basic paragraph splitting."""
        text = "Paragraph 1.\n\nParagraph 2.\n\nParagraph 3."
        chunks = basic_paragraph_split(text)
        assert len(chunks) == 3
        assert chunks[0] == "Paragraph 1."
        assert chunks[1] == "Paragraph 2."
        assert chunks[2] == "Paragraph 3."

    def test_basic_paragraph_split_removes_empty(self):
        """Test that empty paragraphs are removed."""
        text = "Paragraph 1.\n\n\n\nParagraph 2."
        chunks = basic_paragraph_split(text)
        assert len(chunks) == 2

    def test_sanitize(self):
        """Test text sanitization."""
        text = "Test   with    spaces\xa0and\nnewlines"
        clean = sanitize(text)
        assert "  " not in clean
        assert "\xa0" not in clean
        assert clean == "Test with spaces and newlines"

    def test_merge_short_paragraphs(self):
        """Test merging short paragraphs."""
        paragraphs = ["Title", "This is a longer paragraph that should not be merged."]
        merged = merge_short_paragraphs(paragraphs, min_length=20)
        assert len(merged) == 1
        assert "Title" in merged[0]

    def test_merge_short_paragraphs_keeps_long(self):
        """Test that long paragraphs are kept separate."""
        paragraphs = [
            "This is a long paragraph that should not be merged with others.",
            "This is another long paragraph that should be kept separate."
        ]
        merged = merge_short_paragraphs(paragraphs, min_length=20)
        assert len(merged) == 2

    def test_agentic_chunk_basic(self):
        """Test agentic chunking in basic mode."""
        text = "Para 1.\n\nPara 2.\n\nPara 3."
        chunks = agentic_chunk(text, mode="basic")
        assert len(chunks) == 3

    def test_agentic_chunk_merged(self):
        """Test agentic chunking in merged mode."""
        text = "Short\n\nAnother short\n\nThis is a much longer paragraph."
        chunks = agentic_chunk(text, mode="merged")
        assert len(chunks) < 3

    def test_agentic_chunk_auto(self):
        """Test agentic chunking in auto mode."""
        text = "Paragraph 1.\n\nParagraph 2.\n\nParagraph 3."
        chunks = agentic_chunk(text, mode="auto")
        assert len(chunks) >= 1

    def test_agentic_chunk_handles_empty(self):
        """Test that empty text is handled."""
        text = ""
        chunks = agentic_chunk(text)
        assert len(chunks) == 0


@pytest.mark.unit
@pytest.mark.utils
class TestVisualization:
    """Test visualization utilities."""

    def test_radar_chart_creation(self):
        """Test radar chart creation."""
        similarity_dict = {
            "Innovation": 0.9,
            "Sustainability": 0.7,
            "Excellence": 0.8
        }
        chart = radar_chart(similarity_dict)
        assert chart is not None

    def test_radar_chart_with_custom_title(self):
        """Test radar chart with custom title."""
        similarity_dict = {"Test": 0.5}
        chart = radar_chart(similarity_dict, title="Custom Title")
        assert chart is not None
        assert chart.title == "Custom Title"

    def test_pca_semantic_map_insufficient_data(self, patch_db_path):
        """Test PCA map with insufficient data."""
        result = pca_semantic_map()
        assert result is None

    def test_pca_semantic_map_with_data(self, patch_db_path, mock_embedding):
        """Test PCA map with sufficient data."""
        from db.db_utils import insert_content, insert_chunk

        # Insert test data
        content_id = insert_content("Test", "Innovation", 0.9)
        insert_chunk(content_id, "Chunk 1", "Innovation", 0.9, "Explanation", mock_embedding)
        insert_chunk(content_id, "Chunk 2", "Sustainability", 0.8, "Explanation", mock_embedding * 0.9)

        result = pca_semantic_map()
        assert result is not None

    def test_heatmap_creation(self):
        """Test heatmap creation."""
        similarity_matrix = [
            [0.9, 0.7, 0.6],
            [0.8, 0.9, 0.5],
        ]
        chunk_labels = ["Chunk 1", "Chunk 2"]
        strategy_labels = ["Innovation", "Sustainability", "Excellence"]

        chart = heatmap(similarity_matrix, chunk_labels, strategy_labels)
        assert chart is not None

    def test_heatmap_with_single_chunk(self):
        """Test heatmap with single chunk."""
        similarity_matrix = [[0.9, 0.8]]
        chunk_labels = ["Chunk 1"]
        strategy_labels = ["Innovation", "Sustainability"]

        chart = heatmap(similarity_matrix, chunk_labels, strategy_labels)
        assert chart is not None
