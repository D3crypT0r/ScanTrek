import random
from stem import Signal
from stem.control import Controller
import requests

class ProxyRotator:
    def __init__(self):
        self.proxies = []
        self.current_proxy = None
        self.tor_control_port = 9051
        self._load_providers()

    def _load_providers(self):
        self.proxies = [
            *self._get_free_proxies(),
            *self._get_premium_proxies(),
            *self._get_tor_proxies()
        ]
        random.shuffle(self.proxies)

    def _get_free_proxies(self):
        return [
            f"http://{proxy}" for proxy in 
            requests.get("https://free-proxy-list.net/").text.split("\n")[:50]
        ]

    def _get_tor_proxies(self):
        return ["socks5://localhost:9050"]

    def next_proxy(self):
        self.current_proxy = self.proxies.pop(0)
        self.proxies.append(self.current_proxy)
        
        if "socks5" in self.current_proxy:
            self._rotate_tor_circuit()
            
        return self.current_proxy

    def _rotate_tor_circuit(self):
        with Controller.from_port(port=self.tor_control_port) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)

class ProxyValidator:
    def __init__(self):
        self.test_url = "https://httpbin.org/ip"
        
    def validate_proxy(self, proxy):
        try:
            response = requests.get(
                self.test_url,
                proxies={"http": proxy, "https": proxy},
                timeout=10
            )
            return response.json()['origin'] in proxy
        except:
            return False
