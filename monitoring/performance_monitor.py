import psutil
import time
from utils.logger import Logger

class PerformanceMonitor:
    def __init__(self):
        self.logger = Logger("PerformanceMonitor")

    def monitor_cpu(self, interval=1, duration=60):
        start_time = time.time()
        while time.time() - start_time < duration:
            cpu_percent = psutil.cpu_percent(interval=interval)
            self.logger.info(f"CPU Usage: {cpu_percent}%")

    def monitor_memory(self, interval=1, duration=60):
        start_time = time.time()
        while time.time() - start_time < duration:
            memory = psutil.virtual_memory()
            self.logger.info(f"Memory Usage: {memory.percent}%")
            time.sleep(interval)

    def monitor_disk(self, interval=1, duration=60):
        start_time = time.time()
        while time.time() - start_time < duration:
            disk = psutil.disk_usage('/')
            self.logger.info(f"Disk Usage: {disk.percent}%")
            time.sleep(interval)

    def monitor_network(self, interval=1, duration=60):
        start_time = time.time()
        last_bytes_sent = psutil.net_io_counters().bytes_sent
        last_bytes_recv = psutil.net_io_counters().bytes_recv
        while time.time() - start_time < duration:
            time.sleep(interval)
            bytes_sent = psutil.net_io_counters().bytes_sent
            bytes_recv = psutil.net_io_counters().bytes_recv
            self.logger.info(f"Network sent: {(bytes_sent - last_bytes_sent) / interval / 1024:.2f} KB/s")
            self.logger.info(f"Network received: {(bytes_recv - last_bytes_recv) / interval / 1024:.2f} KB/s")
            last_bytes_sent = bytes_sent
            last_bytes_recv = bytes_recv

    def monitor_all(self, interval=1, duration=60):
        self.logger.info("Starting comprehensive system monitoring...")
        start_time = time.time()
        while time.time() - start_time < duration:
            self.monitor_cpu(interval=interval, duration=interval)
            self.monitor_memory(interval=interval, duration=interval)
            self.monitor_disk(interval=interval, duration=interval)
            self.monitor_network(interval=interval, duration=interval)
        self.logger.info("Comprehensive system monitoring completed.")