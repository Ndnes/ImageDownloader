import unittest
import utility


class TestUtility(unittest.TestCase):

    def test_visualTests(self):
        for i in range(11):
            utility.printProgress(i/10)
            print('')
        print('\n')
        for i in range(11):
            utility.printProgress(i/10, width=(i * 4))
            print('')
        print('\n\n Now testing single line progress\n')
        for i in range(11):
            utility.printProgress(
                i/10, width=60, preText='TestPretext',
                postText='TestPosttext', showNumber=False)
        print('')

    def test_badInputs(self):
        print('\n\n')
        utility.printProgress(-2)
        print('')
        utility.printProgress(0.3, width=-2)
        print('')


if __name__ == '__main__':
    unittest.main()
