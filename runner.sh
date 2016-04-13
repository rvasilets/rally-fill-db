#!/usr/bin/env bash

arr=(-h --help help)

if [[ " ${arr[@]} " =~ " $1 " ]]; then
    echo "Script runs rally task start. This is needed to fill Rally db and "
    echo "to test db stuff"
    echo "Required to install Rally at least before."
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
        --tasks-count)
        TASKS_PER_DEPLOYMENT="$2"
        shift # past argument
        ;;
        --deployments-count)
        DEPLOYMENTS_COUNT="$2"
        shift # past argument
        ;;
        --deployment)
        DEPLOYMENT="$2"
        shift # past argument
        ;;
        *)
                # unknown option
        ;;
    esac
    shift # past argument or value
done
for ((i=1;i<=DEPLOYMENT_COUNT;i++)); do
    rally deployment create --filename $DEPLOYMENT --name filled+$i
    for ((j=1;j<=TASKS_PER_DEPLOYMENT;j++)); do
        rally task start --task $TASK
    done
done
