#!/bin/bash

source .nvm/nvm.sh
nvm use stable
echo "Compilling coffee"
coffee -c app/static/app.coffee
