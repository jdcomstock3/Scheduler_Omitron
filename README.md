# Scheduler_Omitron
Candidate for Software Devoloper Position Code Challange

"""Scheduler Driver Script

This script runs a task scheduler. Each task can be run at a specific time and/or run at a specific interval.

This script accepts json (.json) files. Each task must contain the following:
 task_name - Case sensitive string
 task_location  -   String containing a path to an executable to be run
 task_interval  -   Amount of time (in seconds) between executions of the task
                    A value of 0 = run the task once
 task_scheduled_time    -   String specifying the time to run the task
                            Empty string = run at interval (if value is not 0)
                            If interval is equal to 0, only run task once
 task_scheduled -   String containing either True or False
                    True = Enable task to be scheduled / run
                    False = Disable task

 The config file should follow this template:

config.json
{
     "task_config": [{
                "task_name": "Scheduled Task",
                "task_location": "C:\\Users\\myuser\\scheduled_task.exe",
                "task_interval": 5,
                "task_scheduled_time": "03/16/2020 04:00:00 EST",
                "task_scheduled": "true"
           },
           {
                "task_name": "Important Task",
                "task_location": "C:\\Users\\myuser\\important_task.exe",
                "task_interval": 0,
                "task_scheduled_time": "",
                "task_scheduled": "false"
           }
     ]
}

Run parameters:
    -f <config file name>

Execution commands:
    start <task name>   - Enable a task to be scheduled / executed
    stop <task name>    - Disable a task
    status  - Returns the current status of each task

This script requires that 'psutil' and 'schedule' be installed within the Python
environment you are running this script in.

Developed and tested on python 3.8

Written by: Jonathan D. Comstock
"""
