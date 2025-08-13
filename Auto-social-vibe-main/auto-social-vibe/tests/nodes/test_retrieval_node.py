from unittest.mock import AsyncMock, patch

import pytest

from app.nodes_and_edges.nodes.retrieval_node import retrieve_node


@patch("app.nodes_and_edges.nodes.retrieval_node.create_retriever")
@patch("app.nodes_and_edges.nodes.retrieval_node.db")
@pytest.mark.asyncio
async def test_retrieve_node(mock_db, mock_create_retriever, state):
    """
    Test the async retrieve_node function with mocked dependencies.
    """
    mock_retriever = AsyncMock()
    mock_retriever.ainvoke.return_value = [
        {"title": "Document 1", "content": "Content of Document 1"},
        {"title": "Document 2", "content": "Content of Document 2"},
    ]
    mock_create_retriever.return_value = mock_retriever
    updated_state = await retrieve_node(state)

    assert updated_state["context"] == [
        {"title": "Document 1", "content": "Content of Document 1"},
        {"title": "Document 2", "content": "Content of Document 2"},
    ]
    mock_create_retriever.assert_called_once_with(mock_db, k=2)
    mock_retriever.ainvoke.assert_called_once_with(state["question"])
