#!/bin/bash

source env/bin/activate
echo "Compiling scss"
python -mscss < app/static/app.scss > app/static/app.css
deactivate