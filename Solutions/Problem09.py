from GetFile import getContents


# ------Classes------ #
class Marble:
    def __init__(self, value, previous, next):
        self.value = value
        self.previous = previous
        self.next = next

class Player:
    def __init__(self, elfID):
        self.elfID = elfID
        self.score = 0

    def addScore(self, scoreToAdd):
        self.score += scoreToAdd

# ------Input------ #
answer1 = 0
answer2 = 0
contents = getContents(9, True)

words = contents.split(' ')
totalPlayers = int(words[0])
totalMarbles = int(words[6])

# ------Parts 1 & 2------ #
# Place the first marble
currentMarble = Marble(0, 0, 0)
currentMarble.next = currentMarble
currentMarble.previous = currentMarble

part1Stop = totalMarbles
part2Stop = totalMarbles * 100

currentMarbleValue = 1
currentPlayerID = 0
playerDict = {}
highestScoreSoFar = 0
# Play the game
while currentMarbleValue <= part2Stop:
    # If we have a multiple of 23
    if currentMarbleValue % 23 == 0:
        # Add new player if necessary
        if currentPlayerID not in playerDict:
            playerDict[currentPlayerID] = Player(currentPlayerID)

        # Add points for the marble that was about to be placed
        thisPlayer = playerDict[currentPlayerID]
        thisPlayer.addScore(currentMarbleValue)

        # Set the new current marble
        currentMarble = currentMarble.previous.previous.previous.previous.previous.previous

        # Remove the marble 7 before the previous current marble and add the score
        marbleToRemove = currentMarble.previous
        thisPlayer.addScore(marbleToRemove.value)
        marbleToRemove.previous.next = marbleToRemove.next
        marbleToRemove.next.previous = marbleToRemove.previous

        # Update highest score so far
        if thisPlayer.score > highestScoreSoFar:
            highestScoreSoFar = thisPlayer.score

    # If we don't have a multiple of 23
    else:
        # Get the two next marbles clockwise
        beforeMarble = currentMarble.next
        afterMarble = currentMarble.next.next

        # Make a new marble, and add this to the circle
        thisMarble = Marble(currentMarbleValue, beforeMarble, afterMarble)
        beforeMarble.next = thisMarble
        afterMarble.previous = thisMarble
        currentMarble = thisMarble

    # Find the current highest score at our two stopping points
    if currentMarbleValue == part1Stop:
        answer1 = highestScoreSoFar
    if currentMarbleValue == part2Stop:
        answer2 = highestScoreSoFar

    # Update the player and the current marble value
    currentMarbleValue += 1
    currentPlayerID = (currentPlayerID + 1) % totalPlayers

# ------Output------ #
print("Answer 1: " + str(answer1))
print("Answer 2: " + str(answer2))