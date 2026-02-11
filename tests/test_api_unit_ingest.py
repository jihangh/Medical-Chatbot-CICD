from unittest.mock import patch
from app.utils.exceptions import AppBaseException



def test_ingest_docs_success(test_client):
    with patch("app.routes.rag_routes.create_vectors") as mock_create_vectors:
        mock_create_vectors.return_value = None
        response = test_client.post("/rag/vectorstore")
        assert response.status_code == 200
        assert response.json()["status"] == "Embeddings created and upserted to vector store"

def test_ingest_docs_failure(test_client):
    with patch("app.routes.rag_routes.create_vectors") as mock_create_vectors:
        mock_create_vectors.side_effect = AppBaseException("Test vector ingestion error")
        response = test_client.post("/rag/vectorstore")
        assert response.status_code == 500
        assert response.json()["detail"] == "Test vector ingestion error"

def test_ingest_docs_unexpected_failure(test_client):
    with patch("app.routes.rag_routes.create_vectors") as mock_create_vectors:
        mock_create_vectors.side_effect = Exception("Unexpected failure")
        response = test_client.post("/rag/vectorstore")
        assert response.status_code == 500
        assert response.json()["detail"] == "Internal error"
