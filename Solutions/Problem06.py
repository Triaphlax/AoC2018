from GetFile import getContents
from SortedSearch import find_gt_index

# ------Classes------ #
NO_ALLEGIANCE = '.'
EQUAL_ALLEGIANCE = '*' \
                   ''
class Grid:
    def __init__(self, x, y, width, height):
        self.x = x - 1  # Make grid one size bigger
        self.y = y - 1
        self.width = width + 2
        self.height = height + 2
        self.size = (self.x + self.width) * (self.y + self.height)
        self.grid = {}
        for i in range(self.x, self.x + self.width):
            for j in range(self.y, self.y + self.height):
                pointString = self.tupleToString((i, j))
                self.grid[pointString] = Point(pointString, i, j)
        self.pointsCaptured = 0
        self.pointsCapturedInRound = {}  # Points Captured, Round

    def explore(self, coordinate, expRound):
        if expRound not in self.pointsCapturedInRound:
            self.pointsCapturedInRound[expRound] = 0
        toExplore = coordinate.getExplorablePoints(expRound, self)
        for pointToExplore in toExplore:
            pointString = self.tupleToString(pointToExplore)
            wasPointUndiscovered = self.grid[pointString].setAllegiance(coordinate.name, expRound)
            if wasPointUndiscovered:
                self.pointsCaptured += 1
                self.pointsCapturedInRound[expRound] += 1

    def visualizeGrid(self):
        gridVis = ""
        for yValue in range(self.y, self.y + self.height):
            for xValue in range(self.x, self.x + self.width):
                gridVis += self.grid[self.tupleToString((xValue, yValue))].allegiance
            gridVis += '\n'
        print(gridVis)
        return gridVis

    def tupleToString(self, pointTuple):
        return "(" + str(pointTuple[0]) + ", " + str(pointTuple[1]) + ")"
    
    def isGridFull(self):
        return self.size == self.pointsCaptured

    def pointsCapturedForRound(self, expRound):
        return self.pointsCapturedInRound[expRound]

class Point:
    def __init__(self, pointID, x, y):
        self.pointID = pointID
        self.x = x
        self.y = y
        self.allegiance = NO_ALLEGIANCE
        self.roundSet = -1

    # Sets the allegiance for this point
    # Return True is point was undiscovered
    def setAllegiance(self, coordID, expRound):
        if self.roundSet == -1:  #  Point undiscovered
            self.allegiance = coordID
            self.roundSet = expRound
            coordinateDictionary[coordID].addPointCaptured()
            return True
        elif self.roundSet == expRound:  #  Point was discovered in this round
            overwrittenAllegiance = self.allegiance
            if overwrittenAllegiance != EQUAL_ALLEGIANCE:
                coordinateDictionary[overwrittenAllegiance].removePointCaptured()
                self.allegiance = EQUAL_ALLEGIANCE
            return False

class Coordinate:
    # Assuming string of the form 'x, y'
    def __init__(self, coordString):
        coords = coordString.split(', ')
        self.x = int(coords[0])
        self.y = int(coords[1])
        self.name = coords[2]
        self.pointsCaptured = 0

    # Determine the coordinates at exactly Manhattan distance from this coordinate
    def getExplorablePoints(self, distance, grid):
        # If distance is 0, the only point we have to explore is ourselves
        if distance == 0:
            return [(self.x, self.y)]

        # Determine all explorable points
        result = []
        for i in range(0, distance+1):
            for shouldXNegative in range(0, 2):
                for shouldYNegative in range(0, 2):
                    offsetX = (-1)**shouldXNegative * (distance - i)
                    offsetY = (-1)**shouldYNegative * i

                    if (shouldXNegative and offsetX == 0) \
                        or (shouldYNegative and offsetY == 0):
                        continue

                    coordX = offsetX + self.x
                    coordY = offsetY + self.y

                    # If we're outside the grid range, then continue
                    if coordX < grid.x or coordX > grid.x + grid.width - 1 \
                            or coordY < grid.y or coordY > grid.y + grid.height - 1:
                        continue

                    result.append((coordX, coordY))
        return result

    # Add a point captured by this coordinate
    def addPointCaptured(self):
        self.pointsCaptured += 1

    # Remove a point captured by this coordinate
    def removePointCaptured(self):
        self.pointsCaptured -= 1


# ------Input------ #
answer1 = 0
answer2 = 0
contents = getContents(6, True)

# Adjust coordinate list to also add names to them
sepCoordinateStrList = contents.split('\n')
coordinateStrList = [coordStr + ", " + str(chr(i + ord('a')))
                     for i, coordStr in enumerate(sepCoordinateStrList)]

coordinateList = list(map(Coordinate, coordinateStrList))
coordinateDictionary = {coord.name: coord for coord in coordinateList}

# ------Part 1------ #
smallestX = int(min(crd.x for crd in coordinateList))
smallestY = int(min(crd.y for crd in coordinateList))
largestX = int(max(crd.x for crd in coordinateList))
largestY = int(max(crd.y for crd in coordinateList))

area = Grid(smallestX, smallestY, largestX - smallestX + 1, largestY - smallestY + 1)

# Start exploring from each coordinate
distanceExplored = 0
while not area.isGridFull():
    for coord in coordinateList:
        area.explore(coord, distanceExplored)
    if area.pointsCapturedForRound(distanceExplored) == 0:
        break
    distanceExplored += 1

# Check outer edges for coordinates
# Outer columns
for x in range(area.x, area.x + area.width, area.width - 1):
    for y in range(area.y, area.y + area.height):
        allegiance = area.grid[area.tupleToString((x,y))].allegiance
        if allegiance in coordinateDictionary:
            del coordinateDictionary[allegiance]

# Outer rows
for y in range(area.y, area.y + area.height, area.height - 1):
    for x in range(area.x + 1, area.x + area.width - 1):  # We have already checked the first and the last one
        allegiance = area.grid[area.tupleToString((x, y))].allegiance
        if allegiance in coordinateDictionary:
            del coordinateDictionary[allegiance]

answer1 = max(map(lambda c: c.pointsCaptured, coordinateDictionary.values()))

# ------Part 2------ #

def adjustCoordList(crdList):
    sortedCrdList = sorted(crdList)
    minCrd = min(sortedCrdList)
    return list(map(lambda crd: crd - minCrd, sortedCrdList))


def getManhattanDistanceForAxis(crdList):
    startDist = sum(crdList)
    manhatDistances = [startDist]
    offset = len(crdList)
    coordIndex = 0
    distance = startDist
    length = crdList[-1] - crdList[0] + 1
    for i in range(1, length):
        while coordIndex < len(crdList) and i > crdList[coordIndex]:
            coordIndex += 1
            offset -= 2
        distance -= offset
        manhatDistances.append(distance)
    return manhatDistances


# Get the x- and y-coordinates for our safe zones
xs = adjustCoordList([c.x for c in coordinateList])
ys = adjustCoordList([c.y for c in coordinateList])

# Determine the Manhattan distance along the x- and y-axes
xManHatDists = sorted(getManhattanDistanceForAxis(xs))
yManHatDists = sorted(getManhattanDistanceForAxis(ys))

totalDistance = 10000
closenessArea = 0
yIndex = len(yManHatDists)
for i, xDist in enumerate(xManHatDists):
    if yIndex == 0:
        break
    upperBoundYDist = totalDistance - xManHatDists[i] - 1
    if i == 0:
        yIndex = find_gt_index(yManHatDists, upperBoundYDist)
        closenessArea += yIndex
    else:
        while yIndex > 0 and yManHatDists[yIndex-1] > upperBoundYDist:
            yIndex -= 1
        closenessArea += yIndex


answer2 = closenessArea

# ------Output------ #
print("Answer 1: " + str(answer1))
print("Answer 2: " + str(answer2))