import html
import bleach

class Sanitizer:
    ALLOWED_TAGS = bleach.ALLOWED_TAGS + ['br', 'p', 'div']
    ALLOWED_ATTRIBUTES = bleach.ALLOWED_ATTRIBUTES
    
    @staticmethod
    def sanitize_input(input_data):
        if isinstance(input_data, str):
            return bleach.clean(
                html.escape(input_data),
                tags=Sanitizer.ALLOWED_TAGS,
                attributes=Sanitizer.ALLOWED_ATTRIBUTES
            )
        return input_data

    @staticmethod
    def validate_url(url):
        parsed = urlparse(url)
        return all([parsed.scheme in ['http', 'https'], parsed.netloc])
