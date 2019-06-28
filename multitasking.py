"""Module for all activity implementing multitasking."""

import requests
import threading
import os

import globals


class WorkTask:
    """Store tasks that will be assigned to logical processors."""

    def __init__(self):
        """Initialize instance of WorkTask."""
        self.cpuNumber = 1
        self.startCount = None
        self.endCount = None
        self.workList = None


def findNumberOfValidLinks(
                        imageLinks,
                        numberOfValidLinks_t,
                        validLinks_t,
                        unvalidLinks_t,
                        index):
    """Find number of valid links and save to global variables.

    Arguments:
        imageLinks {List} -- List of strings containing URLs
        numberOfValidLinks_t {List} -- Immutable object used for getting
        results of multithreading tasks.
        validLinks_t {List} -- Immutable object used for getting results of
        multithreading tasks.
        unvalidLinks_t {[type]} -- Immutable object used for getting results of
        multithreading tasks.
        index {[type]} -- [description]
    """
    numberOfLinks = len(imageLinks)
    cnt = 0
    globals.g_progress

    _numberOfValidLinks = 0
    _validLinks = []
    _unvalidLinks = []
    for link in imageLinks:
        try:
            r = requests.head(link, timeout=0.2)
            if(r.ok):
                _numberOfValidLinks += 1
                _validLinks.append(link)
            else:
                unvalidLink = f'{link} [Status_code: {r.Status_code}]'
                _unvalidLinks.append(unvalidLink)
        except Exception as e:
            print(e)
        cnt += 1
        trdName = threading.current_thread().name
        trdNum = int(trdName[-3:])
        if numberOfLinks == 0:
            globals.g_progress[trdNum] = 1.0
        else:
            globals.g_progress[trdNum] = cnt/numberOfLinks
    numberOfValidLinks_t[index] = _numberOfValidLinks
    validLinks_t[index] = _validLinks
    unvalidLinks_t[index] = _unvalidLinks


def divideWorkload(workItems, numberOfCpu):
    """Divide work into smaller tasks for multithreading.

    Arguments:
        workItems {List} -- List of items to be treated
        numberOfCpu {int} -- The number of logical cores available for
        multithreading
    Returns:
            [type] -- [description]
    """
    tasksPerCpu = int(workItems / numberOfCpu)
    workTasks = [tasksPerCpu] * numberOfCpu
    for i in range(workItems % numberOfCpu):
        workTasks[i] += 1
    return workTasks


def assignWorkTasks(workTasks, links, directory):
    """Assign work tasks by instantianting WorkTask class.

    Arguments:
        workTasks {List} -- List int with the number of tasks per thread
        links {List} -- List of string with objects to be treated
        directory {string} -- The path where workobjects will be saved
    Returns:
        List -- List of WorkTask instances
    """
    output = []
    if not os.path.exists(directory):
        os.makedirs(directory)
        count = 1
    else:
        count = len(os.listdir(directory))

    i = 0
    initialCount = count
    for items in workTasks:
        if items != 0:
            workList = links[count-initialCount:count-initialCount+items]
            w = WorkTask()
            w.cpuNumber = i
            w.startCount = count
            w.workList = workList
            output.append(w)
            count += items
        i += 1
    return output
