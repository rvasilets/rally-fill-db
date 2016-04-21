import json
import logging
import os
import optparse
import subprocess
import sys
import tempfile
import time

from rally import api
from rally import plugins


LOG = logging.getLogger("fill_rally_db")


def update_times(time, name):
    for f in os.listdir("samples/tasks/"):
        task_file = os.path.join("samples/tasks/", f)
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
            run_task(task_file, "filled%d" % i)

def progression_fill(task_file, deployment_file, deployment_count=1, diff=1,
                     st_cnt_tasks_per_deployment=1):
    for i in range(deployment_count):
        create_deployment(deployment_file, i)
        tasks_count = st_cnt_tasks_per_deployment + diff * i
        LOG.info("Started to run %d tasks" % tasks_count)
        for j in range(tasks_count):
            run_task(task_file)
    

def create_deployment(deployment_file, order):
    with open(deployment_file) as fd:
        deployment_cfg = json.loads(fd.read())
        LOG.info("Creating deployment filled%d" % order)
        api.Deployment.create(deployment_cfg, "filled%d" % order)
        LOG.info("Created deployment filled%d" % order)
        

def run_task(task_files_or_file, deployment):
    if isinstance(task_files_or_file, list):
        for f in task_files_or_file:
            with open(f) as fd:
                task_config = json.loads(fd.read())
                api.Task.start(deployment, task_config)
    else:
        with open(task_files_or_file) as fd:
                task_config = json.loads(fd.read())
                api.Task.start(deployment, task_config)

def destroy_deployment(name):
    st = time.time()
    LOG.info("Started to destroy %s deployment.")
    api.Deployment.destroy(name)
    en = time.time()
    LOG.info("Deployment %s destroy takes %f seconds." % (name, (en - st)))

def destroy_all_deployments(deployments_count):
    for i in range(deployments_count):
        name = "filled%d" % i
        destroy_deployment(name)

def main():
    plugins.load()
    parser = optparse.OptionParser()
    parser.add_option("--task", dest="task_file",
                      help="path to the task file")
    parser.add_option("--deployment", dest="deployment_file",
                      help="path to the rally deployment file")
    parser.add_option("--deployments-count", dest="deployments_count", default=1,
                      help="number of created deployments", type="int")
    parser.add_option("--tasks-count", dest="tasks_count", default=1,
                      help=("number of tasks per deployment. For progression "
                            "fill this is the base of progression."), type="int")
    parser.add_option("--type", dest="fill_type", type="int",
                      help="type of filling Rally db")
    parser.add_option("--times", dest="times", type="int", default=1,
                      help="number of iteration in tasks")
    parser.add_option("--diff", dest="progression_diff", type="int", default=1,
                      help="difference use in progression fill.")
    parser.add_option("--destroy", dest="destroy", type="int", default=1,
                      help=("bigger then 0 - if need to destroy, "
                            "0 - if not needed."))

    fh = logging.FileHandler("fill_db.log")
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)
    fh.setLevel(logging.DEBUG)
    LOG.addHandler(fh)

    (options, args) = parser.parse_args()

    task_file = options.task_file
    deployment_file = options.deployment_file
    deployments_count = options.deployments_count
    tasks_count = options.tasks_count
    progression_difference = options.progression_diff
    destroy = options.destroy

    if hasattr(options, "times"):
        task_file = update_times(options.times, task_file)
    if str(options.fill_type) == "1":
        round_robin_fill(task_file, deployment_file, deployments_count,
                         tasks_count)
    elif str(options.fill_type) == "2":
        progression_fill(task_file, deployment_file, deployments_count,
                         progression_difference, tasks_count)
    if destroy:
        start = time.time()
        destroy_all_deployments(deployments_count)
        LOG.info("Deployment destroy takes %f seconds." % (time.time() - start))
        print "Deployment destroy takes %f seconds." % (time.time() - start)
    

if __name__ == "__main__":
    sys.exit(main())
    
