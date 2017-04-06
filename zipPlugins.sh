#!/bin/bash -x

#ymd=$(date +%Y%m%d)
#find . -name "plugin.xml" -print -exec sed -i "" "s/^<version.*$/<version>${ymd}<\/version>/"  {} \;
## * because we ignore .git those hidden folder
#find . -not -name ".*" -type d  -maxdepth 1 -print -exec zip -r {}_v${ymd}.zip {} \;

plugin_name="footnotes-regenerator"
ymd=$(date -r ./${plugin_name}/plugin.py +%Y%m%d)
sed -i "" "s/^<version.*$/<version>${ymd}<\/version>/" ./${plugin_name}/plugin.xml
zip -r ${plugin_name}_v${ymd}.zip ${plugin_name}/*

plugin_name="full-width-digit"
ymd=$(date -r ./${plugin_name}/plugin.py +%Y%m%d)
sed -i "" "s/^<version.*$/<version>${ymd}<\/version>/" ./${plugin_name}/plugin.xml
zip -r ${plugin_name}_v${ymd}.zip ${plugin_name}/*

plugin_name="full-width-punctuation"
ymd=$(date -r ./${plugin_name}/plugin.py +%Y%m%d)
sed -i "" "s/^<version.*$/<version>${ymd}<\/version>/" ./${plugin_name}/plugin.xml
zip -r ${plugin_name}_v${ymd}.zip ${plugin_name}/*

plugin_name="kobo-footnotes-enhance"
ymd=$(date -r ./${plugin_name}/plugin.py +%Y%m%d)
sed -i "" "s/^<version.*$/<version>${ymd}<\/version>/" ./${plugin_name}/plugin.xml
zip -r ${plugin_name}_v${ymd}.zip ${plugin_name}/*

plugin_name="vertical-cjk-punctuation"
ymd=$(date -r ./${plugin_name}/plugin.py +%Y%m%d)
sed -i "" "s/^<version.*$/<version>${ymd}<\/version>/" ./${plugin_name}/plugin.xml
zip -r ${plugin_name}_v${ymd}.zip ${plugin_name}/*

plugin_name="vertical-rtl"
ymd=$(date -r ./${plugin_name}/plugin.py +%Y%m%d)
sed -i "" "s/^<version.*$/<version>${ymd}<\/version>/" ./${plugin_name}/plugin.xml
zip -r ${plugin_name}_v${ymd}.zip ${plugin_name}/*

