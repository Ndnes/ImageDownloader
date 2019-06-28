"""Module for all activity implementing multitasking."""

import requests
import threading

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
        imageLinks {[string]} -- [description]
        numberOfValidLinks_t {[type]} -- [description]
        validLinks_t {[type]} -- [description]
        unvalidLinks_t {[type]} -- [description]
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
