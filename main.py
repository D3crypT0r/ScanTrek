import argparse
import logging
from config.loader import ConfigLoader
from crawler.ai_crawler import AICrawler
from reporting.json_reporter import JSONReporter
from utils.error_handler import ErrorHandler

def main():
    config = ConfigLoader()
    
    parser = argparse.ArgumentParser(
        description="QuantumCrawler - Advanced Web Security Scanner"
    )
    
    parser.add_argument(
        "-t", "--target",
        help="Target URL to scan",
        required=True
    )
    parser.add_argument(
        "-d", "--depth",
        type=int,
        default=config.get('crawler.max_depth', 5),
        help="Maximum crawl depth"
    )
    parser.add_argument(
        "-o", "--output",
        default="results",
        help="Output directory path"
    )
    
    parser.add_argument(
        "--distributed",
        action="store_true",
        help="Enable distributed crawling mode"
    )
    parser.add_argument(
        "--stealth",
        action="store_true",
        help="Enable anti-detection measures"
    )
    
    parser.add_argument(
        "--full-scan",
        action="store_true",
        help="Perform deep file analysis"
    )
    
    args = parser.parse_args()
    
    try:
        crawler = AICrawler(
            base_url=args.target,
            max_depth=args.depth,
            stealth_mode=args.stealth,
            config=config
        )
        
        if args.distributed:
            start_distributed_workers(config)
            
        crawler.start()
        
        reporter = JSONReporter()
        reporter.generate(
            crawler.findings,
            f"{args.output}/report.json"
        )
        
    except Exception as e:
        ErrorHandler.handle(e, "Main execution failed")
        exit(1)

def start_distributed_workers(config):
    from multiprocessing import Process
    from os import cpu_count
    
    workers = config.get('crawler.parallel_workers', cpu_count() * 2)
    for _ in range(workers):
        Process(target=run_worker, args=(config,)).start()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
