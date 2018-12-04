from FileToRun import getContents

# ------Input----- #
answer1 = 0
answer2 = 0
contents = getContents(1, True)

frequencies = list(map(int, contents.split("\n")))

# ------Part 1------ #
answer1 = sum(frequencies)

# ------Part 2------ #
seenFrequencies = []
currentFrequency = 0
repeatFound = False
while not repeatFound:
    for f in frequencies:
        currentFrequency += f
        if currentFrequency in seenFrequencies:
            answer2 = currentFrequency
            repeatFound = True
            break
        else:
            seenFrequencies.append(currentFrequency)

# ------Output----- #
print("Answer 1: " + str(answer1))
print("Answer 2: " + str(answer2))
