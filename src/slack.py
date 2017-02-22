from cvxopt.solvers import qp
from cvxopt.base import matrix
import numpy, pylab, random, math
from datetime import datetime
from makeData import *
#matrix is a function which takes anything that can be interpreted as a matrix, and converts it into a cvxopt matrix which can be passed as a parameter to qp

# Generate a P matrix
def generateP(data, N):
    p = numpy.zeros((N, N))
    for i in range(N):
        for j in range(N):
            p[i][j] = data[i][2] * data[j][2] * kernel(data[i][0:2], data[j][0:2])
    return p

def constructQ(N):
    q = numpy.zeros(N)
    for i in range(N):
        q[i] = -1
    return q

def constructH(N,C):
    h = numpy.zeros(N)
    slack = numpy.full(N,C)

    h = numpy.append(h, slack)
    return h

def constructG(N):
    G = numpy.zeros((N, N))
    numpy.fill_diagonal(G, -1)
    slack  = numpy.zeros((N, N))
    numpy.fill_diagonal(slack, 1)
    G = numpy.append(G, slack, axis=0)
    return G


#kernel function
def kernel(x_vec, y_vec):
    #return linearKernel(x_vec, y_vec)
    return polynomialKernel(x_vec, y_vec)
    #return radialBasis(x_vec, y_vec)


def linearKernel(x_vec, y_vec):
    # return x * y + 1
    return numpy.dot(x_vec, y_vec) + 1

def polynomialKernel(x_vec, y_vec):
    # return (x * y + 1)^p
    return (numpy.dot(x_vec, y_vec) + 1) **5

def radialBasis(x_vec, y_vec):
    # return e^((x-y)^2)/(2*sigma^2))
    sigma = 20
    vec_diff = numpy.subtract(x_vec, y_vec)
    return math.exp(-numpy.dot(vec_diff, vec_diff) / (2 * sigma**2))


N = 20
C = 100000000

## generate training data from makeData file
classA, classB, data = makeData(N)
P = generateP(data, N)
q = constructQ(N)
h = constructH(N,C)
G = constructG(N)
r = qp(matrix(P), matrix(q), matrix(G), matrix(h))
print(r)
alpha = list(r["x"])
optData = []
optAlpha = []
for i in range(N):
    if (alpha[i] > 10**(-5)):
        optAlpha.append(alpha[i])
        optData.append(data[i])


def indicator(x, y):
    result = 0
    newData = (x, y)
    for i in range(len(optAlpha)):
        result += optAlpha[i] * optData[i][2] * kernel(newData, optData[i][0:2])
    return result


pylab.figure()
pylab.hold(True)
pylab.plot([p[0] for p in classA],
            [p[1] for p in classA],
            "bo")
pylab.plot([p[0] for p in classB],
         [p[1] for p in classB],
           "ro")


xrange = numpy.arange(-4, 4, 0.05)
yrange = numpy.arange(-4, 4, 0.05)
grid = matrix([[indicator(x, y)
      for y in yrange ]
      for x in xrange])
pylab.contour(xrange, yrange, grid, (-1.0, 0, 1.0), colors=("red", "black", "blue"), linewidths=(1, 3, 1))
pylab.title('C = ' + str(C))
pylab.savefig("../newplots/{}.png".format(datetime.now().strftime('%s')))
#pylab.show()
