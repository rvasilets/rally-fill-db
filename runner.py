import json
import logging
import os
import optparse
import re
import sys
import tempfile
import time

from rally import api
from rally import exceptions
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
        LOG.warn("Started to run %d tasks" % tasks_count)
        for j in range(tasks_count):
            run_task(task_file, "filled%d" % i)
    

def create_deployment(deployment_file, order):
    with open(deployment_file) as fd:
        deployment_cfg = json.loads(fd.read())
        LOG.warn("Creating deployment filled%d" % order)
        try:
            # TODO use random name for deployment!!!
            api.Deployment.create(deployment_cfg, "filled%d" % order)
        except exceptions.DeploymentNameExists as e:
            LOG.warn(e)
        LOG.warn("Created deployment filled%d" % order)
        

def run_task(task_files_or_file, deployment):
    if isinstance(task_files_or_file, list):
        for f in task_files_or_file:
            with open(f) as fd:
                task_config = json.loads(fd.read())
                api.Task.start(deployment, task_config)
    else:
        with open(task_files_or_file) as fd:
            task_config = json.loads(fd.read())
            LOG.warn("Started task with config %s" % task_config)
            api.Task.start(deployment, task_config)
            LOG.warn("Finished task with config %s" % task_config)

def destroy_deployment(name):
    st = time.time()
    LOG.warn("Started to destroy %s deployment." % name)
    api.Deployment.destroy(name)
    en = time.time()
    LOG.warn("Deployment %s destroy takes %f seconds." % (name, (en - st)))

def destroy_all_deployments(deployments_count):
    for i in range(deployments_count):
        name = "filled%d" % i
        destroy_deployment(name)

def checkRequiredArguments(opts, parser):
    missing_options = []
    for option in parser.option_list:
        if re.match(r'^\[REQUIRED\]', option.help) and eval('opts.' + option.dest) == None:
            missing_options.extend(option._long_opts)
    if len(missing_options) > 0:
        parser.error('Missing REQUIRED parameters: ' + str(missing_options))

def main():
    plugins.load()
    parser = optparse.OptionParser()
    parser.add_option("--task", dest="task_file",
                      help="[REQUIRED] path to the task file")
    parser.add_option("--deployment", dest="deployment_file",
                      help="[REQUIRED] path to the rally deployment file")
    parser.add_option("--deployments-count", dest="deployments_count", default=1,
                      help="number of created deployments", type="int")
    parser.add_option("--tasks-count", dest="tasks_count", default=1,
                      help=("number of tasks per deployment. For progression "
                            "fill this is the base of progression."), type="int")
    parser.add_option("--type", dest="fill_type", type="int",
                      help="type of filling Rally db")
    parser.add_option("--times", dest="times", type="int",
                      help="number of iteration in tasks")
    parser.add_option("--diff", dest="progression_diff", type="int", default=1,
                      help="difference use in progression fill.")
    parser.add_option("--destroy", dest="destroy", type="int", default=1,
                      help=("bigger then 0 - if need to destroy, "
                            "0 - if not needed."))
    parser.add_option("--use-fill", dest="use_fill", type="int", default=1,
                      help=("bigger then 0 - if need to fill db, "
                            "0 - if not needed."))

    fh = logging.FileHandler("fill_db.log")
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)
    fh.setLevel(logging.NOTSET)
    LOG.addHandler(fh)

    (options, args) = parser.parse_args()
    checkRequiredArguments(options, parser)

    task_file = options.task_file
    deployment_file = options.deployment_file
    deployments_count = options.deployments_count
    tasks_count = options.tasks_count
    progression_difference = options.progression_diff
    use_fill = options.use_fill
    destroy = options.destroy

    if options.times is not None:
        task_file = update_times(options.times, task_file)
    if not (use_fill or destroy):
        parser.error("You must specify at least one of the options --destroy or --use-fill")  
    if use_fill:
        if options.fill_type is None:
            parser.error("fill_type should be specified if u use --use-fill argument")
        if str(options.fill_type) == "1":
            round_robin_fill(task_file, deployment_file, deployments_count,
                             tasks_count)
        elif str(options.fill_type) == "2":
            progression_fill(task_file, deployment_file, deployments_count,
                             progression_difference, tasks_count)
    if destroy:
        start = time.time()
        destroy_all_deployments(deployments_count)
        LOG.warn("Deployment destroy takes %f seconds." % (time.time() - start))
    

if __name__ == "__main__":
    sys.exit(main())
    
