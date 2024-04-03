#!/bin/bash

set -a
source .env
set +a
python 3 app.py runserver 3000