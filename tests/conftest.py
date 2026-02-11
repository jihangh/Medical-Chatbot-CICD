import pytest
from fastapi.testclient import TestClient

import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app  # Adjust if your main.py is nested

@pytest.fixture(scope="module")
def test_client():
    return TestClient(app)