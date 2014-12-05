#!/bin/bash

echo "Starting instalation"
echo "Doing cleanup"
rm -rf .nvm/
rm -rf app/db_repository
rm -rf app/app.db
rm -rf test/db_repository
rm -rf test/test.db

#python
echo "Intalling python virtualenv + dependencies"
virtualenv -p /usr/bin/python2.7 env
source env/bin/activate
pip install -r requirements.txt

echo "Compiling scss"
scss app/static/app.scss app/static/app.css

#node
echo "Installing nvm"
git clone https://github.com/creationix/nvm.git ./.nvm
cd ./.nvm
git checkout `git describe --abbrev=0 --tags`
source ./nvm.sh
nvm install stable
npm install -g coffee-script

echo "Compilling coffee"
cd ..
coffee -c app/static/app.coffee

#db
echo "Creating database"
export PYTHONPATH=$PYTHONPATH:''
python scripts/db_create.py
python scripts/db_migrate.py
python scripts/db_upgrade.py
python scripts/db_reset.py

echo "Installation done"
deactivate