from GetFile import getContents
from SortedSearch import find_le_index
from blist import blist


# ------Classes------ #
class Rectangle:
    def __init__(self, rectID, x, y, width, height):
        self.rectID = rectID
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    # Assuming string of format 'rectID @ x,y: widthxheight'
    def __init__(self, string):
        parts = string.split(' ')
        self.rectID = parts[0]
        xyParts = parts[2][:(len(parts[2]) - 1)].split(',')
        self.x = int(xyParts[0])
        self.y = int(xyParts[1])
        wlParts = parts[3].split('x')
        self.width = int(wlParts[0])
        self.height = int(wlParts[1])


class xLine:
    def __init__(self, x, rectID, isLeftEdge):
        self.x = x
        self.rectID = rectID
        self.isLeftEdge = isLeftEdge


class sweepLinePoint:
    def __init__(self, y, claims, pointsHere, lowerEdges=set()):
        self.y = y
        self.claims = claims
        self.pointsHere = pointsHere
        self.lowerEdges = set()
        self.rectIDs = lowerEdges

    def addClaim(self):
        self.claims += 1

    def removeClaim(self):
        self.claims -= 1

    def addPoint(self):
        self.pointsHere += 1

    def removePoint(self):
        self.pointsHere -= 1

    def addLowerEdge(self, rectID):
        self.lowerEdges.add(rectID)

    def removeLowerEdge(self, rectID):
        self.lowerEdges.discard(rectID)

    def getLenLowerEdges(self):
        return len(self.lowerEdges)

    def addRectID(self, rectID):
        self.rectIDs.add(rectID)

    def removeRectID(self, rectID):
        self.rectIDs.discard(rectID)

    def getLenRectIDs(self):
        return len(self.rectIDs)


class sweepLine:
    def __init__(self):
        self.sweepLineList = blist()
        self.yCoords = blist()
        self.heightCovered = 0

    def addOrRemoveRange(self, yRange, shouldAdd, rectID):
        startIndex = self.addOrRemovePoint(yRange[0], shouldAdd, False, rectID)
        endIndex = self.addOrRemovePoint(yRange[1], shouldAdd, True, rectID)
        prevNonEndingClaims = -1
        prevYCoord = -1
        entriesToDelete = []
        for j, slp in enumerate(self.sweepLineList[startIndex:endIndex+1]):
            if shouldAdd:
                slp.addClaim()
                slp.addRectID(rectID)
                adjustedOverlaps = slp.rectIDs.difference(slp.lowerEdges)
                if len(adjustedOverlaps) > 1:
                    for rid in adjustedOverlaps:
                        overlapsDictionary.pop(rid, None)
            else:
                slp.removeClaim()
                slp.removeRectID(rectID)
                if slp.pointsHere == 0:
                    entriesToDelete = [startIndex + j] + entriesToDelete
            if shouldAdd and ((prevNonEndingClaims == 2 and slp.claims >= 2) or (prevNonEndingClaims >= 2 and slp.claims == 2)):
                self.heightCovered += slp.y - prevYCoord
            if not shouldAdd and ((prevNonEndingClaims == 1 and slp.claims >= 1) or (prevNonEndingClaims >= 1 and slp.claims == 1)):
                self.heightCovered -= slp.y - prevYCoord
            prevNonEndingClaims = slp.claims - slp.getLenLowerEdges()
            prevYCoord = slp.y
        for toDelete in entriesToDelete:
            del self.sweepLineList[toDelete]
            del self.yCoords[toDelete]


    def addOrRemovePoint(self, point, shouldAdd, isLowerEdge, rectID):
        if not self.yCoords:
            if not shouldAdd:
                raise ValueError
            else:
                self.yCoords.append(point)
                newSLP = sweepLinePoint(point, 0, 1)
                self.sweepLineList.append(newSLP)
                return 0
        else:
            try:
                indexBefore = find_le_index(self.yCoords, point)
            except ValueError:
                indexBefore = -1
            if (not indexBefore == -1) and self.yCoords[indexBefore] == point:
                if shouldAdd:
                    self.sweepLineList[indexBefore].addPoint()
                    if isLowerEdge:
                        self.sweepLineList[indexBefore].addLowerEdge(rectID)
                else:
                    self.sweepLineList[indexBefore].removePoint()
                    if isLowerEdge:
                        self.sweepLineList[indexBefore].removeLowerEdge(rectID)
                return indexBefore
            else:
                insertAt = indexBefore + 1
                self.yCoords.insert(insertAt, point)
                if insertAt == 0 or insertAt == len(self.yCoords) - 1:
                    claims = 0
                    lowerEdges = set()
                else:
                    claims = self.sweepLineList[indexBefore].claims - self.sweepLineList[indexBefore].getLenLowerEdges()
                    lowerEdges = self.sweepLineList[indexBefore].rectIDs.difference(self.sweepLineList[indexBefore].lowerEdges)
                newSLP = sweepLinePoint(point, claims, 1, lowerEdges)
                if isLowerEdge:
                    newSLP.addLowerEdge(rectID)
                self.sweepLineList.insert(insertAt, newSLP)
                return insertAt



# ------Input------ #
answer1 = 0
answer2 = 0
contents = getContents(3, True)

rectangleStrings = contents.split("\n")

rectangles = list(map(Rectangle, rectangleStrings))

# ------Part 1 & 2------ #
rectangleDictionary = {rectObj.rectID: rectObj for rectObj in rectangles}
overlapsDictionary = {rectObj.rectID: 0 for rectObj in rectangles}
xLines = list(map(lambda rectObj: xLine(rectObj.x, rectObj.rectID, True), rectangles)) \
         + list(map(lambda rectObj: xLine(rectObj.x + rectObj.width, rectObj.rectID, False), rectangles))
xLines = sorted(xLines, key=lambda xl: (xl.x, xl.isLeftEdge, rectangleDictionary[xl.rectID].y))

sl = sweepLine()
previousX = 0
intersectionArea = 0
for i, xl in enumerate(xLines):
    intersectionArea += sl.heightCovered * (xl.x - previousX)
    currRectangle = rectangleDictionary[xl.rectID]
    yRange = (currRectangle.y, currRectangle.y + currRectangle.height)
    sl.addOrRemoveRange(yRange, xl.isLeftEdge, xl.rectID)
    previousX = xl.x

answer1 = intersectionArea
answer2 = list(overlapsDictionary)[0]

# ------Output------ #
print("Answer 1: " + str(answer1))
print("Answer 2: " + str(answer2))
