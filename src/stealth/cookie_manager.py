import browser_cookie3
import datetime

class CookieEngine:
    def __init__(self):
        self.cookie_jar = {}
        
    def simulate_session(self, domain):
        self._load_common_cookies(domain)
        self._generate_session_cookies()
        return self.cookie_jar

    def _load_common_cookies(self, domain):
        for cookie in browser_cookie3.load(domain_name=domain):
            self.cookie_jar[cookie.name] = {
                "value": cookie.value,
                "domain": cookie.domain,
                "path": cookie.path,
                "expires": cookie.expires
            }

    def _generate_session_cookies(self):
        self.cookie_jar.update({
            "session_id": self._generate_session_id(),
            "last_activity": datetime.datetime.now().isoformat(),
            "tracking_enabled": random.choice(["0", "1"])
        })

    def _generate_session_id(self):
        return hashlib.sha256(str(random.getrandbits(256)).encode()).hexdigest()
