#!/bin/bash -x

#ymd=$(date +%Y%m%d)
#find . -name "plugin.xml" -print -exec sed -i "" "s/^<version.*$/<version>${ymd}<\/version>/"  {} \;
## * because we ignore .git those hidden folder
#find . -not -name ".*" -type d  -maxdepth 1 -print -exec zip -r {}_v${ymd}.zip {} \;
plugins=( \
"footnotes-regenerator" \
"full-width-digit" \
"full-width-punctuation" \
"kobo-footnotes-enhance" \
"vertical-cjk-punctuation" \
"vertical-rtl" \
"test-plugin" \
"prompt-user-example" \
)

for plugin_name in ${plugins[@]}
do
  ymd=$(date -r ${plugin_name}/plugin.py +%Y%m%d)
  # rm ${plugin_name}_v*.zip
  sed -i "" "s/^<version.*$/<version>${ymd}<\/version>/" ${plugin_name}/plugin.xml
  zip -r ${plugin_name}_v${ymd}.zip ${plugin_name}/*
done
