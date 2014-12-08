#!/bin/bash

source ./nvm.sh
echo "Compilling coffee"
coffee -c app/static/app.coffee
deactivate
