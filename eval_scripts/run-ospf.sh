#!/usr/bin/env bash

# modified by yongzheng for unify the output logs
# PATH_TO_LOGS="logs"
PATH_TO_LOGS="logs/ospf_logs"
# modified by yongzheng for python2
# SYNET_SCRIPT="python ./eval_scripts/ospf_eval.py"
SYNET_SCRIPT="python2 ./eval_scripts/ospf_eval.py"

TOPO=$1
VALUES=$2
SYN=$3
REQ_TYPE=$4
REQS=$5
FIXED=$6
RUN_ID=$7

BASE=$(basename $TOPO | sed 's/.graphml//')

LOG_FILE="$PATH_TO_LOGS/$BASE-$SYN-$REQ_TYPE-$REQS-$FIXED-$RUN_ID.txt"

# added by yongzheng for ERROR as follows:
# cannot create logs/xxx-xxx.txt: Directory nonexistent
if [ ! -d "./${PATH_TO_LOGS}" ]; then
	mkdir -p $PATH_TO_LOGS
fi

echo "Running topology=$BASE syn_type=$SYN reqs_type=$REQ_TYPE num_reqs=$REQS fixed=$FIXED run-id=$RUN_ID"
echo "Command $SYNET_SCRIPT --topo=$TOPO --values=$VALUES --syn=$SYN --type=$REQ_TYPE --reqsize=$REQS --fixed=$FIXED"

START=$(date +%s)
stdbuf -oL $SYNET_SCRIPT --topo=$TOPO --values=$VALUES --syn=$SYN --type=$REQ_TYPE --reqsize=$REQS --fixed=$FIXED > $LOG_FILE 2>&1
END=$(date +%s)

TIME=$((END-START))
echo "Total time: $TIME" >> $LOG_FILE
