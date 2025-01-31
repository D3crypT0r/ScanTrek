import pytest
from unittest.mock import MagicMock, patch
from crawler.ai_crawler import AICrawler
from urllib.parse import urlparse

@pytest.fixture
def mock_crawler():
    return AICrawler("http://test.com")

def test_url_prioritization(mock_crawler):
    test_urls = [
        ("http://test.com/login", 0.9),
        ("http://test.com/about", 0.2),
        ("http://test.com/secret.pdf", 0.95)
    ]
    
    for url, score in test_urls:
        mock_crawler.priority_queue.put(url, score)
    
    assert mock_crawler.priority_queue.get() == "http://test.com/secret.pdf"
    assert mock_crawler.priority_queue.qsize() == 2

@patch('crawler.ai_crawler.requests.get')
def test_js_detection(mock_get, mock_crawler):
    mock_response = MagicMock()
    mock_response.text = '<script src="app.js"></script>'
    mock_get.return_value = mock_response
    
    assert mock_crawler.is_js_site("http://test.com") is True

@patch('crawler.ai_crawler.requests.get')
def test_file_identification(mock_get, mock_crawler):
    mock_response = MagicMock()
    mock_response.headers = {'Content-Type': 'application/pdf'}
    mock_get.return_value = mock_response
    
    assert mock_crawler.identify_file_type("http://test.com/doc.pdf") == "pdf"
