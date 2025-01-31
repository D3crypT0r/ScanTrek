import logging
import time
from functools import wraps

class ErrorHandler:
    RETRY_EXCEPTIONS = (ConnectionError, TimeoutError, HTTPError)
    
    def __init__(self, max_retries=3, backoff_factor=0.3):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.logger = logging.getLogger('QuantumCrawler')

    @classmethod
    def retry(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0] if args else None
            last_exception = None
            for attempt in range(1, self.max_retries+1 if self else 3+1):
                try:
                    return func(*args, **kwargs)
                except cls.RETRY_EXCEPTIONS as e:
                    last_exception = e
                    sleep_time = attempt * (self.backoff_factor if self else 0.3)
                    time.sleep(sleep_time)
                    cls.logger.warning(f"Retry {attempt}/{self.max_retries} for {func.__name__}")
            raise last_exception or Exception("Unknown error")
        return wrapper

    @staticmethod
    def handle(error, context=None):
        error_type = type(error).__name__
        error_msg = f"[{error_type}] {str(error)}"
        if context:
            error_msg += f" | Context: {context}"
            
        logging.error(error_msg)
        ErrorHandler._send_alert(error_msg)

    @staticmethod
    def _send_alert(message):
        pass
