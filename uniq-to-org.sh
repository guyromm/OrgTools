#!/bin/bash
while read x; do
    echo $x | sed -E 's/([0-9]+)/\1|/' | sed 's/^/|/'
    done