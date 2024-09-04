import ast
from utils.logger import Logger

class CodeAnalyzer:
    def __init__(self):
        self.logger = Logger("CodeAnalyzer")

    def analyze(self, code):
        try:
            ast.parse(code)
            return AnalysisResult(True, [])
        except SyntaxError as e:
            return AnalysisResult(False, [f"Syntax error: {str(e)}"])
        except Exception as e:
            return AnalysisResult(False, [f"Unknown error: {str(e)}"])

class AnalysisResult:
    def __init__(self, is_valid, errors):
        self.is_valid = is_valid
        self.errors = errors

    def has_errors(self):
        return not self.is_valid

    def get_errors(self):
        return self.errors