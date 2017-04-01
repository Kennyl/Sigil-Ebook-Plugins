#!/bin/bash -x

find * -type d -exec zip  -r {}.zip  {} \;
