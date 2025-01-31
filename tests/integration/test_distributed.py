import pytest
import redis
import time
from unittest.mock import patch
from rq import Queue, Worker
from crawler.distributed_queue import DistributedQueue, TaskDistributor

@pytest.fixture
def redis_conn():
    return redis.Redis()

@pytest.fixture
def distributed_queue(redis_conn):
    return DistributedQueue(redis_host='localhost', redis_port=6379)

def test_task_distribution(distributed_queue):
    distributor = TaskDistributor(nodes=3)
    
    test_tasks = [
        {"url": f"http://test.com/page{i}", "priority": i} 
        for i in range(10)
    ]
    
    for task in test_tasks:
        distributor.balance_load(task)
    
    for i in range(3):
        queue = Queue(f'node_{i}', connection=distributed_queue.redis)
        assert 3 <= len(queue.jobs) <= 4  

def test_worker_processing(redis_conn, distributed_queue):
    test_queue = Queue('test_queue', connection=redis_conn)
    test_queue.enqueue('test_task', 'http://test.com')
    
    worker = Worker(['test_queue'], connection=redis_conn)
    worker.work(burst=True)  
    
    assert test_queue.count == 0
    assert redis_conn.llen('failed') == 0

@patch('crawler.distributed_queue.requests.get')
def test_failure_retry_logic(mock_get, distributed_queue):
    mock_get.side_effect = Exception("Simulated failure")
    
    distributed_queue.push_task("http://failing.com", 1)
    task = distributed_queue.pop_task()
    
    for attempt in range(3):
        try:
            requests.get(task['url'])
        except Exception:
            if attempt < 2:
                distributed_queue.push_task(task['url'], task['priority'])
    
    assert distributed_queue.task_count() == 0
    assert distributed_queue.redis.llen('failed_jobs') == 1

def test_worker_scaling(redis_conn):
    test_queue = Queue('scaling_test', connection=redis_conn)
    
    for i in range(100):
        test_queue.enqueue('process_task', i)
    
    start_time = time.time()
    workers = [Worker(['scaling_test'], connection=redis_conn) for _ in range(10)]
    for w in workers:
        w.work(burst=True)
    
    processing_time = time.time() - start_time
    assert processing_time < 2  

@pytest.mark.stresstest
def test_high_volume_workload(distributed_queue):
    for i in range(1000):
        distributed_queue.push_task(f"http://loadtest.com/page{i}", 1)
    
    workers = [Worker([distributed_queue.queue_name], 
              connection=distributed_queue.redis) for _ in range(20)]
    
    start = time.time()
    for w in workers:
        w.work(burst=True)
    
    total_time = time.time() - start
    assert total_time < 5  
    assert distributed_queue.task_count() == 0
