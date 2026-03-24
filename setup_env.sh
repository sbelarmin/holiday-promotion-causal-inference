#!/bin/bash
set -e

PROJECT_NAME=$(basename "$PWD")

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt ipykernel

python -m ipykernel install \
  --user \
  --name "${PROJECT_NAME}-venv" \
  --display-name "Python (${PROJECT_NAME})"

echo "✅ Environment ready for ${PROJECT_NAME}"