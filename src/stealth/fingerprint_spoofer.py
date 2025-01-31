import platform
import hashlib
from fake_useragent import UserAgent
import ssl

class FingerprintGenerator:
    def __init__(self):
        self.ua = UserAgent()
        self.tls_versions = [
            ssl.PROTOCOL_TLSv1_2,
            ssl.PROTOCOL_TLSv1_1,
            ssl.PROTOCOL_TLSv1
        ]
        
    def generate_fingerprint(self):
        return {
            "user_agent": self.ua.random,
            "platform": self._get_platform(),
            "tls_fingerprint": self._generate_tls_hash(),
            "timezone": random.choice(["America/New_York", "Europe/London", "Asia/Tokyo"]),
            "screen_res": f"{random.randint(1200,3840)}x{random.randint(800,2160)}",
            "fonts": self._generate_font_list()
        }

    def _get_platform(self):
        return {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "architecture": platform.architecture()[0]
        }

    def _generate_tls_hash(self):
        tls_config = {
            "version": random.choice(self.tls_versions),
            "cipher": random.choice(ssl._DEFAULT_CIPHERS.split(":")),
            "extension_order": random.sample(["ALPN", "SNI", "EC"], 3)
        }
        return hashlib.sha256(str(tls_config).encode()).hexdigest()

    def _generate_font_list(self):
        base_fonts = ["Arial", "Times New Roman", "Verdana"]
        extra_fonts = random.sample(["Helvetica", "Georgia", "Courier New"], 2)
        return base_fonts + extra_fonts
