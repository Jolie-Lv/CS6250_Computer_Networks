#!/bin/bash

mkdir -p runlogs
rm runlogs/* 2>/dev/null
for i in *Topo.py; do
    j="$(basename "$i" .py)"
    /bin/echo -n Running $j Topo...
    python ./run_spanning_tree.py "$j" "$j".log > runlogs/$j.run.log
    echo done.  Comparing against log file.
    if [ -f ./Logs/$j.log ]; then
        if diff -w "$j".log ./Logs/"$j".log; then
            echo Looks good!
        else
            echo Differences found.
        fi
    else
        echo No log file to compare against.
    fi
done