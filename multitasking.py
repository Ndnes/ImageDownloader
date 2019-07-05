"""Module for all activity implementing multitasking."""

# Built in modules
import os
import pathlib
import threading

# Installed modules
import cv2
import numpy as np
import requests

# User defined modules
import config


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
                        trdIndex):
    """Find number of valid links and save to global variables.

    Arguments:
        imageLinks {List} -- List of strings containing URLs
        numberOfValidLinks_t {List} -- Mutable object used for getting
        results of multithreading tasks.
        validLinks_t {List} -- Mutable object used for getting results of
        multithreading tasks.
        unvalidLinks_t {List} -- Mutable object used for getting results of
        multithreading tasks.
        trdIndex {int} -- Index describing which thread is executing
    """
    numberOfLinks = len(imageLinks)
    cnt = 0

    _numberOfValidLinks = 0
    _validLinks = []
    _unvalidLinks = []
    for link in imageLinks:
        try:
            r = requests.head(link, timeout=0.5)
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
        if trdName != 'MainThread':  # Needed to run function without mthread
            trdNum = int(trdName[-3:])
            if numberOfLinks == 0:
                config.g_progress[trdNum] = 1.0
            else:
                config.g_progress[trdNum] = cnt/numberOfLinks
    numberOfValidLinks_t[trdIndex] = _numberOfValidLinks
    validLinks_t[trdIndex] = _validLinks
    unvalidLinks_t[trdIndex] = _unvalidLinks


def divideWorkload(workItems, numberOfCpu):
    """Divide work into smaller tasks for multithreading.

    Arguments:
        workItems {List} -- List of items to be treated
        numberOfCpu {int} -- The number of logical cores available for
        multithreading
    Returns:
            List of int -- A list with the number of tasks per thread
    """
    tasksPerCpu = int(len(workItems) / numberOfCpu)
    workTasks = [tasksPerCpu] * numberOfCpu
    for i in range(len(workItems) % numberOfCpu):
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


def saveImages(directory, links, startCount, size=None, grayScale=False):
    """Save images and report progress to global variable.

    Arguments:
        directory {string} -- The directory where images will be saved
        links {List} -- List of string containing URL links for images.
        startCount {int} -- The startnumber used so that threads will not over-
        write each others files
    Keyword Arguments:
        size {List} -- [width, height] of image default: {None})
        grayScale {bool} -- Pass in true for grayscale image (default: {False})
    """
    if not os.path.exists(directory):
        os.mkdir(directory)
        cnt = 1
    else:
        cnt = startCount
    failCnt = 0
    progressCount = 0
    numberOfLinks = len(links)
    for link in links:
        imgPath = pathlib.Path(f'{directory}/{cnt}.png')
        try:
            r = requests.get(link, timeout=0.5)
        except Exception as e:
            failCnt += 1
            print(e)
        else:
            imgStr = r.content
            imgArr = np.fromstring(imgStr, np.uint8)
            if grayScale:  # TODO: Refactor move grayscale to separate func
                img = cv2.imdecode(imgArr, cv2.IMREAD_GRAYSCALE)
            else:
                img = cv2.imdecode(imgArr, cv2.IMREAD_COLOR)
            if size:  # TODO: Refactor move resizing to separate func
                img = cv2.resize(img, (size[0], size[1]))
            cv2.imwrite(imgPath, img)
            cnt += 1
        progressCount += 1
        trdName = threading.current_thread().name
        trdNum = int(trdName[-3:])  # Gets last 3 characters from threadname
        if numberOfLinks == 0:
            config.g_progress[trdNum] = 1
        else:
            config.g_progress[trdNum] = progressCount / numberOfLinks
