import psutil
import json
import logging

class sched_utilities:
    """This class contains utility functions for the scheduler."""

    def checkIfRunning(name):
        """
        This function checks if the process is currently running.

        :param name: Process name
        :return: Boolean value representing if the process is running.
        """

        logging.debug('Checking if process %s is currently running', name)
        for process in psutil.process_iter():
            try:
                if name in process.name():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def printWelcome(configFilePath):
        """
        This function creates a welcome message.

        :param configFilePath: String path to the config json file.
        :return: String containing the welcome message.
        """

        logging.debug('Printing welcome message')
        bracket = ''
        output = bracket.ljust(40, '*')
        output = output + '\n' + 'Welcome to Task Scheduler'
        configName = configFilePath
        configName = configName.rsplit('\\', 1)
        configName = configName[1]
        output = output + '\n' + 'Config loaded: ' + configName + \
                 '\n' + 'Commands:' + '\n' + 'start <task name>  -- Start the task\n' +\
                 'stop <task name>  -- Stop the task\n' + \
                 'status  -- Print the status of each task in the config file' + \
                 '\n' + bracket.ljust(40, '*')
        return output

    def parseConfig(filePath_in):
        """
        Read the config json file and parse the tasks to a dictionary.

        :param filePath_in: String containing the path to the config json file.
        :return: List of dictionaries containing each task.
        """

        logging.debug('Parsing config file:')
        with open(filePath_in) as conF:
            dataDict = json.load(conF)

        # Change the initial dict into a list of dicts (remove the top layer)
        dataDict = dataDict['task_config']
        for i_task in dataDict:
            logStr = "Name: {task_name} - Interval: {task_interval} - Scheduled Time: {task_scheduled_time} - "\
                     "Scheduled: {task_scheduled}\nLocation: {task_location}".format(**i_task)
            logging.debug(logStr)
            logging.debug('Finished parsing config file')
        return dataDict

    def printStatus(dataDict_in):
        """
        This function creates a status message containing the name and
        boolean status of each task.

        :param dataDict_in: List of dictionaries containing each task.
        :return: String containing status message.
        """
        name = 'Task Name'
        status = 'Status'
        underline = ''
        output = name.ljust(20, '-') + status.rjust(20, '-') + \
                 '\n' + underline.ljust(40, '-')
        for i_task in dataDict_in:
            name = i_task['task_name']
            status = i_task['task_scheduled']
            output = output + '\n' + name.ljust(20, '-') + status.rjust(20, '-')
        return output