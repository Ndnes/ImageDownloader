

def printProgress(progress,
                  preText='Progress: ',
                  postText='% complete',
                  width=25,
                  showNumber=True):
    """Prints progress to the terminal.
# noqa W293
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
    print(progressString)
