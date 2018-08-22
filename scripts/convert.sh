#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
ENV=$DIR"/../.env"
REQ=$DIR"/requirements.txt"

if [ ! -d "$ENV" ]; then
  mkdir $ENV
  virtualenv --no-site-packages -p python3 $ENV
  source $ENV"/bin/activate"
  pip install -r requirements.txt
else
  source $ENV"/bin/activate"
fi

python $DIR"/../src/convert.py" -d mnist
deactivate
