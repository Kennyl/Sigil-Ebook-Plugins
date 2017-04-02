#!/bin/sh
set -x

find . -name "*.py" -print -exec python -m py_compile {} \;
