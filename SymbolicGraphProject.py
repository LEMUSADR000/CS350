from pyeda.inter import *
from pyeda.boolalg.bdd import *
from graphviz import Source

def createPairs():
   for i in range(0, 32):
       for j in range(0, 32):
           if (i+3)%32 == j or (i+7)%32 == j :
               R.append((i, j))
               G.append(('{0:05b}'.format(i), '{0:05b}'.format(j)))
               expresssionList.append(getExpression(G[-1]))

def getExpression(node):
    expression = ''
    for index, i in enumerate(node[0]):
        if i == '1':
            expression += str(x[index]) + ' & '
            l = 1
        elif i == '0':
            expression += '~' + str(x[index]) + ' & '
    for index, i in enumerate(node[1]):
        if i == '1':
            expression += str(y[index]) + ' & '
        elif i == '0':
            expression += '~' + str(y[index]) + ' & '
    expression = expression[:-3]
    return expression

def createBDDR() :
    BDDR = None
    for kExp in expresssionList:
        t = expr(kExp)
        tt = expr2bdd(t)
        BDDR = BDDR | tt

    return BDDR

if __name__ == "__main__":
    R = []
    G = []
    expresssionList = []
    x = bddvars('x', 5)
    y = bddvars('y', 5)
    z = bddvars('z', 5)

    # create Graph containing binary values of paths
    # also generate expressionlist in same place in operation
    createPairs()

    # Perform BDD operations to compute the transitive closure
    BDDR = createBDDR()

    R3 = None
    # Obtain R1(x, z) and R2(z, y)
    for i in range(0, 32) :
        # Obtain R1(x, z) and R2(z, y)
        R1 = BDDR.compose({x[0]:z[0], x[1]:z[1], x[2]:z[2], x[3]:z[3], x[4]:z[4]})
        R2 = BDDR.compose({z[0]:y[0], z[1]:y[1], z[2]:y[2], z[3]:y[3], z[4]:y[4]})
        R1andR2 = R1 & R2
        R3 = R1andR2.smoothing(z)

    gv = Source(R3.to_dot())
    gv.render('test')
