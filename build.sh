#!/bin/bash
#set -e
#buildozer --allow-root android clean
#buildozer --allow-root android debug


#!/bin/bash
set -e

if [ "$1" == "clean" ]; then
  echo "Requested clean build..."
  # Only run clean if p4a directory exists
  if [ -d ".buildozer/android/platform/python-for-android" ]; then
    buildozer --allow-root android clean
  else
    echo "Skipping clean: platform/python-for-android not found (likely first build)"
  fi
fi

# Always build
buildozer --allow-root android debug
