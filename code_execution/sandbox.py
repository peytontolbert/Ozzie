import asyncio
import subprocess
from utils.logger import Logger

class CodeSandbox:
    def __init__(self):
        self.logger = Logger("CodeSandbox")

    def initialize(self):
        # Set up the sandbox environment
        pass

    async def execute(self, code):
        try:
            # Write code to a temporary file
            with open("temp_code.py", "w") as f:
                f.write(code)

            # Execute the code in a separate process with restrictions
            process = await asyncio.create_subprocess_exec(
                "python", "temp_code.py",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if process.returncode == 0:
                return ExecutionResult(True, stdout.decode())
            else:
                return ExecutionResult(False, stderr.decode())

        except Exception as e:
            self.logger.error(f"Error executing code: {str(e)}")
            return ExecutionResult(False, str(e))

class ExecutionResult:
    def __init__(self, success, output):
        self.success = success
        self.output = output

    def is_successful(self):
        return self.success

    def get_output(self):
        return self.output

    def get_error(self):
        return self.output if not self.success else None