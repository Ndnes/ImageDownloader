"""Module for all activity implementing multitasking."""


class WorkTask:
    """Store tasks that will be assigned to logical processors."""

    def __init__(self):
        """Initialize instance of WorkTask."""
        self.cpuNumber = 1
        self.startCount = None
        self.endCount = None
        self.workList = None
