import json
import os
import optparse
import subprocess
import sys
import time

def update_times(time):
    for f in os.listdir("./samples/tasks/"):
        task_file = os.path.join("./samples/tasks/", f)
        if os.path.isfile(task_file):
            with open(task_file) as fd:
                task_config = json.loads(fd.read()).values()[0][0]
                task_config["runner"]["times"] = time
                json.dumps(task_config, indent=4)

def round_robin_fill(task_file, deployment_file, deployments_count=10,
                     tasks_count=10):
    for i in range(deployments_count):
        create_deployment(deployment_file, i)
        for j in range(tasks_count):
            run_task(task_file)

def create_deployment(deployment_file, order):
    subprocess.call(["rally", "deployment", "create", "--task",
                      deployment_file, "--name", "filled%d" % order])

def run_task(task_file):
    subprocess.call(["rally", "task", "start", "--task", task_file])

def destroy_deployment(name):
    subprocess.call(["rally", "deployment", "destroy", name])

def destroy_all_deployments():
    for i in range(deployments_count):
        name = "filled%d" % i
        destroy_deployment(name)

def main():
    parser = optparse.OptionParser()
    parser.add_option("--task", dest="task_file",
                      help="path to the task file")
    parser.add_option("--deployment", dest="deployment_file",
                      help="path to the rally deployment file")
    parser.add_option("--deployments-count", dest="deployments_count", default=10,
                      help="number of created deployments")
    parser.add_option("--tasks-count", dest="tasks_count", default=10,
                      help="number of tasks per deployment.")
    parser.add_option("--type", dest="fill_type",
                      help="type of filling Rally db")
    parser.add_option("--times", dest="times",
                      help="number of iteration in tasks")


    (options, args) = parser.parse_args()

    task_file = options.task_file
    deployment_file = options.deployment_file
    deployments_count = options.deployments_count
    tasks_count = options.tasks_count

    update_times(options.times)
    if str(options.fill_type) == "1":
        round_robin_fill(task_file, deployment_file, deployments_count,
                         tasks_count)
    start = time.time()
    destroy_all_deployments()
    print "Deployment destroy takes %f seconds." % (time.time() - start)
    

if __name__ == "__main__":
    sys.exit(main())
    
