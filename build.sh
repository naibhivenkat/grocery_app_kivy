#!/bin/bash
set -e
buildozer --allow-root android clean
buildozer --allow-root android debug
