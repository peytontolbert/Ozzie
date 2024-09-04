import math
import statistics
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class MathOperations:
    def __init__(self):
        self.logger = Logger("MathOperations")
        self.error_handler = ErrorHandler()

    def mean(self, numbers):
        try:
            return sum(numbers) / len(numbers)
        except Exception as e:
            self.error_handler.handle_error(e, "Error calculating mean")
            return None

    def median(self, numbers):
        try:
            return statistics.median(numbers)
        except Exception as e:
            self.error_handler.handle_error(e, "Error calculating median")
            return None

    def mode(self, numbers):
        try:
            return statistics.mode(numbers)
        except Exception as e:
            self.error_handler.handle_error(e, "Error calculating mode")
            return None

    def standard_deviation(self, numbers):
        try:
            return statistics.stdev(numbers)
        except Exception as e:
            self.error_handler.handle_error(e, "Error calculating standard deviation")
            return None

    def variance(self, numbers):
        try:
            return statistics.variance(numbers)
        except Exception as e:
            self.error_handler.handle_error(e, "Error calculating variance")
            return None

    def factorial(self, n):
        try:
            return math.factorial(n)
        except Exception as e:
            self.error_handler.handle_error(e, "Error calculating factorial")
            return None

    def fibonacci(self, n):
        try:
            a, b = 0, 1
            for _ in range(n):
                a, b = b, a + b
            return a
        except Exception as e:
            self.error_handler.handle_error(e, "Error calculating Fibonacci number")
            return None

    def is_prime(self, n):
        try:
            if n < 2:
                return False
            for i in range(2, int(math.sqrt(n)) + 1):
                if n % i == 0:
                    return False
            return True
        except Exception as e:
            self.error_handler.handle_error(e, "Error checking if number is prime")
            return None