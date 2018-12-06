from GetFile import getContents
from enum import Enum
import datetime


# ------Classes------ #
class TimeStampType(Enum):
    START = 1
    SLEEP = 2
    AWAKE = 3


DATE_START_INDEX = 1
DATE_END_INDEX = 17
TYPE_INDEX = 19
GUARD_INDEX = 25
LETTERS = {'G': TimeStampType.START,
           'f': TimeStampType.SLEEP,
           'w': TimeStampType.AWAKE}


class TimeStamp:
    # Assuming layout of [yyyy-mm-dd ii-ss] TimeStampType
    def __init__(self, timeStampStr):
        dateStr = timeStampStr[DATE_START_INDEX:DATE_END_INDEX]
        self.date = datetime.datetime.strptime(dateStr, "%Y-%m-%d %H:%M")
        self.type = LETTERS[timeStampStr[TYPE_INDEX]]
        if self.type == TimeStampType.START:  # We only keep note of a guard when it's their START timestamp
            self.guardID = timeStampStr[GUARD_INDEX:].split(' ')[0]


class Guard:
    def __init__(self, guardID):
        self.guardID = guardID
        self.minutesSlept = 0
        self.log = {}

    # Update sleep log with minutes in which guard fell asleep and woke up
    def updateSleepLog(self, start, end):
        if start not in self.log:
            self.log[start] = 1
        else:
            self.log[start] += 1
        if end not in self.log:
            self.log[end] = -1
        else:
            self.log[end] -= 1
        self.minutesSlept += end - start

    # Determine in which minute the guard slept the most
    # Return tuple of form (Days slept, Minute slept on)
    def getMinuteMostSleptIn(self):
        currentDays = 0
        currentBestMinute = (0, 0)  #  Days slept, Minute in question
        for minit in range(0,60):
            if minit in self.log:
                currentDays += self.log[minit]
                if currentDays > currentBestMinute[0]:
                    currentBestMinute = (currentDays, minit)
        return currentBestMinute

# ------Input------ #
answer1 = 0
answer2 = 0
contents = getContents(4, True)

timestamps = list(map(TimeStamp, contents.split('\n')))
timestamps = sorted(timestamps, key=lambda ts: ts.date)

# ------Part 1------ #

# Loop through timestamps and update guards accordingly
guardList = {}
currentGuard = 0
minuteFellAsleep = 0
guardAsleep = False
sleepiestGuard = 0  # GuardID, minutes asleep
for ts in timestamps:

    # Guard starts their shift
    if ts.type == TimeStampType.START:
        if guardAsleep:
            raise ValueError("New shift start while previous guard still asleep")

        # Add guard to guardList if new
        if ts.guardID not in guardList:
            guardList[ts.guardID] = Guard(ts.guardID)

        # Update currentGuard and sleepiestGuard if uninitialized
        currentGuard = guardList[ts.guardID]
        if sleepiestGuard == 0:
            sleepiestGuard = currentGuard

    # Guard falls asleep
    elif ts.type == TimeStampType.SLEEP:
        guardAsleep = True
        minuteFellAsleep = ts.date.minute

    # Guard wakes up
    elif ts.type == TimeStampType.AWAKE:
        guardAsleep = False
        currentGuard.updateSleepLog(minuteFellAsleep, ts.date.minute)

        # If this guard has been asleep for longer than current best, update sleepiestGuard
        if currentGuard.minutesSlept > sleepiestGuard.minutesSlept:
            sleepiestGuard = currentGuard

answer1 = sleepiestGuard.getMinuteMostSleptIn()[1] * int(sleepiestGuard.guardID[1:])

# ------Part 2------ #

# Loop through guardList and get minute most slept in for all guards
guardAsleepTheMost = (0, 0, "")  # Days asleep, Minute slept on, guardID
for guardID in guardList:
    resultTuple = guardList[guardID].getMinuteMostSleptIn()
    if resultTuple[0] > guardAsleepTheMost[0]:
        guardAsleepTheMost = (resultTuple[0], resultTuple[1], guardID)

answer2 = guardAsleepTheMost[1] * int(guardAsleepTheMost[2][1:])

# ------Output------ #
print("Answer 1: " + str(answer1))
print("Answer 2: " + str(answer2))