from GetFile import getContents
from re import split
from math import sin, cos, radians

# ------Classes------ #

class Star:
    def __init__(self, string):
        words = split('<|>|, ', string)
        self.position = (int(words[1]), int(words[2]))
        self.velocity = (int(words[4]), int(words[5]))

    def updatePosition(self):
        self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])

    def addOffset(self, offset):
        return self.position[0] + offset[0], self.position[1] + offset[1]


# ------Input------ #
answer1 = 0
answer2 = 0
contents = getContents(10, True)

starList = list(map(Star, contents.split('\n')))

# ------Part 1------ #
# Function that checks the score for a given list of stars
# It basically awards points for straight lines in one of the compass directions
def calculateScore(starDict):
    score = 0
    for starsAtThisPoint in starDict.values():
        for star in starsAtThisPoint:
            # We only need to look at two compass directions here: East and North
            for k in range(0,2):
                scoreThisRound = 0
                baseOffset = (int(sin(radians(90 * k))), int(cos(radians(90 * k))))
                hasNeighbor = True
                scalar = 1
                while hasNeighbor:
                    offset = tuple(c * scalar for c in baseOffset)
                    newPositionToCheck = star.addOffset(offset)
                    if newPositionToCheck in starDict:
                        scoreThisRound += scoreThisRound + 1
                        scalar += 1
                    else:
                        hasNeighbor = False
                        score += scoreThisRound
    return score


# Initialize the points first
newStarDict = {}
for star in starList:
    if star.position not in newStarDict:
        newStarDict[star.position] = [star]
    else:
        newStarDict[star.position].append(star)
firstScore = calculateScore(newStarDict)
averageScore = firstScore
totalRounds = 1
OUTLIER_MARGIN = 200

while True:

    # Adjust the positions of the stars each round
    prevStarDict = newStarDict
    newStarDict = {}
    for starsAtThisPoint in prevStarDict.values():
        for star in starsAtThisPoint:
            star.updatePosition()
            if star.position not in newStarDict:
                newStarDict[star.position] = [star]
            else:
                newStarDict[star.position].append(star)
    prevStarDict = {}

    # Calculate the new score for these stars
    newScore = calculateScore(newStarDict)

    # If it's an outlier, print the stars
    if newScore > averageScore * OUTLIER_MARGIN:

        # Determine the dimensions of the grid
        minX = 0
        minY = 0
        maxX = 0
        maxY = 0
        for starsAtThisPoint in newStarDict.values():
            for star in starsAtThisPoint:
                if star.position[0] < minX:
                    minX = star.position[0]
                elif star.position[0] > maxX:
                    maxX = star.position[0]
                if star.position[1] < minY:
                    minY = star.position[1]
                elif star.position[1] > maxY:
                    maxY = star.position[1]

        # Draw the grid
        vizString = "\n"
        for yCoord in range(minY, maxY+1):
            for xCoord in range(minX, maxX+1):
                if (xCoord, yCoord) in newStarDict:
                    vizString += '#'
                else:
                    vizString += '.'
            vizString += '\n'
        answer1 = vizString
        answer2 = totalRounds
        break
        
    # Otherwise, just move onto the next round
    else:
        averageScore = ((averageScore * totalRounds) + newScore) / (totalRounds + 1)
        totalRounds += 1

# ------Part 2------ #

# ------Output------ #
print("Answer 1: " + str(answer1))
print("Answer 2: " + str(answer2))