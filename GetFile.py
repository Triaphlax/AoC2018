import os

# Get the contents of the file
dirname = os.path.dirname('..\\Input\\')
testDelimiter = '+++++'


def getContents(problem, realRun):
    contents = open(os.path.join(dirname,
                              'Input' + str(problem).zfill(2) + ('' if realRun else '_Test') + '.txt'), 'r').read()
    sanitizedInput = contents.strip()
    delimiterIndex = sanitizedInput.find('+++++')
    if delimiterIndex == -1:
        return contents
    else:
        return contents[:delimiterIndex - 1]