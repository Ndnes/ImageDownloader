"""Unit testing module for multitasking module."""

import unittest
import multitasking
import requests
from multitasking import WorkTask

urlLink = \
    'http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=n01729977'

r = requests.get(urlLink, timeout=1)
urlString = r.content.decode()

urlList = str.splitlines(urlString)
numberOfValidLinks_t = 0
validLinks_t = []
unvalidLinks_t = []


class TestMultitasking(unittest.TestCase):

    def setUp(self):
        self.workTask_1 = WorkTask()
        self.workTask_1.cpuNumber = 1
        self.workTask_1.startCount = 0
        self.workTask_1.endCount = 10
        self.workTask_1.workList = urlList[:10]

    def tearDown(self):
        pass

    def test_findNumberOfValidLinks(self):
        #  TODO: Refactor Do setup in a setUp method.
        urlLink = \
        'http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=n01729977'# noqa

        r = requests.get(urlLink, timeout=1)
        urlString = r.content.decode()

        urlList = str.splitlines(urlString)
        numberOfValidLinks_t = [0]
        validLinks_t = ['']
        unvalidLinks_t = ['']
        numberOfTestLinks = 6
        try:
            multitasking.findNumberOfValidLinks(
                                            urlList[:(numberOfTestLinks)],
                                            numberOfValidLinks_t,
                                            validLinks_t,
                                            unvalidLinks_t,
                                            0)
        except Exception as e:
            self.fail('Unexpected exception')
            print(f'\n\n {e}')
        else:
            self.assertEqual(numberOfValidLinks_t[0], numberOfTestLinks)
            self.assertEqual(len(validLinks_t[0]), numberOfTestLinks)


if __name__ == "__main__":
    unittest.main()
