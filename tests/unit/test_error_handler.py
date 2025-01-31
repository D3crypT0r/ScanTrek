import pytest
from unittest.mock import patch
from utils.error_handler import ErrorHandler
import logging

def test_error_retry_logic(capsys):
    mock_func = pytest.fail
    retries = 3
    
    @ErrorHandler.retry
    def failing_function():
        raise ConnectionError("Test error")
    
    with pytest.raises(ConnectionError):
        failing_function()
    
    captured = capsys.readouterr()
    assert "Retry 1/3" in captured.out
    assert "Retry 2/3" in captured.out
    assert "Retry 3/3" in captured.out

def test_non_retry_error():
    @ErrorHandler.retry
    def critical_error():
        raise ValueError("Non-retry error")
    
    with pytest.raises(ValueError):
        critical_error()

@patch('utils.error_handler.logging.error')
def test_error_handling(mock_log):
    test_error = RuntimeError("Test error")
    context = "TEST_CONTEXT"
    
    ErrorHandler.handle(test_error, context)
    
    mock_log.assert_called_with(
        "[RuntimeError] Test error | Context: TEST_CONTEXT"
    )

def test_error_handler_config():
    handler = ErrorHandler(max_retries=5, backoff_factor=0.5)
    
    @handler.retry
    def test_func():
        raise TimeoutError
    
    with pytest.raises(TimeoutError):
        test_func()
    
    assert handler.max_retries == 5
    assert handler.backoff_factor == 0.5
