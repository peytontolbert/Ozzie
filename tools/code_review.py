import subprocess
import sys
from typing import List, Tuple

def run_command(command: List[str]) -> Tuple[str, str]:
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode(), stderr.decode()

def run_flake8() -> str:
    stdout, stderr = run_command(["flake8", "."])
    return stdout or stderr

def run_pylint() -> str:
    stdout, stderr = run_command(["pylint", "."])
    return stdout or stderr

def run_mypy() -> str:
    stdout, stderr = run_command(["mypy", "."])
    return stdout or stderr

def generate_report(flake8_output: str, pylint_output: str, mypy_output: str) -> str:
    report = "Automated Code Review Report\n"
    report += "============================\n\n"
    
    report += "Flake8 Results:\n"
    report += "--------------\n"
    report += flake8_output + "\n\n"
    
    report += "Pylint Results:\n"
    report += "---------------\n"
    report += pylint_output + "\n\n"
    
    report += "MyPy Results:\n"
    report += "-------------\n"
    report += mypy_output + "\n"
    
    return report

def main():
    flake8_output = run_flake8()
    pylint_output = run_pylint()
    mypy_output = run_mypy()
    
    report = generate_report(flake8_output, pylint_output, mypy_output)
    
    with open("code_review_report.txt", "w") as f:
        f.write(report)
    
    print("Code review report generated: code_review_report.txt")

if __name__ == "__main__":
    main()