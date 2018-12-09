from GetFile import getContents
from bisect import insort
import copy

# ------Classes------ #
class Condition:
    def __init__(self, conditionString):
        conditionStringSplit = conditionString.split(' ')
        self.parent = conditionStringSplit[1]
        self.child = conditionStringSplit[7]

class Step:
    def __init__(self, stepName):
        self.name = stepName
        self.children = []
        self.predecessors = 0


    def addChild(self, childName):
        self.children.append(childName)

    def addPredecessor(self):
        self.predecessors += 1

    def removePredecessor(self):
        self.predecessors -= 1

class TimeStamp:
    def __init__(self, timeFinished, stepName):
        self.timeFinished = timeFinished
        self.stepName = stepName

# ------Input------ #
answer1 = 0
answer2 = 0
contents = getContents(7, True)

conditions = list(map(Condition, contents.split('\n')))

# ------Part 1------ #
# Make a conditions dictionary and save how many references a condition has:
stepsDictPt1 = {}
for condition in conditions:
    if condition.parent not in stepsDictPt1:
        stepsDictPt1[condition.parent] = Step(condition.parent)
        stepsDictPt1[condition.parent].addChild(condition.child)
    else:
        stepsDictPt1[condition.parent].addChild(condition.child)
    if condition.child not in stepsDictPt1:
        stepsDictPt1[condition.child] = Step(condition.child)
        stepsDictPt1[condition.child].addPredecessor()
    else:
        stepsDictPt1[condition.child].addPredecessor()
stepsDictPt2 = copy.deepcopy(stepsDictPt1)

# Find out which conditions do not have predecessors
availableStepsPt1 = []
for stepName, stepObj in stepsDictPt1.items():
    if stepObj.predecessors == 0:
        insort(availableStepsPt1, stepName)
availableStepsPt2 = copy.deepcopy(availableStepsPt1)

# Recurse over list, adding chain of commands as we go
resultString = ""
while availableStepsPt1:
    # Add this step to our list
    currentStepName = availableStepsPt1.pop(0)
    resultString += currentStepName

    # Remove predecessor from children
    currentStepChildren = stepsDictPt1[currentStepName].children
    for childName in currentStepChildren:
        childObj = stepsDictPt1[childName]
        childObj.removePredecessor()
        if childObj.predecessors == 0:
            insort(availableStepsPt1, childName)

answer1 = resultString

# ------Part 2------ #
workers = 5
baseTime = 60
currentTime = 0
timeStamps = []

# Loop through availableSteps, making note of when each step is finished for nice concurrency
while timeStamps or currentTime == 0:
    # A step has finished
    if timeStamps:
        currentTimeStamp = timeStamps.pop(0)
        finishedStepName = currentTimeStamp.stepName
        currentTime = currentTimeStamp.timeFinished
        workers += 1

        # Remove predecessor from children
        currentStepChildren = stepsDictPt2[finishedStepName].children
        for childName in currentStepChildren:
            childObj = stepsDictPt2[childName]
            childObj.removePredecessor()
            if childObj.predecessors == 0:
                insort(availableStepsPt2, childName)

    # Assign new steps
    while availableStepsPt2 and workers > 0:
        currentStepName = availableStepsPt2.pop(0)
        workers -= 1
        timeStamps.append(TimeStamp(currentTime + baseTime + ord(currentStepName) - ord('A') + 1, currentStepName))
        timeStamps = sorted(timeStamps, key=lambda ts: ts.timeFinished)

answer2 = currentTime

# ------Output------ #
print("Answer 1: " + str(answer1))
print("Answer 2: " + str(answer2))