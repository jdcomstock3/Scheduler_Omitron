
import schedule
import comVar
from sched_utilities import sched_utilities
import os
import time
import logging

def runOnce(task_dict):
    """
    Run the task once and return the schedule with the task canceled.

    This function brings in the task's dictionary, finds the path to the
    executable and attempts to run it. Before running the executable,
    there is a check performed to see if the executable is already
    running. If the executable is already running, an error is recorded
    in the log and the executable will not be run.

    :param task_dict: Dictionary with the task's information
    :return: Return a schedule with the task canceled, or nothing if an
             error has occurred
    """
    logging.debug('Attempting to run task %s', task_dict["task_name"])
    taskPath = task_dict['task_location']
    name = taskPath.rsplit('\\', 1)
    name = name[-1]
    if not sched_utilities.checkIfRunning(name):
        logging.info('Running task %s', task_dict["task_name"])
        taskPathabs = os.path.abspath(taskPath)
        runCommand = "start cmd /c " + taskPathabs
        os.system(runCommand)
        return schedule.CancelJob
    else:
        logging.error('Task %s could not be run. Program %s is already running', task_dict["task_name"], name)

def runInterval(task_dict):
    """
    Run the task if it is not already running.

    This function brings in the task's dictionary, finds the path to the
    executable and attempts to run it. Before running the executable,
    there is a check performed to see if the executable is already
    running. If the executable is already running, an error is recorded
    in the log and the executable will not be run.

    :param task_dict: Dictionary with the task's information

    """
    logging.debug('Attempting to run task %s', task_dict["task_name"])
    taskPath = task_dict['task_location']
    name = taskPath.rsplit('\\', 1)
    name = name[-1]
    if not sched_utilities.checkIfRunning(name):
        logging.info('Running task %s', task_dict["task_name"])
        taskPathabs = os.path.abspath(taskPath)
        runCommand = "start cmd /c " + taskPathabs
        os.system(runCommand)
    else:
        logging.error('Task %s could not be run. Program %s is already running', task_dict["task_name"], name)

class schedule_ops:
    """
    This is a class for handling the scheduling of tasks.

    Attributes:
        dataDict (dictionary): Dictionary containing information on each task.
        schedule (schedule): Schedule that contains when each task should be run.
    """

    def __init__(self, dataDict):
        """
        The constructor for the schedule_ops class.

        :param dataDict: Dictionary containing information on each task.
        """
        self.dataDict = dataDict
        self.schedule = schedule.default_scheduler

    def runSpecificTime_andInterval(self, task_dict):
        """
        Schedule this task to happen at the appropriate interval, then run the task.

        When a task is defined to run at a specific time and at an interval,
        this function will be run at the specific time. This function will
        schedule the task to be run at the correct interval and then run
        the task now. The function will return a schedule with the specific
        time part being canceled.

        :param task_dict: Dictionary with the task's information.
        :return: Return a schedule with the task canceled, or nothing if an
                 error has occurred.
        """
        # first schedule this job to happen again at the specified interval
        taskInterval = task_dict['task_interval']
        self.schedule.every(taskInterval).seconds.do(runInterval, task_dict).tag(task_dict['task_name'])
        # now run the job once
        return runOnce(task_dict)

    def scheduleInitialTask(self, dataDict_in):
        """
        Schedule the tasks that are set to true.

        This function can be called at the beginning of the schedule program
        or when a start command has been entered. Each inputted task is checked
        for a true value, a specific run time, and for an interval run time.
        The appropriate scheduling occurs for each task. If a task has a
        true value with no specific time or interval time, the task is run
        right away.

        :param dataDict_in: Dictionary containing information on each task or
                            a singular task.
        """
        # Schedule all the tasks that have a task_scheduled value of true in the config json file
        # For each task in the config file, check if should be scheduled right away
        for i_task in dataDict_in:
            if i_task['task_scheduled'] == 'true':
                logging.debug('Scheduling task %s')
                thisTaskTime = i_task['task_scheduled_time']
                if "/" in thisTaskTime:
                    # task_scheduled_time contains an exact start time
                    #### Strip down to only the time part
                    thisTaskTime = thisTaskTime.split()
                    thisTaskTime = thisTaskTime[1]
                    thisInterval = i_task['task_interval']
                    if thisInterval == 0:
                        # Schedule this task to only be run once
                        logging.debug('Task scheduled for specific time')
                        self.schedule.every().day.at(thisTaskTime).do(runOnce, i_task).tag(i_task['task_name'])
                    else:
                        logging.debug('Task scheduled for specific time and inveral')
                        self.schedule.every().day.at(thisTaskTime).do(self.runSpecificTime_andInterval, i_task).tag(
                            i_task['task_name'])
                else:
                    # Task does not have a specific time to start
                    # Check for interval time
                    thisInterval = i_task['task_interval']
                    if thisInterval != 0:
                        logging.debug('Scheduling task for interval %d', thisInterval)
                        # schedule this task to run at every interval
                        self.schedule.every(thisInterval).seconds.do(runInterval, i_task).tag(i_task['task_name'])
                        runOnce(i_task)
                    else:
                        # run immediately
                        runOnce(i_task)

    def scheduleNewTask(self, taskDict):
        """
        Schedule a task when a start command has been entered.

        This function creates a list containing 1 dictionary of a task.
        The scheduleInitialTask function is then called to do the actual
        scheduling procedure.

        :param taskDict: Dictionary with the task's information.
        """
        # if isinstance(taskDict, list):
        # taskDict = taskDict[0]
        logging.info('Scheduling new task: %s', taskDict["task_name"])
        taskDict['task_scheduled'] = 'true'
        thisList = list((taskDict,))
        self.scheduleInitialTask(thisList)
        return taskDict

    def receiveInput(self):
        """
        This function removes the command from the queue and performs the
        correct operation.

        This function removes the tuple from the queue. Then it determines
        if the command is start, stop, or status. If the command is start
        or stop, then the index number of the task is determined and
        the appropriate scheduling function is called. If the command
        is status then the print status function is called.
        """
        thisInput = comVar.inputQueue.get()
        thisCom = thisInput[0]

        if "start" in thisCom:
            thisIdx = thisInput[1]
            logging.debug('Received start command for task #%d', thisIdx)
            self.dataDict[thisIdx] = self.scheduleNewTask(self.dataDict[thisIdx])
        elif "stop" in thisCom:
            thisIdx = thisInput[1]
            logging.debug('Received stop command for task #%d', thisIdx)
            thisDict = self.dataDict[thisIdx]
            logging.info('Stopping task %s', thisDict["task_name"])
            self.schedule.clear(thisDict["task_name"])
            #thisDict["task_scheduled"] = "false"
            self.dataDict[thisIdx]["task_scheduled"] = "false"
        elif "status" in thisCom:
            logging.debug('Received status command')
            print(sched_utilities.printStatus(self.dataDict))

    def mainRunner(self):
        """Looping function that checks for new input and pending tasks."""

        logging.debug('Beginning main schedule loop')
        while True:
            try:
                if not comVar.inputQueue.empty():
                    logging.debug('Consumer received a command')
                    self.receiveInput()

                self.schedule.run_pending()
            finally:
                time.sleep(1)