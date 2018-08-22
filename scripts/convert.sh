#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
ENV=$DIR"/../.env"
REQ=$DIR"/../requirements.txt"

if [ ! -d "$ENV" ]; then
  mkdir $ENV
  virtualenv --no-site-packages -p python3 $ENV
fi

source $ENV"/bin/activate"
pip install -r $REQ

if [ ! -z "$1" ]; then
  python $DIR"/../src/convert.py" -d $1
else
  echo "Please specify data to convert."
fi

deactivate
