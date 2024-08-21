import os
import subprocess
import tempfile
import sys
import re
from dotenv import get_key
from backend.modules.llms import pure_llama3

class LLM:
    def __init__(self):
        self.messages = []

    def ask(self, prompts: list, format: str = "", temperature: float = 0.8):
        """
        Args:
            prompts (list): A list of prompts to ask.
            format (str, optional): The format of the response. Use "json" for json. Defaults to "".
            temperature (float, optional): The temperature of the LLM. Defaults to 0.8.
        """
        return pure_llama3(prompts)  # Adjust based on your actual implementation
    
    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
    
    def run(self) -> str:
        return self.ask(self.messages)

class CodeBrew:
    def __init__(
            self,
            llm: LLM,
            maxRetries: int = 3,
            keepHistory: bool = True,
            verbose: bool = False,
            ) -> None:
        self.llm = llm
        self.maxRetries = maxRetries
        self.keepHistory = keepHistory
        self.verbose = verbose

    def filterCode(self, txt: str) -> str:
        pattern = r"```python(.*?)```"
        matches = re.findall(pattern, txt, re.DOTALL)
        return matches[0].strip() if matches else ""
    
    def pipPackages(self, *packages: str):
        python_executable = get_key(".env", "PYTHON_EXE")
        print(f"Installing {', '.join(packages)} with pip...")
        try:
            result = subprocess.run(
                [python_executable, "-m", "pip", "install", *packages],
                capture_output=True,
                check=True,
            )
            print(result.stdout.decode())
        except subprocess.CalledProcessError as e:
            print(e.stderr.decode(), file=sys.stderr)
            raise

    def _execute_script_in_subprocess(self, script: str) -> tuple[str, str, int]:
        output, error = "", ""
        return_code = 0
        python_executable = get_key(".env", "PYTHON_EXE")
        try:
            with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp_script:
                tmp_script_name = tmp_script.name
                tmp_script.write(script)
                tmp_script.flush()
                try:
                    process = subprocess.Popen(
                        [python_executable, tmp_script_name],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        stdin=subprocess.DEVNULL,
                        text=True,
                    )
                    for line in process.stdout:
                        output += line
                        if self.verbose:
                            print(line, end="")
                    for line in process.stderr:
                        error += line
                        if self.verbose:
                            print(line, end="", file=sys.stderr)
                    return_code = process.wait()
                finally:
                    os.remove(tmp_script_name)
        except Exception as e:
            error += str(e)
            print(e)
            return_code = 1
        return output, error, return_code

    def execute_script(self, script: str) -> tuple[str, str, int]:
        return self._execute_script_in_subprocess(script)
    
    def run(self, prompt: str) -> None:
        the_copy = self.llm.messages.copy()
        self.llm.add_message("user", prompt)
        _continue = True
        while _continue:
            _continue = False
            try:
                response = self.llm.run()
                self.llm.add_message("assistant", response)
                script = self.filterCode(response)
                if script:
                    output, error, return_code = self.execute_script(script)
                    if output:
                        self.llm.add_message("user", f"LAST SCRIPT OUTPUT:\n{output}")
                        if output.strip().endswith("CONTINUE"):
                            _continue = True
                    if error:
                        self.llm.add_message("user", f"Error: {error}")
                    if return_code != 0:
                        self.maxRetries -= 1
                        if self.maxRetries > 0:
                            print("Retrying...\n")
                            _continue = True
            except KeyboardInterrupt:
                break
        if not self.keepHistory:
            self.llm.messages = the_copy
