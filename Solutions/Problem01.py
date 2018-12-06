from GetFile import getContents

# ------Input------ #
answer1 = 0
answer2 = 0
contents = getContents(1, True)

# Parse the frequencies and put them in a list
frequencies = list(map(int, contents.split("\n")))

# ------Part 1------ #

#  Sum the entire list of frequencies
answer1 = sum(frequencies)

# ------Part 2------ #

# Keep track of frequencies we've seen
seenFrequencies = []
currentFrequency = 0
repeatFound = False

# Update the frequency list every step of the way
while not repeatFound:
    for f in frequencies:
        currentFrequency += f
        # If we find a frequency we've already encoutered, stop and note the answer
        if currentFrequency in seenFrequencies:
            answer2 = currentFrequency
            repeatFound = True
            break
        else:
            seenFrequencies.append(currentFrequency)

# ------Output------ #
print("Answer 1: " + str(answer1))
print("Answer 2: " + str(answer2))
