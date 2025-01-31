import time
import numpy as np
from collections import deque

class AdaptiveThrottler:
    def __init__(self, max_requests=50, timeframe=60):
        self.request_log = deque()
        self.max_requests = max_requests
        self.timeframe = timeframe
        self.block_duration = 300  
        
    def check_rate_limit(self):
        self._clean_old_entries()
        if len(self.request_log) >= self.max_requests:
            time.sleep(self._calculate_sleep_time())
            
        self.request_log.append(time.time())

    def _clean_old_entries(self):
        now = time.time()
        while self.request_log and now - self.request_log[0] > self.timeframe:
            self.request_log.popleft()

    def _calculate_sleep_time(self):
        if len(self.request_log) < 2:
            return 1.0
            
        intervals = np.diff(self.request_log)
        avg_interval = np.mean(intervals)
        std_dev = np.std(intervals)
        
        return max(0.5, avg_interval + 2*std_dev + random.uniform(0, 0.3))

class RequestPatternMasker:
    def __init__(self):
        self.normal_distribution = []
        
    def humanize_timing(self, base_delay):
        jitter = random.choice([
            lambda x: x * random.uniform(0.8, 1.2),
            lambda x: x + random.uniform(-0.1, 0.1)
        ])
        return max(0.5, jitter(base_delay))
    
    def randomize_mouse_movements(self, driver):
        actions = webdriver.ActionChains(driver)
        for _ in range(random.randint(2,5)):
            x_offset = random.randint(-10,10)
            y_offset = random.randint(-10,10)
            actions.move_by_offset(x_offset, y_offset)
            actions.pause(random.uniform(0.1, 0.3))
        actions.perform()
