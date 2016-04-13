#!/usr/bin/env bash

arr=(-h --help help)

if [[ " ${arr[@]} " =~ " $1 " ]]; then
    echo "Script runs in parallel rally verify and rally task"
    echo "This is required to run functional testing during the load"
    echo
    echo "Arguments:"
    echo "--task-count <task_count>      - Count of newly created tasks in db"
    echo "--task <task_file>        - Path to Rally task file"
    exit 0
fi

# Argument parsing was copied from here:
# http://stackoverflow.com/questions/192249/how-do-i-parse-command-line-arguments-in-bash/14203146#14203146
# Big thanks Bruno Bronosky!

# Use > 1 to consume two arguments per pass in the loop (e.g. each
# argument has a corresponding value to go with it).
# Use > 0 to consume one or more arguments per pass in the loop (e.g.
# some arguments don't have a corresponding value to go with it such
# as in the --default example).
# note: if this is set to > 0 the /etc/hosts part is not recognized ( may be a bug )

while [[ $# > 1 ]]
do
    key="$1"

    case $key in
        --task)
        TASK="$2"
        shift # past argument
        ;;
        --task-count)
        TASK_COUNT="$2"
        shift # past argument
        ;;
        *)
                # unknown option
        ;;
    esac
    shift # past argument or value
done
for ((i=1;i<=TASK_COUNT;i++)); do
    rally task start --task $TASK
done
