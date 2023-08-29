#!/bin/bash

# Global variables
unb_home="$(realpath ~/Documents/unb/)"
github_user=nszchagas
script_home="$(pwd)"

function config_pipeline() {
  cd $path
  print "Creating pipeline in: $path/.github/workflows/deploy.yml"
  mkdir -p $path/.github/workflows
  cp $script_home/unb_templates/deploy.yml $path/.github/workflows/deploy.yml
}

function config_mkdocs() {
  if [[ -f $path/mkdocs.yml ]]; then
    print "Mkdocs already configured. Exiting stage..."
    return 0
  fi

  cd $path
  declare -A COLORS=(
    ["1"]='\033[0;32mgreen\033[0m'
    ["2"]='\033[0;36mblue\033[0m'
    ["3"]='\033[0;34mindigo\033[0m'
    ["4"]='\033[0;35mdeep purple\033[0m'
    ["5"]='\033[1;35mpink\033[0m'
    ["6"]='\033[0;31mred\033[0m'
  )

  echo -e "MKDOCS color options: "
  for code in "${!COLORS[@]}"; do
    echo -e "$code) ${COLORS[$code]}${RESET_COLOR}"
  done

  read -p "Choose the color for $sub: (code 1-6)" opt_1

  export COLOR=${COLORS[$opt_1]}
  echo -e "Color chosen: $COLOR"
  read -p "Enter description for $sub: " sub_description

  export sub=$sub
  export sub_description=$sub_description
  echo -e "Configuration:\nColor chosen: $COLOR.\nDescription: $sub_description"

  pipenv --python 3.9
  pipenv install mkdocs mkdocs-material
  pipenv run mkdocs new .

  envsubst <$script_home/unb_templates/mkdocs.yml >mkdocs.yml

  print "Creating codes and styles structure..."
  mkdir codes
  mkdir -p docs/stylesheets/
  cp $script_home/unb_templates/extra.css docs/stylesheets/extra.css

}

print() {
  GREEN='\033[0;32m'
  RESET_COLOR='\033[0m'
  echo -e "${GREEN}[INFO $(date +"%Y-%m-%d %T")] $1${RESET_COLOR}"
}

setup_dir() {
  if ! [[ -d $unb_home ]]; then
    print "Starting unb_home at $unb_home."
    mkdir -p $unb_home || return 1
    print "Done! ($unb_home)"
  fi
}

setup_git() {
  path=$(realpath "$unb_home/$sub")
  mkdir -p $path
  cd $path

  remote_url="git@github.com:$github_user/$sub-notes.git"

  if ! [[ -d "$path"/.git/ ]]; then
    print "Initializing empty git at $path."
    cd $path && git init . || {
      print "Error initializing git repository at $path"
      return 1
    }
  else
    print "Git already configured."
  fi

  if ! git remote | grep -q "origin"; then
    print "Adding remote origin: $remote_url"
    git remote add origin $remote_url
    git branch -M main
    git push -u origin main
  fi
}

main() {
  setup_dir
  subjects="$@"

  print "Creating structure for subjects: $@"
  for sub in $subjects; do
    sub=${sub^^}
    path=$(realpath "$unb_home/$sub")
    setup_git
    config_mkdocs
    config_pipeline

  done

}

main $@
