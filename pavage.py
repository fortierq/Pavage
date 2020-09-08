#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 11:27:58 2020

@author: qfortier
"""

from mip import *
import numpy as np
import matplotlib.pyplot as plt

def pl(tiles, n, p):
    m, x, w = Model(), [], []
    constraints = [[[] for j in range(p)] for i in range(n)]
    for t in range(len(tiles)):
        a, b = tiles[t].shape
        for i in range(n - a + 1):
            for j in range(p - b + 1):
                x.append(m.add_var(var_type=BINARY, name=str(t)+","+str(i)+","+str(j)))
                w.append(tiles[t].sum())
                for k, l in np.argwhere(tiles[t]):
                    constraints[i + k][j + l].append(x[-1])
    for i in range(len(constraints)):
        for j in range(len(constraints[i])):
            m += xsum(constraints[i][j]) <= 1
    m.objective = maximize(xsum(x[i]*w[i] for i in range(len(x))))
    return m
    
def solve(tiles, n, p):
    m = pl(tiles, n, p)
    sol = np.zeros((n, p))
    ntile = 0
    status = m.optimize(max_seconds=1000)
    if status == OptimizationStatus.OPTIMAL:
        for v in m.vars:
           if abs(v.x) > 1e-6: 
              t, i, j = map(int, v.name.split(","))
              ntile += 1
              for k, l in np.argwhere(tiles[t]):
                  sol[i + k, j + l] = ntile
        print("Solution optimale avec", ntile, "dominos")
        print((sol == 0).sum(), "cases ne sont pas couvertes")
    plt.imshow(sol, cmap = "gist_ncar")

L = np.full((2, 2), True)
L[1, 1] = False
I = np.full((1, 4), True)
tiles = [L, L[::-1, :], L[:, ::-1], L[::-1, ::-1]]

solve(tiles, 5, 5)