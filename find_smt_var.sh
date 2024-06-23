#!/bin/bash

# target_line="SelectOneRmapLineIndex_84"
target_line="SelectOne_index_88"

target_file1="smt.smt2"             # before z3 solver
target_file2="smt_solvered.smt2"    # after z3 solver

output_file1=$target_line".txt"
output_file2=$target_line"_solvered.txt"

lines=""

rm -rf $output_file1
rm -rf $output_file2

while read -r line; do
    if [[ "$line" == *"(assert"* ]] || [[ "$line" == *"(check-sat)"* ]]; then
        if [[ "$lines" == *"$target_line"* ]]; then
            echo $lines >> $output_file1
        fi
        lines="$line"
    else
        lines="$lines""$line"
    fi
done < $target_file1

lines=""

while read -r line; do
    if [[ "$line" == *"(assert"* ]] || [[ "$line" == *"(check-sat)"* ]]; then
        if [[ "$lines" == *"$target_line"* ]]; then
            echo $lines >> $output_file2
        fi
        lines="$line"
    else
        lines="$lines""$line"
    fi
done < $target_file2
