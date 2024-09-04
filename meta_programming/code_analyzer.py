import ast
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class CodeAnalyzer:
    def __init__(self):
        self.logger = Logger("CodeAnalyzer")
        self.error_handler = ErrorHandler()

    def analyze_code(self, code):
        try:
            tree = ast.parse(code)
            analysis = {
                "classes": self._analyze_classes(tree),
                "functions": self._analyze_functions(tree),
                "imports": self._analyze_imports(tree),
                "complexity": self._analyze_complexity(tree)
            }
            return analysis
        except Exception as e:
            self.error_handler.handle_error(e, "Error analyzing code")
            return None

    def _analyze_classes(self, tree):
        return [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

    def _analyze_functions(self, tree):
        return [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

    def _analyze_imports(self, tree):
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.append(f"{node.module}.{node.names[0].name}")
        return imports

    def _analyze_complexity(self, tree):
        class ComplexityVisitor(ast.NodeVisitor):
            def __init__(self):
                self.complexity = 1

            def visit_If(self, node):
                self.complexity += 1
                self.generic_visit(node)

            def visit_For(self, node):
                self.complexity += 1
                self.generic_visit(node)

            def visit_While(self, node):
                self.complexity += 1
                self.generic_visit(node)

            def visit_FunctionDef(self, node):
                self.complexity += 1
                self.generic_visit(node)

        visitor = ComplexityVisitor()
        visitor.visit(tree)
        return visitor.complexity

    def suggest_improvements(self, analysis):
        suggestions = []
        if analysis["complexity"] > 10:
            suggestions.append("Consider breaking down complex functions or methods.")
        if len(analysis["imports"]) > 15:
            suggestions.append("Consider organizing imports or using specific imports instead of wildcard imports.")
        if len(analysis["functions"]) > 20:
            suggestions.append("Consider splitting the module into smaller, more focused modules.")
        return suggestions