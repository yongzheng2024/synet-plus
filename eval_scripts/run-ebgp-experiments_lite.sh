#!/usr/bin/env bash

# Generate evaluation values for all given reqs
NUM_PROCESSES=1
NUM_REPEATS=1

PATH_TO_TOPOS="topos/*/"

for file in topos/small/Arnes;
do
    topo="${file}.graphml"
    values="${file}_ospf_reqs.py "

	for reqs in 1 2 4 8 16;
    do
        for req_type in "order" "simple";
        do
            for fixed in "0" "0.5";
            do
                for sketch in "abs" "attrs";
                do
                    for RUN_ID in $(seq 1 $NUM_REPEATS);
                    do
                        echo $topo $values $req_type $reqs $fixed $sketch $RUN_ID
                    done
				done
            done
        done
    done
done | xargs -n 7 -I{} -P $NUM_PROCESSES sh -c "sh ./eval_scripts/run-ebgp.sh {}"
