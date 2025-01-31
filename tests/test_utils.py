def assert_valid_url(url):
    parsed = urlparse(url)
    assert parsed.scheme in ['http', 'https']
    assert '.' in parsed.netloc
    assert len(parsed.netloc) > 3

def generate_test_file(extension, content=None):
    from faker import Faker
    fake = Faker()
    
    content = content or fake.text()
    return io.BytesIO(content.encode())
