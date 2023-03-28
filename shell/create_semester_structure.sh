#!/bin/bash

dest=$1
cd "$dest" || echo "Error!"

PIPELINE="name: deploy
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
"

function create_folders() {
  echo "Print all the subjects for this semester, separated by space. These are the folders and repos names."

  read -r subjects

  for sub in $subjects; do
    sub=${sub^^}
    sub_folder="$dest/$sub"
    echo "Creating folder structure for $sub, if doesn't exist."
    mkdir -p "$sub_folder"
    cd "$sub_folder" || exit 1
    git init .
    git branch -m "main"
    pipenv --python 3.9
    pipenv run pip install mkdocs mkdocs-material
    pipenv run mkdocs new .
  done
}

function create_pipeline() {
  for f in "$dest"*/; do
    echo "Creating pipeline in: $f/.github/workflows/deploy.yml"
    mkdir -p "$f/.github/workflows/"
    echo "$PIPELINE" >"$f/.github/workflows/deploy.yml"
    echo "Finished creating pipeline."
  done
}

function create_mkdocs_yml() {
  for f in "$dest"*/; do
    echo "Creating mkdocs.yml in: $f/mkdocs.yml"
    mkdir -p "$f/codes"
    subname="$(basename -- "$f")"
    echo "Print description for subject $subname:"
    read -r subdescription

    MKDOCS="site_name: $subdescription
copyright: 2022 Nicolas Souza
repo_name: $subname-notes
repo_url: https://github.com/nszchagas/$subname-notes

theme:
  name: material
  logo: _static/icon.png
  features:
    - content.code.annotate
    - content.code.copy
  favicon: _static/icon.png
  palette:
    - media: '(prefers-color-scheme: light)'
      scheme: default
      primary: blue grey
      toggle:
        icon: material/brightness-7
        name: Dark mode

    - media: '(prefers-color-scheme: dark)'
      scheme: slate
      primary: deep purple
      toggle:
        icon: material/brightness-4
        name: Light mode

markdown_extensions:
  - pymdownx.arithmatex:
      generic: true
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.inlinehilite
  - pymdownx.snippets:
      base_path: ['codes']
  - pymdownx.superfences
  - attr_list
  - pymdownx.emoji:
      emoji_index: !!python/name:materialx.emoji.twemoji
      emoji_generator: !!python/name:materialx.emoji.to_svg

extra_javascript:
  - js/mathjax.js
  - https://polyfill.io/v3/polyfill.min.js?features=es6
  - https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js

nav:
  - About: index.md
"
    echo "$MKDOCS" >"$f/mkdocs.yml"
    echo "Finished creating mkdocs patters."
  done
}

while true; do
  echo "
  1) Create folders, mkdocs and git repositories for specified subjects.
  2) Create pipelines
  3) Create patterned mkdocs.yml
  *) Exit
"
  read -r option
  case $option in
  1) create_folders ;;
  2) create_pipeline ;;
  3) create_mkdocs_yml ;;
  *) echo "Exiting" && exit 0 ;;
  esac
done
