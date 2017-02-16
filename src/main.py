from cvxopt.solvers import qp
from cvxopt.base import matrix
import numpy, pylab, random, math
#matrix is a function which takes anything that can be interpreted as a matrix, and converts it into a cvxopt matrix which can be passed as a parameter to qp

classA = [(random.normalvariate(-1.5, 1),
           random.normalvariate(0.5, 1),
           1.0)
           for i in range(5)] + \
        [(random.normalvariate(1.5, 1),
          random.normalvariate(0.5, 1),
          1.0)
          for i in range(5)]

classB = [(random.normalvariate(0.0, 0.5),
            random.normalvariate(-0.5, 0.5),
            -1.0)
            for i in range(10)]
data = classA + classB
random.shuffle(data)

pylab.hold(True)
pylab.plot([p[0] for p in classA],
            [p[1] for p in classA],
            "bo")
pylab.plot([p[0] for p in classB],
         [p[1] for p in classB],
           "ro")


# divide list into t and x vector
# make matrix p

def generateP(data, N):
    p = numpy.zeros((N, N))
    for i in range(N):
        for j in range(N):
            p[i][j] = data[i][2] * data[j][2] * kernel(data[i][0:2], data[j][0:2])
    return p


def kernel(x_vec, y_vec):
    return numpy.dot(x_vec, y_vec) + 1
        #result += x*y

def constructQ(N):
    q = numpy.zeros(N)
    for i in range(N):
        q[i] = -1
    return q

def constructH(N):
    h = numpy.zeros(N)
    return h

def constructG(N):
    G = numpy.zeros((N, N))
    numpy.fill_diagonal(G, -1)
    return G


def indicator(x, y, optData, optAlpha):
    result = 0
    newData = (x, y)
    for i in range(len(optAlpha)):
        result += optAlpha[i] * optData[i][2] * kernel(newData, data[i][0:2])
    return result
    if (result>0):
        return 1.0
    elif(result < 0):
        return -1.0
    else:
        return 0


N = 20
P = generateP(data, N)
q = constructQ(N)
h = constructH(N)
G = constructG(N)
r = qp(matrix(P), matrix(q), matrix(G), matrix(h))
alpha = list(r["x"])
optData = []
optAlpha = []
for i in range(N):
    if (alpha[i] > 10**(-5)):
        optAlpha.append(alpha[i])
        optData.append(data[i])


xrange = numpy.arange(-4, 4, 0.05)
yrange = numpy.arange(-4, 4, 0.05)
grid = matrix([[indicator(x, y, optData, optAlpha)
      for y in yrange ]
      for x in xrange])
pylab.contour(xrange, yrange, grid, levels=(-1.0, 0, 1.0), colors=("red", "black", "blue"), linewidths=(1, 3, 1))
pylab.show()
