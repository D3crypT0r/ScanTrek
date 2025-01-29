import redis
from hashlib import sha256
import json

class DistributedQueue:
    def __init__(self, redis_host='localhost', redis_port=6379):
        self.redis = redis.Redis(
            host=redis_host,
            port=redis_port,
            password='your_secure_password',
            decode_responses=True
        )
        self.queue_name = 'crawler:queue'
        self.lock_name = 'crawler:lock'
        
    def push_task(self, url, depth=0, priority=1):
        task = {
            'url': url,
            'depth': depth,
            'priority': priority,
            'hash': sha256(url.encode()).hexdigest()
        }
        self.redis.zadd(self.queue_name, {json.dumps(task): priority})

    def pop_task(self):
        with self.redis.lock(self.lock_name, timeout=5):
            tasks = self.redis.zrevrange(self.queue_name, 0, 0)
            if tasks:
                task = json.loads(tasks[0])
                self.redis.zrem(self.queue_name, tasks[0])
                return task
        return None

    def task_count(self):
        return self.redis.zcard(self.queue_name)

class TaskDistributor:
    def __init__(self, nodes=3):
        self.queues = [DistributedQueue() for _ in range(nodes)]
        
    def balance_load(self, task):
        node_index = hash(task['url']) % len(self.queues)
        self.queues[node_index].push_task(**task)
