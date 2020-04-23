import threading
import comVar
import logging


def checkInput(line_in):
    """Returns the index of the specific task."""

    return comVar.dataDictIndex.get(line_in, -1)

def analyzeInput(line):
    """
    This function error checks the entered command and puts the command
    into the queue.

    This function determines if the command entered is start, stop, or
    status. If the command is start or stop, then the task name is checked
    against the tasks in the config json file. If the command contains
    no errors, then the command is put into the producer-consumer queue.

    :param line: Command entered into the console.
    """

    logging.info('Analyzing input: %s', line)
    lineSpt = line.split(' ', 1)
    lineSpt[0] = lineSpt[0].lower()
    if "start" in lineSpt[0] or "stop" in lineSpt[0]:
        lineSpt[1] = lineSpt[1].rstrip()
        resultOfCheck = checkInput(lineSpt[1])
        if resultOfCheck == -1:
            logging.error('Task %s not found in config', lineSpt[1])
            print("Task named:'" + lineSpt[1] + "' not found in config")
        else:
            tup = (lineSpt[0], resultOfCheck)
            logging.info('Sending command to consumer')
            comVar.inputQueue.put(tup)

    elif "status" in lineSpt[0]:
        tup = (lineSpt[0],)
        logging.info('Sending status command to consumer')
        comVar.inputQueue.put(tup)

    else:
        logging.error('Invalid command entered')
        print("Invalid Command Entered. Valid commands: \nstart  stop  status")


class InputThread(threading.Thread):
    """This class is for monitoring for possible input."""

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        """Constructor function for the InputThread class."""

        super(InputThread, self).__init__()
        self.target = target
        self.name = name

    def run(self):
        """This function continuously loops checking for an entered command."""

        logging.debug('Starting input thread')
        #for line in sys.stdin:
            #analyzeInput(line)
        while True:
            line = input(">")
            analyzeInput(line)
