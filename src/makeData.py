import random, math, csv

## generate training data
def makeData(N):
    intA = int(round(N/4))
    intB = int(round(N/2))
    classA = [(random.normalvariate(-1.5, 1),
               random.normalvariate(0.5, 1),
               1)
               for i in range(intA)] + \
            [(random.normalvariate(-1.5, 1),
              random.normalvariate(0.5, 1),
              1)
              for i in range(intA)]

    classB = [(random.normalvariate(0, 0.5),
                random.normalvariate(-0.5, 0.5),
                -1)
                for i in range(intB)]
    data = classA + classB
    random.shuffle(data)
    return classA, classB, data

def readData(File):
    data = 2
    return data


def writeData(File):
