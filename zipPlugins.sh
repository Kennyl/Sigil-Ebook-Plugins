#!/bin/bash -x

ymd=$(date +%Y%m%d)

find . -name "plugin.xml" -exec sed -i "s/^<version>.*$/<version>${ymd}<\/version>/"  {} \;

# * because we ignore .git those hidden folder
find * -type d -exec zip -r {}_v${ymd}.zip {} \;
