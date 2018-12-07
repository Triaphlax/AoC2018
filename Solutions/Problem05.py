from GetFile import getContents
from blist import blist

# ------Input------ #
answer1 = 0
answer2 = 0
contents = getContents(5, True)

polymer = contents

# ------Part 1------ #
def collapsePolymer(polymerToCollapse, charToRemove):
    # Remove any leading instances of the char to remove
    while polymerToCollapse[-1].lower() == charToRemove.lower():
        del polymerToCollapse[-1]
    # Traverse the string backwards and delete any double entries.
    # Only one pass is required due to how unit deletion works here.
    for i in range(len(polymerToCollapse)-1, 0, -1):
        # In case the units we collapsed were at the end of the string
        if i > len(polymerToCollapse) - 1:
            continue
        currentUnit = polymerToCollapse[i]
        nextUnit = polymerToCollapse[i-1]
        # If we come across a forbidden char, we remove it.
        # We continue the loop and have it decrease the index 1 by
        # to continue where we left off.
        if nextUnit.lower() == charToRemove.lower():
            del polymerToCollapse[i-1]
            continue
        if currentUnit == nextUnit.swapcase():
            # Deleting the units here moves all previous units down by 2 units.
            # This means that when we decrease index i by 1 in the next step,
            # we're actually comparing the indices i+1 and i-2 from before deletion.
            del polymerToCollapse[i]
            del polymerToCollapse[i-1]
            i = min(i, len(polymerToCollapse) - 1)
    return polymerToCollapse


answer1 = len(collapsePolymer(blist(polymer), ''))

# ------Part 2------ #
# Loop through all characters in the alphabet to find out which one to remove
bestLength = len(polymer)
for charToRemove in range(ord('a'), ord('z') + 1):
    intermediateResult = len(collapsePolymer(blist(polymer), str(chr(charToRemove))))
    if intermediateResult < bestLength:
        bestLength = intermediateResult

answer2 = bestLength

# ------Output------ #
print("Answer 1: " + str(answer1))
print("Answer 2: " + str(answer2))