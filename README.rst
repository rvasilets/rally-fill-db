Prepare Rally

  Update & source openrc file from this directory vi openrc source openrc
  Create rally deployment rally deployment create --fromenv --name testing


Running script

  . runner.sh --task <task_file> --tasks-count <tasks_count> --deployment <deployment_file> --deployments-count <deployment_count>

Script creates <deployment_count> deployments with <task_count> per deployment tasks in you db.

