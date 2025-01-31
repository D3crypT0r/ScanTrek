from urllib.parse import urlparse, urlunparse, parse_qs
import tldextract

class UrlNormalizer:
    @staticmethod
    def normalize(url, base_domain=None):
        parsed = urlparse(url)
        
        scheme = parsed.scheme.lower() if parsed.scheme else 'http'
        netloc = parsed.netloc.lower()
        
        if ':' in netloc:
            host, port = netloc.split(':', 1)
            if (scheme == 'http' and port == '80') or (scheme == 'https' and port == '443'):
                netloc = host
                
        path = parsed.path.rstrip('/') or '/'
        
        query = parse_qs(parsed.query, keep_blank_values=True)
        filtered_query = {k: v for k,v in query.items() if k not in ['sessionid', 'token']}
        sorted_query = '&'.join(f'{k}={v[0]}' for k,v in sorted(filtered_query.items()))
        
        return urlunparse((
            scheme,
            netloc,
            path,
            parsed.params,
            sorted_query,
            parsed.fragment
        ))

    @staticmethod
    def is_same_domain(url1, url2):
        ext1 = tldextract.extract(url1)
        ext2 = tldextract.extract(url2)
        return (ext1.domain, ext1.suffix) == (ext2.domain, ext2.suffix)
