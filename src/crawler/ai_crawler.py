import asyncio
from urllib.parse import urljoin
from sklearn.ensemble import RandomForestClassifier
import numpy as np

class AICrawler:
    def __init__(self, start_url, model_path='models/priority_model.pkl'):
        self.start_url = start_url
        self.visited = set()
        self.queue = []
        self.model = self.load_model(model_path)
        self.session = None
        self.feature_vector = []

    async def start_crawl(self):
        async with aiohttp.ClientSession() as session:
            self.session = session
            self.queue.append((self.start_url, 0))
            while self.queue:
                url, depth = self.queue.pop(0)
                if self.should_crawl(url, depth):
                    await self.process_url(url, depth)

    async def process_url(self, url, depth):
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    content = await response.text()
                    self.analyze_content(url, content)
                    self.extract_links(content, depth)
                    self.visited.add(url)
        except Exception as e:
            print(f"Error crawling {url}: {str(e)}")

    def analyze_content(self, url, content):
        # Generate features for ML model
        features = self.extract_features(content)
        priority = self.model.predict([features])[0]
        self.feature_vector.append((url, features, priority))

    def extract_features(self, content):
        return np.array([
            len(content),
            len(content.split()),
            len(content.splitlines()),
            len(re.findall(r'<form', content)),
            len(re.findall(r'\.js', content))
        ])

class PriorityQueue:
    def __init__(self):
        self.queue = []
        
    def put(self, item, priority):
        heapq.heappush(self.queue, (-priority, item))
        
    def get(self):
        return heapq.heappop(self.queue)[1]
