import waybackpy
from datetime import datetime

class WaybackMachine:
    def __init__(self, user_agent="QuantumCrawler/1.0"):
        self.user_agent = user_agent
        
    def get_archive_url(self, target_url):
        try:
            archive = waybackpy.Url(target_url, self.user_agent)
            return archive.newest().archive_url
        except waybackpy.exceptions.NoCDXRecordFound:
            return None

    def historical_snapshots(self, target_url, limit=5):
        cdx = waybackpy.CDXSnapshot(target_url)
        return [{
            'timestamp': snap.timestamp,
            'url': snap.archive_url,
            'status': snap.statuscode
        } for snap in cdx.snapshots()[:limit]]

class FallbackFetcher:
    def __init__(self):
        self.wayback = WaybackMachine()
        
    def fetch(self, url):
        try:
            response = requests.get(url)
            if response.status_code in [403, 404]:
                return self.fetch_archive(url)
            return response.content
        except requests.RequestException:
            return self.fetch_archive(url)

    def fetch_archive(self, url):
        archive_url = self.wayback.get_archive_url(url)
        if archive_url:
            return requests.get(archive_url).content
        return None
