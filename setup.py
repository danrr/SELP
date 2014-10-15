import subprocess

subprocess.call("virtualenv -p /usr/bin/python2.7 env", shell=True)

subprocess.call("source env/bin/activate && pip install -r requirements.txt", shell=True)
