#!/bin/bash

set -euo pipefail

if [ "$#" -ne 2 ]; then
    echo "Must provide <current_version> and <new_version> arguments"
    exit 1
fi

entry_exists=$(grep "$(echo "$2" | sed 's/\./\\./g')" CHANGELOG.rst) || (echo "You must add an entry for $2 in CHANGELOG.rst" && exit 1)

echo previous_version: $1
echo new_version: $2

sed -i "s/$1/$2/g" src/pdmongo/__init__.py
sed -i "s/$1/$2/g" README.rst
sed -i "s/$1/$2/g" setup.py
sed -i "s/$1/$2/g" docs/conf.py

git add src/pdmongo/__init__.py README.rst setup.py docs/conf.py
git commit -m "Release: v$2"
git tag -f "v$2"
git push -f --tags
sleep 10

echo "Running checks"

tox

echo "Bump version $1 -> $2 complete"
