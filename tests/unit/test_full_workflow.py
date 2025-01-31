import pytest
from main import main
from unittest.mock import patch

@patch('crawler.ai_crawler.AICrawler.start')
def test_end_to_end_workflow(mock_crawl, tmp_path):
    test_args = [
        "main.py",
        "-t", "http://example.com",
        "-d", "2",
        "-o", str(tmp_path)
    ]
    
    with patch('sys.argv', test_args):
        main()
        
    report_file = tmp_path / "report.json"
    assert report_file.exists()
    assert report_file.stat().st_size > 0

@pytest.mark.distributed
@patch('worker.run_worker')
def test_distributed_workflow(mock_worker, redis_server):
    from crawler.distributed_queue import DistributedQueue
    queue = DistributedQueue()
    
    test_tasks = [
        {"url": "http://test.com/page1", "priority": 1},
        {"url": "http://test.com/page2", "priority": 2}
    ]
    
    for task in test_tasks:
        queue.push_task(task['url'], task['priority'])
    
    assert queue.task_count() == 2
    assert queue.pop_task()['url'] == "http://test.com/page2"
