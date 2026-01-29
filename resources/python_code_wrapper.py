from pathlib import Path
from sys import path

path.insert(0, str(Path(__file__).parent))

import python_code

program = python_code.Program()

while True:
    program.run_iter()
