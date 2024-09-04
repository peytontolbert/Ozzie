import ast
import astor
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class RefactoringEngine:
    def __init__(self):
        self.logger = Logger("RefactoringEngine")
        self.error_handler = ErrorHandler()

    def extract_method(self, code, start_line, end_line, new_method_name):
        try:
            tree = ast.parse(code)
            extractor = MethodExtractor(start_line, end_line, new_method_name)
            modified_tree = extractor.visit(tree)
            return astor.to_source(modified_tree)
        except Exception as e:
            self.error_handler.handle_error(e, "Error extracting method")
            return None

    def rename_variable(self, code, old_name, new_name):
        try:
            tree = ast.parse(code)
            renamer = VariableRenamer(old_name, new_name)
            modified_tree = renamer.visit(tree)
            return astor.to_source(modified_tree)
        except Exception as e:
            self.error_handler.handle_error(e, "Error renaming variable")
            return None

    def inline_variable(self, code, variable_name):
        try:
            tree = ast.parse(code)
            inliner = VariableInliner(variable_name)
            modified_tree = inliner.visit(tree)
            return astor.to_source(modified_tree)
        except Exception as e:
            self.error_handler.handle_error(e, "Error inlining variable")
            return None

class MethodExtractor(ast.NodeTransformer):
    def __init__(self, start_line, end_line, new_method_name):
        self.start_line = start_line
        self.end_line = end_line
        self.new_method_name = new_method_name

    def visit_FunctionDef(self, node):
        extracted_body = []
        new_body = []
        for stmt in node.body:
            if self.start_line <= stmt.lineno <= self.end_line:
                extracted_body.append(stmt)
            else:
                new_body.append(stmt)
        
        if extracted_body:
            new_method = ast.FunctionDef(
                name=self.new_method_name,
                args=ast.arguments(args=[], vararg=None, kwarg=None, defaults=[]),
                body=extracted_body,
                decorator_list=[]
            )
            new_body.insert(0, new_method)
            new_body.append(ast.Expr(ast.Call(func=ast.Name(id=self.new_method_name, ctx=ast.Load()), args=[], keywords=[])))
        
        node.body = new_body
        return node

class VariableRenamer(ast.NodeTransformer):
    def __init__(self, old_name, new_name):
        self.old_name = old_name
        self.new_name = new_name

    def visit_Name(self, node):
        if node.id == self.old_name:
            return ast.Name(id=self.new_name, ctx=node.ctx)
        return node

class VariableInliner(ast.NodeTransformer):
    def __init__(self, variable_name):
        self.variable_name = variable_name
        self.variable_value = None

    def visit_Assign(self, node):
        if isinstance(node.targets[0], ast.Name) and node.targets[0].id == self.variable_name:
            self.variable_value = node.value
            return None
        return node

    def visit_Name(self, node):
        if node.id == self.variable_name and isinstance(node.ctx, ast.Load) and self.variable_value:
            return self.variable_value
        return node