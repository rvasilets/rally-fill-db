Prepare Rally

  Update & source openrc file from this directory vi openrc source openrc
  Create rally deployment rally deployment create --fromenv --name testing


Running script

    python runner.py --task samples/tasks/dummy.json --deployment samples/deployments/rally_deployment.json --deployments-count 2 --type 1

Script creates <deployment_count> deployments with <task_count> per deployment tasks in you db.

