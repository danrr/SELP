import subprocess

subprocess.call("virtualenv -p /usr/bin/python2.7 env &&"
                "source env/bin/activate && "
                "pip install -r requirements.txt && "
                "git clone https://github.com/creationix/nvm.git ./.nvm && "
                "cd ./.nvm && git checkout `git describe --abbrev=0 --tags` && "
                "source ./nvm.sh && "
                "nvm install stable && "
                "npm install -g coffee-script && cd .. && "
                "coffee -c app/static/app.coffee &&"
                "scss app/static/app.scss app/static/app.css", shell=True)
