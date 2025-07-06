#!/bin/bash
#set -e
#buildozer --allow-root android clean
#buildozer --allow-root android debug



set -e

# Run clean only if you pass 'clean' as an argument
if [[ "$1" == "clean" ]]; then
  echo "Running clean build..."
  buildozer --allow-root android clean
fi

buildozer --allow-root android debug
