from FileToRun import getContents

# ------Input----- #
answer1 = 0
answer2 = 0
contents = getContents(2, True)

boxIDs = contents.split("\n")

# ------Part 1------ #
letter2 = 0
letter3 = 0
for box in boxIDs:
    letterFreqs = {}
    for char in box:
        letterFreqs[char] = letterFreqs.get(char, 0) + 1
    hasLetter2 = False
    hasLetter3 = False
    for letter, freq in letterFreqs.items():
        if hasLetter2 and hasLetter3:
            break
        if freq == 2 and not hasLetter2:
            hasLetter2 = True
        elif freq == 3 and not hasLetter3:
            hasLetter3 = True
    if hasLetter2:
        letter2 += 1
    if hasLetter3:
        letter3 += 1

answer1 = letter2 * letter3


# ------Part 2------ #
def findMatchingID(boxIndex):
    currentBoxID = boxIDs[boxIndex]
    for _, otherBoxID in enumerate(boxIDs[boxIndex+1:], start=boxIndex+1):
        possibleIndex = -1
        strikes = 0
        solutionPossible = False
        for j, ch in enumerate(currentBoxID):
            if currentBoxID[j] != otherBoxID[j]:
                strikes += 1
                if strikes == 1:
                    solutionPossible = True
                    possibleIndex = j
                elif strikes == 2:
                    solutionPossible = False
                    break
        if solutionPossible:
            return currentBoxID[:possibleIndex] + currentBoxID[(possibleIndex+1):]
    return ""


answer2 = ""
for i in range(0, len(boxIDs)):
    answer2 = findMatchingID(i)
    if answer2 != "":
        break

# ------Output----- #
print("Answer 1: " + str(answer1))
print("Answer 2: " + str(answer2))
