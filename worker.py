import argparse
import logging
import redis
from rq import Worker, Queue, Connection
from config.loader import ConfigLoader
from crawler.distributed_queue import DistributedQueue
from analysis.file_detectors import FileAnalyzer

ROLES = ['crawler', 'analyzer']

def run_worker():
    config = ConfigLoader()
    
    parser = argparse.ArgumentParser(description="QuantumCrawler Worker Node")
    parser.add_argument(
        "-r", "--role",
        choices=ROLES,
        required=True,
        help="Worker role type"
    )
    parser.add_argument(
        "-n", "--nodes",
        type=int,
        default=1,
        help="Number of worker instances"
    )
    
    args = parser.parse_args()
    
    redis_conn = redis.Redis(
        host=config.get('redis.host', 'localhost'),
        port=config.get('redis.port', 6379),
        password=config.get('redis.password', '')
    )
    
    with Connection(redis_conn):
        if args.role == 'crawler':
            worker = Worker(
                Queue('crawler', connection=redis_conn),
                name=f'crawler-{args.nodes}'
            )
            worker.work()
            
        elif args.role == 'analyzer':
            worker = Worker(
                Queue('analyzer', connection=redis_conn),
                name=f'analyzer-{args.nodes}'
            )
            worker.work()

def process_crawl_task(url):
    from crawler.ai_crawler import AICrawler
    crawler = AICrawler(base_url=url)
    return crawler.crawl_single(url)

def process_analysis_task(file_path):
    analyzer = FileAnalyzer()
    return analyzer.analyze(file_path)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    run_worker()
