import subprocess

subprocess.call("virtualenv env", shell=True)

subprocess.call("source env/bin/activate && pip install -r requirements.txt", shell=True)
