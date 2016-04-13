Prepare Rally

  Update & source openrc file from this directory vi openrc source openrc
  Create rally deployment rally deployment create --fromenv --name testing


Running script

  . runner.sh --task <task_file> --count <tasks_count>

Script creates <task_count> tasks in you db.

