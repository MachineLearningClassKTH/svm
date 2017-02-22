import random, math, csv

## generate training data
def makeData(N):
    intA = int(round(N/4))
    intB = int(round(N/2))
    classA = [(random.normalvariate(-1.5, 1),
               random.normalvariate(0.5, 1),
               1)
               for i in range(intA)] + \
            [(random.normalvariate(1.5, 1),
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


# def anonfunc((A,B)):
#
#
# def readData(File):
#     list = []
#     with open(File) as csvfile:
#         reader = csv.reader(csvfile, delimiter=',', quotechar='|')
#         list = [tuple(row) for row in reader]
#     list = map()
#     print(list)
#     return
#
#
# def writeData(File, Data):
#     with open(File, 'w') as csvfile:
#         writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#         for item in Data:
#             writer.writerow(item)
#     return
