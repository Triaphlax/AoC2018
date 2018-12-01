import os

# ------Input----- #
answer1 = 0
answer2 = 0

dirname = os.path.dirname('..\\Input\\')
contents1 = open(os.path.join(dirname, 'Input01_1.txt'), 'r').read()

# ------Part 1------ #
frequencies = list(map(int, contents1.split("\n")))
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
