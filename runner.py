import json
import os
import optparse
import subprocess
import sys
import tempfile
import time

def update_times(time, name):
    for f in os.listdir("samples/tasks/"):
        task_file = os.path.join("samples/tasks/", f)
        print name, task_file
        if os.path.isfile(task_file) and task_file == name:
            with open(task_file) as fd:
                task_config = json.loads(fd.read())
                task_config.values()[0][0]["runner"]["times"] = time
                tf = tempfile.NamedTemporaryFile(delete=False)
                tf.write(json.dumps(task_config, indent=4))
                return tf.name

def round_robin_fill(task_file, deployment_file, deployments_count=1,
                     tasks_count=1):
    for i in range(deployments_count):
        create_deployment(deployment_file, i)
        for j in range(tasks_count):
            run_task(task_file)

def create_deployment(deployment_file, order):
    subprocess.call(["rally", "deployment", "create", "--filename",
                      deployment_file, "--name", "filled%d" % order])

def run_task(task_file):
    subprocess.call(["rally", "task", "start", task_file])

def destroy_deployment(name):
    subprocess.call(["rally", "deployment", "destroy", name])

def destroy_all_deployments(deployments_count):
    for i in range(deployments_count):
        name = "filled%d" % i
        destroy_deployment(name)

def main():
    parser = optparse.OptionParser()
    parser.add_option("--task", dest="task_file",
                      help="path to the task file")
    parser.add_option("--deployment", dest="deployment_file",
                      help="path to the rally deployment file")
    parser.add_option("--deployments-count", dest="deployments_count", default=1,
                      help="number of created deployments", type="int")
    parser.add_option("--tasks-count", dest="tasks_count", default=1,
                      help="number of tasks per deployment.", type="int")
    parser.add_option("--type", dest="fill_type", type="int",
                      help="type of filling Rally db")
    parser.add_option("--times", dest="times", type="int", default=1,
                      help="number of iteration in tasks")


    (options, args) = parser.parse_args()

    task_file = options.task_file
    deployment_file = options.deployment_file
    deployments_count = options.deployments_count
    tasks_count = options.tasks_count

    task_file = update_times(options.times, task_file)
    print task_file
    if str(options.fill_type) == "1":
        round_robin_fill(task_file, deployment_file, deployments_count,
                         tasks_count)
    subprocess.call(["rally", "deployment", "list"])
    start = time.time()
    destroy_all_deployments(deployments_count)
    subprocess.call(["rally", "deployment", "list"])
    print "Deployment destroy takes %f seconds." % (time.time() - start)
    

if __name__ == "__main__":
    sys.exit(main())
    
