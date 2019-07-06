"""Unit testing module for multitasking module."""

import unittest
import multitasking
import requests
from multitasking import WorkTask
import os


urlLink = \
    'http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=n01729977'

numberOfValidLinks_t = 0
validLinks_t = []
unvalidLinks_t = []


class TestMultitasking(unittest.TestCase):

    def setUp(self):
        r = requests.get(urlLink, timeout=1)
        urlString = r.content.decode()

        self.urlList = str.splitlines(urlString)

        self.workTask_1 = WorkTask()
        self.workTask_1.cpuNumber = 1
        self.workTask_1.startCount = 0
        self.workTask_1.endCount = 6
        self.workTask_1.workList = self.urlList[:6]

        self.directory = 'testingDir'
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        self.workNumbers = multitasking.divideWorkload(
                                                self.workTask_1.workList,
                                                3)

    def tearDown(self):
        pass
        # os.remove(self.directory)
        # TODO: Mock filesystem to create and delete test-files.

    def test_findNumberOfValidLinks(self):
        #  TODO: Refactor Do setup in a setUp method.
        numberOfValidLinks_t = [0]
        validLinks_t = ['']
        unvalidLinks_t = ['']
        try:
            multitasking.findNumberOfValidLinks(
                                            self.workTask_1.workList,
                                            numberOfValidLinks_t,
                                            validLinks_t,
                                            unvalidLinks_t,
                                            0)
        except Exception as e:
            self.fail('Unexpected exception')
            print(f'\n\n {e}')
        else:
            self.assertEqual(numberOfValidLinks_t[0], self.workTask_1.endCount)
            self.assertEqual(len(validLinks_t[0]), self.workTask_1.endCount)

    def test_divideWorkLoad(self):
        testList = self.workTask_1.workList
        cpuNumber = len(testList)
        # Testing edge case when there are as many items in list as cores.
        ret = multitasking.divideWorkload(testList, cpuNumber)
        self.assertEqual(len(ret), len(testList))
        self.assertEqual(len(testList), sum(ret))
        for number in ret:
            self.assertLessEqual(number, len(testList) / cpuNumber + 1)
        # Testing that only one list element is returned when 1 core.
        cpuNumber = 1
        ret = multitasking.divideWorkload(testList, cpuNumber)
        self.assertEqual(len(ret), 1)
        self.assertEqual(ret[0], len(testList))
        self.assertEqual(len(testList), sum(ret))
        for number in ret:
            self.assertLessEqual(number, len(testList) / cpuNumber + 1)
        # Testing edge case when there are more cores than items.
        cpuNumber = len(testList) + 3
        ret = multitasking.divideWorkload(testList, cpuNumber)
        self.assertEqual(len(testList), sum(ret))
        for number in ret:
            self.assertLessEqual(number, len(testList) / cpuNumber + 1)

    def test_assignWorkTasks(self):
        ret = multitasking.assignWorkTasks(self.workNumbers,
                                           self.workTask_1.workList,
                                           self.directory)
        self.assertEqual(len(ret), len(self.workNumbers))

    def test_saveImages():
        pass
    # TODO: Finish this test.


if __name__ == "__main__":
    unittest.main()
