import sched_utilities
import os
import time
import input
import comVar
from schedule_ops import schedule_ops
import datetime

class TestClass:
    """Class containing unit tests for scheduler."""

    def test_welcome(self):
        """Test to see if the welcome message is correct."""

        expectedOutput = '****************************************\nWelcome to Task Scheduler\n' \
                         'Config loaded: config3.json\nCommands:\nstart <task name>  -- Start the task' \
                         '\nstop <task name>  -- Stop the task\nstatus  -- Print the status ' \
                         'of each task in the config file\n****************************************'
        configPath = 'C:\\Users\\Jonathan\\PycharmProjects\\proj1Omitron\\config3.json'
        assert sched_utilities.sched_utilities.printWelcome(configPath) == expectedOutput

    def test_parseConfig(self):
        """Test to confirm the config file is properly parsed."""

        configPath = 'C:\\Users\\Jonathan\\PycharmProjects\\proj1Omitron\\config3.json'
        dict0 = {'task_name':'Scheduled Task',
                 'task_location':'C:\\Users\\Jonathan\\PycharmProjects\\proj1Omitron\\dist\\WaitProgram10.exe',
                 'task_interval': 30,
                 'task_scheduled_time':'03/18/2020 21:12:00 EST',
                 'task_scheduled': 'true'}
        dict1 = {'task_name': 'Important Task',
                 'task_location': 'C:\\Users\\Jonathan\\PycharmProjects\\proj1Omitron\\dist\\WaitProgram10.exe',
                 'task_interval': 7,
                 'task_scheduled_time': '',
                 'task_scheduled': 'true'}
        dict2 = {'task_name': 'Test Task',
                 'task_location': 'C:\\Users\\Jonathan\\PycharmProjects\\proj1Omitron\\dist\\WaitProgram30.exe',
                 'task_interval': 65,
                 'task_scheduled_time': '',
                 'task_scheduled': 'false'}
        dict3 = {'task_name': 'Task1',
                 'task_location': 'C:\\Users\\Jonathan\\PycharmProjects\\proj1Omitron\\dist\\WaitProgram60.exe',
                 'task_interval': 0,
                 'task_scheduled_time': '',
                 'task_scheduled': 'false'}
        expectedOutput = [dict0, dict1, dict2, dict3]
        assert sched_utilities.sched_utilities.parseConfig(configPath) == expectedOutput

    def test_statusUpdate(self):
        """Test to confirm the status message is correct."""

        dict0 = {'task_name': 'Scheduled Task',
                 'task_location': 'C:\\Users\\Jonathan\\PycharmProjects\\proj1Omitron\\dist\\WaitProgram10.exe',
                 'task_interval': 30,
                 'task_scheduled_time': '03/18/2020 21:12:00 EST',
                 'task_scheduled': 'true'}
        dict1 = {'task_name': 'Important Task',
                 'task_location': 'C:\\Users\\Jonathan\\PycharmProjects\\proj1Omitron\\dist\\WaitProgram10.exe',
                 'task_interval': 7,
                 'task_scheduled_time': '',
                 'task_scheduled': 'true'}
        dict2 = {'task_name': 'Test Task',
                 'task_location': 'C:\\Users\\Jonathan\\PycharmProjects\\proj1Omitron\\dist\\WaitProgram30.exe',
                 'task_interval': 65,
                 'task_scheduled_time': '',
                 'task_scheduled': 'false'}
        dict3 = {'task_name': 'Task1',
                 'task_location': 'C:\\Users\\Jonathan\\PycharmProjects\\proj1Omitron\\dist\\WaitProgram60.exe',
                 'task_interval': 0,
                 'task_scheduled_time': '',
                 'task_scheduled': 'false'}
        input = [dict0, dict1, dict2, dict3]

        expectedOutput = 'Task Name-------------------------Status\n' + \
                         '----------------------------------------\n' +\
                         'Scheduled Task----------------------true\n' +\
                         'Important Task----------------------true\n' +\
                         'Test Task--------------------------false\n' +\
                         'Task1------------------------------false'
        assert sched_utilities.sched_utilities.printStatus(input) == expectedOutput

    def test_checkIfRunning(self):
        """Test to confirm that a running process can be detected."""

       # taskPath = 'C:\Users\Jonathan\PycharmProjects\proj1Omitron\dist\WaitProgram10.exe'
        taskPathabs = os.path.abspath(r'C:\Users\Jonathan\PycharmProjects\proj1Omitron\dist\WaitProgram10.exe')
        runCommand = "start cmd /c " + taskPathabs
        os.system(runCommand)
        time.sleep(2)
        assert sched_utilities.sched_utilities.checkIfRunning('WaitProgram10.exe') == True

    def test_analyzeInput(self):
        """
        Test to confirm that start, stop, and status commands can be
        correctly analyzed and checked for errors.
        """

        comVar.init()
        dict0 = {'task_name': 'Scheduled Task',
                 'task_location': 'C:\\Users\\Jonathan\\PycharmProjects\\proj1Omitron\\dist\\WaitProgram10.exe',
                 'task_interval': 30,
                 'task_scheduled_time': '03/18/2020 21:12:00 EST',
                 'task_scheduled': 'true'}
        dict1 = {'task_name': 'Important Task',
                 'task_location': 'C:\\Users\\Jonathan\\PycharmProjects\\proj1Omitron\\dist\\WaitProgram10.exe',
                 'task_interval': 7,
                 'task_scheduled_time': '',
                 'task_scheduled': 'true'}
        dict2 = {'task_name': 'Test Task',
                 'task_location': 'C:\\Users\\Jonathan\\PycharmProjects\\proj1Omitron\\dist\\WaitProgram30.exe',
                 'task_interval': 65,
                 'task_scheduled_time': '',
                 'task_scheduled': 'false'}
        dict3 = {'task_name': 'Task1',
                 'task_location': 'C:\\Users\\Jonathan\\PycharmProjects\\proj1Omitron\\dist\\WaitProgram60.exe',
                 'task_interval': 0,
                 'task_scheduled_time': '',
                 'task_scheduled': 'false'}
        inputDict = [dict0, dict1, dict2, dict3]
        comVar.createDictIndex(inputDict)
        input.analyzeInput('start Test Task\n')
        if not comVar.inputQueue.empty():
            thisInput = comVar.inputQueue.get()
            assert thisInput[0] == 'start'
            assert thisInput[1] == 2

        input.analyzeInput('stop Important Task\n')
        if not comVar.inputQueue.empty():
            thisInput = comVar.inputQueue.get()
            assert thisInput[0] == 'stop'
            assert thisInput[1] == 1

        input.analyzeInput('start notATask\n')
        assert comVar.inputQueue.empty() == True

    def test_consumerReceieve(self):
        """
        Test to confirm that commands can be correctly received in
        the queue. Test to confirm that the start and stop commands
        correctly schedule / remove the task.
        """

        comVar.init()
        dict0 = {'task_name': 'Scheduled Task',
                 'task_location': 'C:\\Users\\Jonathan\\PycharmProjects\\proj1Omitron\\dist\\WaitProgram10.exe',
                 'task_interval': 30,
                 'task_scheduled_time': '03/18/2020 21:12:00 EST',
                 'task_scheduled': 'true'}
        dict1 = {'task_name': 'Important Task',
                 'task_location': 'C:\\Users\\Jonathan\\PycharmProjects\\proj1Omitron\\dist\\WaitProgram10.exe',
                 'task_interval': 7,
                 'task_scheduled_time': '',
                 'task_scheduled': 'true'}
        dict2 = {'task_name': 'Test Task',
                 'task_location': 'C:\\Users\\Jonathan\\PycharmProjects\\proj1Omitron\\dist\\WaitProgram30.exe',
                 'task_interval': 65,
                 'task_scheduled_time': '',
                 'task_scheduled': 'false'}
        dict3 = {'task_name': 'Task1',
                 'task_location': 'C:\\Users\\Jonathan\\PycharmProjects\\proj1Omitron\\dist\\WaitProgram60.exe',
                 'task_interval': 0,
                 'task_scheduled_time': '',
                 'task_scheduled': 'false'}
        inputDict = [dict0, dict1, dict2, dict3]
        sched = schedule_ops(inputDict)
        tup = ('start', 0)
        comVar.inputQueue.put(tup)
        sched.receiveInput()
        jobs = sched.schedule.jobs
        expectedTime = datetime.time(hour=21, minute=12, second=0)
        assert jobs[0].at_time == expectedTime
        assert jobs[0].job_func.args[0] == dict0

        tup = ('stop', 0)
        comVar.inputQueue.put(tup)
        sched.receiveInput()
        jobs = sched.schedule.jobs
        assert jobs.__len__() == 0