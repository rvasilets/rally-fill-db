#!/usr/bin/env bash

arr=(-h --help help)

if [[ " ${arr[@]} " =~ " $1 " ]]; then
    echo "Script runs rally task start. This is needed to fill Rally db and "
    echo "to test db stuff"
    echo "Required to install Rally at least before."
    echo
    echo "Arguments:"
    echo "--task-count <task_count>                   - Count of newly created tasks in db(optional)"
    echo "--task <task_file>                          - Path to Rally task file"
    echo "--deployments-count <task_file>             - Path to Rally task file(optional)"
    echo "--deployment <deployment_file>              - Path to Rally deployment file"
    echo "--type <type_of_filling>                    - Type of the way to fill Rally db."
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

DEPLOYMENTS_COUNT=10
TASKS_PER_DEPLOYMENT=10

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
        --type)
        TYPE="$2"
        shift
        ;;
        *)
                # unknown option
        ;;
    esac
    shift # past argument or value
done

case $type in
        1)
        for ((i=1;i<=DEPLOYMENTS_COUNT;i++)); do
            rally deployment create --filename $DEPLOYMENT --name filled+$i
            for ((j=1;j<=TASKS_PER_DEPLOYMENT;j++)); do
                rally task start --task $TASK
            done
        done
        ;;
        2)
        for ((i=1;i<=DEPLOYMENTS_COUNT;i++)); do
            rally deployment create --filename $DEPLOYMENT --name filled+$i
            TASKS_PER_DEPLOYMENT= expr $RANDOM % $TASKS_PER_DEPLOYMENT
            for ((j=1;j<=TASKS_PER_DEPLOYMENT;j++)); do
                FILE=$(ls ./samples/tasks/ | shuf -n 1)
                rally task start --task $FILE
            done
        done
        ;;
        *)
                # unknown option
        ;;
    esac

START=$(date +%s.%N)
for ((i=1;i<=DEPLOYMENTS_COUNT;i++)); do
    rally deployment destroy filled+$i
done
END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)
echo "It took $DIFF seconds."
