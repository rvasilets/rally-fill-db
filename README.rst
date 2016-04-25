Prepare Rally

  Update & source openrc file from this directory vi openrc source openrc
  Create rally deployment rally deployment create --fromenv --name testing


Running script

    python runner.py --task <task_cfg> --deployment <deployment_cfg> --deployments-count <deployment_count> --type <type_of_fill> --times <iteration_count>

Script creates <deployment_count> deployments with <task_count> per deployment tasks in you db.

For more details how to run print `$python runner.py -h`
Usage: runner.py [options]

Options:
  -h, --help            show this help message and exit
  --task=TASK_FILE      [REQUIRED] path to the task file
  --deployment=DEPLOYMENT_FILE
                        [REQUIRED] path to the rally deployment file
  --deployments-count=DEPLOYMENTS_COUNT
                        [OPTIONAL] number of created deployments. By default
                        1.
  --tasks-count=TASKS_COUNT
                        [OPTIONAL] number of tasks per deployment. For
                        progression fill this is the base of progression. By
                        default 1.
  --type=FILL_TYPE      type of filling Rally db
  --times=TIMES         [OPTIONAL] number of iteration in tasks.
  --diff=PROGRESSION_DIFF
                        difference use in progression fill. When --type=2. By
                        default 1.
  --destroy=DESTROY     bigger then 0 - if need to destroy, 0 - if not needed.
                        By default it destroy.
  --use-fill=USE_FILL   bigger then 0 - if need to fill db, 0 - if not needed.
                        By default it fills.

Or contact me - rvasilets@mirantis.com
