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

In standard Form:
(1) all constraints are equalities => good for expressing it as a matrix multiplication
(2) only binary variables => because my quantum variables are binary!
(3) Minimization objective => because the quantum annealer minimizes the objetive function

Constraints:
   \sum{i \in 1,...10} x_i * c_i   + s1 + 2 s2 + 4 s3 + 8 s4 + 16 s5 + 32 s6 + 64 s7<= 120
   x3 + x4 + s8 = 1
   x5 + x6 + s9 = 1
    -x3 - x4 + x5 + s10 + s11 = 0      because  -x3 - x4 + x5 <= 0
    -x3 - x4 + x6 + s12 + s13 = 0
    x1 + x2 + x7 + x8 + x9 + x10 - s14 - s15 - s16 - s17 = 2
    x1 + x2 + x7 + x8 + x9 + x10 + s18 + s19 + s20 + s21 = 4

"""

from gurobipy import *

try:
    # Create a new model
    m = Model("01-ilp-std")
    Q =  120
    P = [1,  1,  1, 1, 1, 1, 1, 1, 1, 1]
    C = [1, 1, 1, 1, 1, 1, 1, 1, 1, 3]
    X = [m.addVar(vtype=GRB.BINARY, name="x%d" % (i+1)) for i in range(len(P))]
    S = [m.addVar(vtype=GRB.BINARY, name="s%d" % (i+1)) for i in range(21)] # 21 slack variables are needed

    # Set objective
    #m.setObjective(sum(p * x for p, x in zip(P, X)), GRB.MAXIMIZE)
    m.setObjective(-sum(p * x for p, x in zip(P, X)), GRB.MINIMIZE)


    m.addConstr(sum(c*x for c,x in zip(C, X)) +
                S[0] + 2*S[1] + 4*S[2] + 8*S[3] + 16*S[4] + 32*S[5] + 64*S[6],  GRB.EQUAL, Q, "c6")

    # Add constraints
    # note index starts from 0, different than the above description

    m.addConstr(X[2] + X[3] + S[7], GRB.EQUAL, 1, "c0")
    m.addConstr(X[4] + X[5] + S[8], GRB.EQUAL, 1, "c1")
    m.addConstr(-X[2] - X[3] + X[4] + S[9] + S[10], GRB.EQUAL, 0, "c2")
    m.addConstr(-X[2] - X[3] + X[5] + S[11] + S[12], GRB.EQUAL, 0, "c3")
    m.addConstr(X[0] + X[1] + X[6] + X[7] + X[8] + X[9] - S[13] - S[14] - S[15] - S[16], GRB.EQUAL, 2, "c4")
    m.addConstr(X[0] + X[1] + X[6] + X[7] + X[8] + X[9] + S[17] + S[18] + S[19] + S[20], GRB.EQUAL, 4, "c5")

    m.optimize()

    for v in m.getVars():
        print('%s %g' % (v.varName, v.x))

    print('Obj: %g' % m.objVal)

except GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
    print('Encountered an attribute error')
