#!/usr/bin/env bash
set -e

if ! (which pyenv >/dev/null) ; then
  echo "!! You must use pyenv to use this setup script. Please install pyenv, pyenv-virtualenv. !!" >&2
  exit 1
fi

PYVER=$(cat ./.python-version | cut -d '/' -f 1)

pyenv install -s $PYVER
pyenv virtualenv $PYVER billtracker || echo "Could not create virtualenv -- is it already set up? If so: good."

echo "Setup of venv complete. You should be able to activate with: 'pyenv shell'"
