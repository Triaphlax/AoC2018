from GetFile import getContents

# ------Input------ #
answer1 = 0
answer2 = 0
contents = getContents(2, True)

boxIDs = contents.split("\n")

# ------Part 1------ #
letter2 = 0
letter3 = 0

# Go through the entire list of boxes
for box in boxIDs:
    # For a box ID, note how often each char appears
    letterFreqs = {}
    for char in box:
        letterFreqs[char] = letterFreqs.get(char, 0) + 1

    # Count whether or not this word has chars occurring twice or thrice
    hasLetter2 = False
    hasLetter3 = False
    for letter, freq in letterFreqs.items():
        if hasLetter2 and hasLetter3:
            break
        if freq == 2 and not hasLetter2:
            hasLetter2 = True
        elif freq == 3 and not hasLetter3:
            hasLetter3 = True

    # Increase our counters if necessary
    if hasLetter2:
        letter2 += 1
    if hasLetter3:
        letter3 += 1

answer1 = letter2 * letter3


# ------Part 2------ #
def findMatchingID(boxIndex):
    """
    Finds out whether or not a boxID differs by one character from another boxID that comes after in in boxIDs
    @param boxIndex: Index of the boxID to check correspoding to boxIDs
    @return: The boxID with the differing chracter removed, or "" if no such match found
    """

    # Loop through all boxIDs
    currentBoxID = boxIDs[boxIndex]
    for _, otherBoxID in enumerate(boxIDs[boxIndex+1:], start=boxIndex+1):

        # Loop through the string of our boxID
        possibleIndex = -1
        strikes = 0
        solutionPossible = False
        for j, ch in enumerate(currentBoxID):
            # If a char matches between the two strings
            if currentBoxID[j] != otherBoxID[j]:
                strikes += 1
                if strikes == 1: # One strike means possible solution
                    solutionPossible = True
                    possibleIndex = j
                elif strikes == 2: # Two strikes means a solution is no longer possible
                    solutionPossible = False
                    break
        if solutionPossible:
            return currentBoxID[:possibleIndex] + currentBoxID[(possibleIndex+1):]
    return ""

# Check for a matching boxID for all boxIDs in our list
result = ""
for i in range(0, len(boxIDs)):
    result = findMatchingID(i)
    if result != "":
        break

answer2 = result

# ------Output------ #
print("Answer 1: " + str(answer1))
print("Answer 2: " + str(answer2))
