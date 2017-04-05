#!/bin/bash -x

ymd=$(date +%Y%m%d)

find . -name "plugin.xml" -print -exec sed -i "" "s/^<version.*$/<version>${ymd}<\/version>/"  {} \;

# * because we ignore .git those hidden folder
find . -not -name ".*" -type d  -maxdepth 1 -print -exec zip -r {}_v${ymd}.zip {} \;
