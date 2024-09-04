from utils.logger import Logger
from utils.error_handler import ErrorHandler

class AlertSystem:
    def __init__(self):
        self.logger = Logger("AlertSystem")
        self.error_handler = ErrorHandler()

    def send_alert(self, alert_level, message):
        if alert_level == "INFO":
            self.logger.info(f"ALERT: {message}")
        elif alert_level == "WARNING":
            self.logger.warning(f"ALERT: {message}")
        elif alert_level == "ERROR":
            self.logger.error(f"ALERT: {message}")
        elif alert_level == "CRITICAL":
            self.logger.critical(f"ALERT: {message}")
        else:
            self.error_handler.handle_error(ValueError(f"Invalid alert level: {alert_level}"))

    def cpu_usage_alert(self, usage):
        if usage > 90:
            self.send_alert("CRITICAL", f"CPU usage is critically high: {usage}%")
        elif usage > 80:
            self.send_alert("WARNING", f"CPU usage is high: {usage}%")

    def memory_usage_alert(self, usage):
        if usage > 90:
            self.send_alert("CRITICAL", f"Memory usage is critically high: {usage}%")
        elif usage > 80:
            self.send_alert("WARNING", f"Memory usage is high: {usage}%")

    def disk_usage_alert(self, usage):
        if usage > 90:
            self.send_alert("CRITICAL", f"Disk usage is critically high: {usage}%")
        elif usage > 80:
            self.send_alert("WARNING", f"Disk usage is high: {usage}%")

    def network_alert(self, sent_rate, recv_rate):
        if sent_rate > 1000 or recv_rate > 1000:  # 1000 KB/s
            self.send_alert("WARNING", f"High network activity: Sent {sent_rate:.2f} KB/s, Received {recv_rate:.2f} KB/s")