Prepare Rally

  Update & source openrc file from this directory vi openrc source openrc
  Create rally deployment rally deployment create --fromenv --name testing


Running script

    python runner.py --task <task_cfg> --deployment <deployment_cfg> --deployments-count <deployment_count> --type <type_of_fill> --times <iteration_count>

Script creates <deployment_count> deployments with <task_count> per deployment tasks in you db.

