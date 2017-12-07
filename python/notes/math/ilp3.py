#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Author : Thamme Gowda
Date   : December 6, 2017
Taken from http://people.brunel.ac.uk/~mastjjb/jeb/or/moreip.html

"""

"""
A project manager in a company is considering a portfolio of 10 large project investments. These investments differ in the estimated long-run profit (net present value) they will generate as well as in the amount of capital required.
Let Pj and Cj denote the estimated profit and capital required (both given in units of millions of £) for investment opportunity j (j=1,...,10) respectively. The total amount of capital available for these investments is Q (in units of millions of £)
Investment opportunities 3 and 4 are mutually exclusive and so are 5 and 6. Furthermore, neither 5 nor 6 can be undertaken unless either 3 or 4 is undertaken. At least two and at most four investment opportunities have to be undertaken from the set {1,2,7,8,9,10}.
The project manager wishes to select the combination of capital investments that will maximise the total estimated long-run profit subject to the restrictions described above.
Formulate this problem using an integer programming model and comment on the difficulties of solving this model.
"""
"""
Lets pick values
    P = [10, 5, 3, 2, 4, 6, 9, 5, 3, 2]
    C = [20, 40, 10, 7, 6, 9, 8, 5, 5, 4]
    Q = 120

Variables: x_i \in {0, 1} for \i= 1,2...10
Constraints:
   \sum{i \in 1,...10} x_i * c_i <= 120

   x_3 + x_4 <= 1
   x_5 + x_6 <= 1
   x_5 <= x_3 + x_4
   x_6 <= x_3 + x_4
   x_1 + x_2 + x_7 + x_8 + x_9 + x_10 >= 2
   x_1 + x_2 + x_7 + x_8 + x_9 + x_10 <= 4

Objective:
  Maximize : \sum{i \in 1...10} p_i * x_i
"""

from gurobipy import *

try:
    # Create a new model
    m = Model("01-ilp")
    Q =  120
    P = [10,  5,  3, 2, 4, 6, 9, 5, 3, 2]
    C = [20, 40, 10, 7, 6, 9, 8, 5, 5, 4]
    X = [m.addVar(vtype=GRB.BINARY, name="x%d" % (i+1)) for i in range(len(P))]
    # note index starts from 0, different than the above description


    # Set objective
    m.setObjective(sum(p * x for p, x in zip(P, X)), GRB.MAXIMIZE)

    # Add constraints
    m.addConstr(X[2] + X[3] <= 1, "c0")
    m.addConstr(X[4] + X[5] <= 1, "c1")
    m.addConstr(X[4] <= X[2] + X[3], "c2")
    m.addConstr(X[5] <= X[2] + X[3], "c3")
    m.addConstr(X[0] + X[1] + X[6] + X[7] + X[8] + X[9] >= 2, "c4")
    m.addConstr(X[0] + X[1] + X[6] + X[7] + X[8] + X[9] <= 4, "c5")
    m.addConstr(sum(c*x for c,x in zip(C, X)) <= Q, "c6")

    m.optimize()

    for v in m.getVars():
        print('%s %g' % (v.varName, v.x))

    print('Obj: %g' % m.objVal)

except GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
    print('Encountered an attribute error')
