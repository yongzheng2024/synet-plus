#!/usr/bin/env bash

# modified by yongzheng for unify the output logs
# PATH_TO_LOGS="ebgpfinal"
PATH_TO_LOGS="logs/ebgp_logs"
# modified by yongzheng for python2
# SYNET_SCRIPT="python ./eval_scripts/new_ebgp_eval.py"
SYNET_SCRIPT="python2 ./eval_scripts/new_ebgp_eval.py"

TOPO=$1
VALUES=$2
REQ_TYPE=$3
REQS=$4
FIXED=$5
SKETCH=$6
RUN_ID=$7

BASE=$(basename $TOPO | sed 's/.graphml//')

LOG_FILE="$PATH_TO_LOGS/$BASE-$SKETCH-$REQ_TYPE-$REQS-$FIXED-$RUN_ID.txt"

# added by yongzheng for ERROR as follows:
# cannot create ebgpfinal/xxx-xxx.txt: Directory nonexistent
# open read and write serialized/xxx_xxx.json
if [ ! -d "./${PATH_TO_LOGS}" ]; then
	mkdir -p $PATH_TO_LOGS
fi
if [ ! -d "./${PATH_TO_LOGS}/serialized" ]; then
	mkdir -p $PATH_TO_LOGS/serialized
fi

echo "Running topology=$BASE reqs_type=$REQ_TYPE num_reqs=$REQS fixed=$FIXED sketch=$SKETCH run-id=$RUN_ID"
echo "Command $SYNET_SCRIPT $TOPO --values=$VALUES --type=$REQ_TYPE --reqsize=$REQS --fixed=$FIXED --sketch=$SKETCH"

START=$(date +%s)
stdbuf -oL $SYNET_SCRIPT $TOPO --values=$VALUES --type=$REQ_TYPE --reqsize=$REQS --fixed=$FIXED --sketch=$SKETCH > $LOG_FILE 2>&1
END=$(date +%s)

TIME=$((END-START))
echo "Total time: $TIME" >> $LOG_FILE
