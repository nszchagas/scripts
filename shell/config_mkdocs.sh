#!/bin/bash

# Configuring python environment
pipenv --python 3.9

pipenv run pip install mkdocs mkdocs-material

# Creating mkdocs 

pipenv run mkdocs new .

# Configuring deploy ci for github

mkdir -p .github/workflows/
echo "name: deploy
on:
  push:
    branches:
      - master 
      - main
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.
      - run: pip install mkdocs-material
      - run: mkdocs gh-deploy --force
" >> .github/workflows/deploy.yml












