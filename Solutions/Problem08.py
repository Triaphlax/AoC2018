from GetFile import getContents


# ------Classes------ #
class Node:
    def __init__(self, childNodes, metadata, value):
        self.childNodes = childNodes
        self.metadata = metadata
        self.value = value


# ------Input------ #
answer1 = 0
answer2 = 0
contents = getContents(8, True)

numberList = list(map(int, contents.split(' ')))


# ------Parts 1 & 2------ #
def makeNode():
    global sumOfMetaData

    # Determine how many child nodes and metadata points we have
    noOfChildNodes = numberList.pop(0)
    childNodes = []

    noOfMetadata = numberList.pop(0)
    metadata = []

    nodeValue = 0

    for i in range(0, noOfChildNodes):
        childNodeObj = makeNode()
        childNodes.append(childNodeObj)
    for i in range(0, noOfMetadata):
        metadataPiece = numberList.pop(0)
        sumOfMetaData += metadataPiece
        metadata.append(metadataPiece)

    if len(childNodes) == 0:
        nodeValue = sum(metadata)
    else:
        for metadataPiece in metadata:
            if metadataPiece-1 < len(childNodes):
                nodeValue += childNodes[metadataPiece-1].value

    # Finalise our node and update the dictionary
    newNodeObj = Node(childNodes, metadata, nodeValue)
    return newNodeObj


# Create the tree while solving parts 1 and 2
sumOfMetaData = 0
nodeDict = {}
rootNode = makeNode()

answer1 = sumOfMetaData
answer2 = rootNode.value

# ------Output------ #
print("Answer 1: " + str(answer1))
print("Answer 2: " + str(answer2))