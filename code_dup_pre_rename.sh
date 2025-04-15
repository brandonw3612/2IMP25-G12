#!/bin/bash

# Change to the directory where the script is located
cd "$(dirname "$0")"

# Rename all .jsx files to .js
for file in *.jsx; do
  [ -e "$file" ] || continue  # Skip if no .jsx files
  mv -- "$file" "${file%.jsx}.js"
done

# Rename all .tsx files to .ts
for file in *.tsx; do
  [ -e "$file" ] || continue  # Skip if no .tsx files
  mv -- "$file" "${file%.tsx}.ts"
done

echo "Renaming complete"