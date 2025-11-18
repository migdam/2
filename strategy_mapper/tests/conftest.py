import pytest
import sqlite3
import numpy as np
import tempfile
import os
import sys
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def temp_db():
    """Create a temporary test database."""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    temp_db_path = temp_file.name
    temp_file.close()

    # Create schema
    conn = sqlite3.connect(temp_db_path)
    schema_path = os.path.join(os.path.dirname(__file__), '..', 'db', 'schema.sql')
    with open(schema_path) as f:
        conn.executescript(f.read())
    conn.close()

    yield temp_db_path

    # Cleanup
    if os.path.exists(temp_db_path):
        os.unlink(temp_db_path)


@pytest.fixture
def mock_embedding():
    """Return a mock embedding vector."""
    return np.random.rand(1536).astype(np.float32)


@pytest.fixture
def mock_openai_embedding(mock_embedding):
    """Mock OpenAI embedding API call."""
    with patch('ai.embeddings.client.embeddings.create') as mock:
        # Create mock response
        mock_response = MagicMock()
        mock_response.data = [MagicMock()]
        mock_response.data[0].embedding = mock_embedding.tolist()
        mock.return_value = mock_response
        yield mock


@pytest.fixture
def mock_openai_chat():
    """Mock OpenAI chat completion API call."""
    with patch('ai.reasoning.client.chat.completions.create') as mock:
        # Create mock response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "This is a test explanation."
        mock.return_value = mock_response
        yield mock


@pytest.fixture
def sample_strategies(mock_embedding):
    """Sample strategies for testing."""
    return [
        (1, "Innovation", "AI-driven products and automation", mock_embedding),
        (2, "Operational Excellence", "Process improvement and quality", mock_embedding * 0.9),
        (3, "Sustainability", "Environmental and social responsibility", mock_embedding * 0.8),
    ]


@pytest.fixture
def sample_text():
    """Sample text for testing."""
    return "We are developing new AI-powered products to automate business processes."


@pytest.fixture
def sample_chunks():
    """Sample chunks for testing."""
    return [
        "We are developing new AI-powered products.",
        "Our goal is to automate business processes.",
        "We focus on innovation and technology."
    ]


@pytest.fixture
def mock_embedding_cache():
    """Mock embedding cache."""
    with patch('ai.embeddings.load_cache') as load_mock, \
         patch('ai.embeddings.save_cache') as save_mock:
        load_mock.return_value = {}
        yield load_mock, save_mock


@pytest.fixture
def temp_upload_file():
    """Create a temporary upload file."""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w')
    temp_file.write("This is a test document.\n\nIt has multiple paragraphs.")
    temp_file.close()

    yield temp_file.name

    # Cleanup
    if os.path.exists(temp_file.name):
        os.unlink(temp_file.name)


@pytest.fixture
def patch_db_path(temp_db, monkeypatch):
    """Patch the DB_PATH to use temporary database."""
    monkeypatch.setattr('db.db_utils.DB_PATH', temp_db)
    monkeypatch.setattr('db.init_db.DB_PATH', temp_db)
    return temp_db


@pytest.fixture(autouse=True)
def env_setup(monkeypatch):
    """Set up environment variables for testing."""
    monkeypatch.setenv('OPENAI_API_KEY', 'test-key-12345')
