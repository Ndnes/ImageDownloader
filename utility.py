"""This module does various utility functions such as printing progress bar."""

import config
import time


def getProgress(workDescription='Progress: '):
    """Gets progress from threads. Uses global variable

    Keyword Arguments:
        workDescription {str} -- Describes the monitored work
                                 (default: {'Progress: '})
    """
    progress = 0.0
    while progress < 100.0:
        progress = min(config.g_progress)
        printProgress(progress, preText=workDescription)
        time.sleep(0.25)
    config.g_progress = [0.0] * len(config.g_progress)


def printProgress(progress,
                  preText='Progress: ',
                  postText='% complete',
                  width=25,
                  showNumber=True):
    """Print progress to the terminal.

    Arguments:
        progress {float} -- The amount of progress from 0.0 to 1.0.
    Keyword Arguments:
        preText {str} -- Text appearing before the progress bar
                         (default: {'Progress: '})
        postText {str} -- [description] (default: {'% complete'})
        width {int} -- [description] (default: {25})
        showNumber {bool} -- [description] (default: {True})
    """
# TODO: Figure out how to handle blank line error in docstrings.
    numberOfBars = int(progress*width)
    numberOfWhitespaces = width - numberOfBars
    bars = '▓' * numberOfBars
    whitSpaces = '░' * numberOfWhitespaces
    if showNumber:
        progressString = \
            f'{preText}{bars}{whitSpaces} {progress * 100}{postText}\r'
    else:
        progressString = f'{preText}{bars}{whitSpaces}{postText}\r'
    print(progressString, end='')
