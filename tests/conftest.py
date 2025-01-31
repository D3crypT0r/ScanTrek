import pytest
import redis
from fakeredis import FakeRedis

@pytest.fixture(scope="session")
def redis_server():
    return FakeRedis()

@pytest.fixture
def mock_redis(redis_server):
    redis_server.flushall()
    return redis_server

@pytest.fixture
def sample_html():
    return """
    <html>
        <body>
            <a href="/page1">Link 1</a>
            <a href="/page2.pdf">PDF</a>
            <script src="app.js"></script>
        </body>
    </html>
    """
