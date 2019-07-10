from multiprocessing import Process, freeze_support
from threading import Thread
from pathlib import Path
import os
import urllib
import cv2
import numpy as np
import requests
import time

# Custom modules
import utility
import multitasking
import config

# Get input from user.

imgType = input('\n\nPlease enter image type name.\n')

workDirString = input('\n\nPlease enter the path to save images.\n\
    \rEnter a blank path to use current_directory/image_type_name as path.\n')
if not workDirString:
    workDir = f'{os.getcwd()}/{imgType}'
else:
    # Replace \ with / to ensure path will work.
    workDirString = workDirString.replace(os.sep, '/')
    workDir = Path(workDirString)

imgLink = input(
    '\n\nPlease provide a link to an \"image-net.org\" downloads page.\n\
    \rAlternatively leave this input empty and enter links manually.\n')

if not imgLink:
    print("\n\nYou left the previous input blank.\n\
          \rPlease copy/paste a set of image links separated by newlines.\n\
          \rTo finish entering sites enter a blank input.\n")
    rawUrlList = []
    while True:  # This while loop is needed to get multiple lines at once.
        try:
            line = input()
        except EOFError:
            break
        if not line:
            break
        rawUrlList.append(line)
else:
    imageUrls = urllib.request.urlopen(imgLink).read().decode()
    rawUrlList = imageUrls.splitlines()

size = []
grayScale = False

ans = input('\n\nDo you wish to resize images? y/n\n')
if 'y' in ans:
    size.append(int(input('\r\n\nEnter desired width.\n')))
    size.append(int(input('\r\n\nEnter desired height.\n')))

ans = input('\n\nConvert image to gray-scale? y/n\n')
if 'y' in ans:
    print('\n\rImage will be converted to gray-scale')
    grayScale = True
else:
    print('\n\rImage will not be converted to gray-scale')

time.sleep(0.7)

# 1 thread is reserved for reporting progress.
numberOfWorkThread = os.cpu_count() - 1  # TODO: Find a more robust method
workCounts = multitasking.divideWorkload(rawUrlList, numberOfWorkThread)

# Init mutable objects to store results from threads
threads = [None] * numberOfWorkThread
numberOfValidLinks_t = [None] * numberOfWorkThread
validLinks_t = [None] * numberOfWorkThread
unvalidLinks_t = [None] * numberOfWorkThread
config.g_progress = [0.0] * numberOfWorkThread  # Global progress variable

# Validate links with multithreading
i = 0
cnt = 0
progressThread = Thread(
                    target=utility.getProgress,
                    kwargs={'workDescription': 'Verifying URLs: '})
for linkCount in workCounts:
    threads[i] = Thread(
                    name=(f'Thread_{i:03d}'),
                    target=multitasking.findNumberOfValidLinks,
                    args=(
                        rawUrlList[cnt:cnt+linkCount],
                        numberOfValidLinks_t,
                        validLinks_t,
                        unvalidLinks_t, i))
    # f'{i:03d}' converts the integer i to a 3 digit 0 leading padded string.
    threads[i].start()
    i += 1
    cnt += linkCount

progressThread.start()

# Close all threads.
for i in range(len(threads)):
    threads[i].join()
progressThread.join()

# Merge results from the threads.
numberOfValidLinks = 0
validLinks = []
unvalidLinks = []
for i in range(numberOfWorkThread):
    numberOfValidLinks += numberOfValidLinks_t[i]
    validLinks += validLinks_t[i]
    unvalidLinks += unvalidLinks_t[i]

if len(validLinks) > 0:
    print(f"\n\nThere are {numberOfValidLinks} valid links,\
           the first link is {validLinks[0]}")
    print(unvalidLinks)
