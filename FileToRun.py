import os

# Get the contents of the file
dirname = os.path.dirname('..\\Input\\')


def getContents(problem, realRun):
    return open(os.path.join(dirname,
                              'Input' + str(problem).zfill(2) + ('' if realRun else '_Test') + '.txt'), 'r').read()