import queue
import logging

def init():
    """
    This function declares and initializes global attributes.

    Attributes:
        BUF_SIZE (int): Constant size of the queue.
        inputQueue (queue): Producer - consumer queue
        dataDictIndex (dictionary): Dictionary containing the name of each task
                                    as the keys and the index as the corresponding
                                    values.
    """

    logging.debug('Creating global variables')
    global BUF_SIZE
    BUF_SIZE = 5

    global inputQueue
    inputQueue = queue.Queue(BUF_SIZE)

    global dataDictIndex
    dataDictIndex = {}

def createDictIndex(dataDict):
    """
    Enumerates over each task's dictionary and fills in the dataDictIndex
    dictionary.
    :param dataDict: List of dictionaries containing each task.
    """

    for idx, i_task in enumerate(dataDict):
        dataDictIndex[i_task['task_name']] = idx