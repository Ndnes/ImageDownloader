"""Unit testing module for utility module."""


import unittest
import utility


class TestUtility(unittest.TestCase):
    """Unit test class.

    Arguments:
        unittest {module?} -- Module to run that will test other module.
    """

    # TODO: Write test for getProgress()

    def test_visualTests(self):
        """Tests printProgress() visually. (Verify in terminal)."""
        iterations = 11
        f"\n\nTesting {iterations} iterations.\n"
        for i in range(iterations):
            utility.printProgress(i/10)
            print('')
        print('\n')
        print(f'\n\nTesting {iterations} iterations with varying length.\n')
        for i in range(iterations):
            utility.printProgress(i/10, width=(i * 4))
            print('')
        print('\n\nTesting single line progress\n')
        for i in range(iterations):
            utility.printProgress(
                i/10, width=60, preText='TestPretext',
                postText='TestPosttext', showNumber=False)
        print('')

    def test_badInputs(self):
        """Test that bad inputs do not crash the application."""
        unexpectedExceptionString = "printProgress() unexpected exception"

        print('\n\n')

        try:
            utility.printProgress(-2)
        except Exception as e:
            self.fail(unexpectedExceptionString)
            print(f'\n\n {e}')
        print('')

        try:
            utility.printProgress(0.3, width=-2)
        except Exception as e:
            self.fail(unexpectedExceptionString)
            print(f'\n\n {e}')
        print('')


if __name__ == '__main__':
    unittest.main()
