#!/bin/sh

if [ ! -d venv ]; then
  python3 -m venv venv
  source venv/bin/activate
  pip install flask
  pip install flask_cors
  pip install pinecone
fi
source venv/bin/activate
