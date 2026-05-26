"""This module is the entrypoint of the robot."""

import os
import subprocess

script_directory = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_directory)

subprocess.run(["pip", "install", "--upgrade", "uv"])
subprocess.run(["uv", "run", "process.py"])
