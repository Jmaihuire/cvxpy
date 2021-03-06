"""
Copyright 2013 Steven Diamond

This file is part of CVXPY.

CVXPY is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CVXPY is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CVXPY.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import division
import sys

import cvxopt
import numpy as np
from pylab import *
import math

from cvxpy import *

from multiprocessing import Pool

# Taken from CVX website http://cvxr.com/cvx/examples/
# Exercise 5.1d: Sensitivity analysis for a simple QCQP
# Ported from cvx matlab to cvxpy by Misrab Faizullah-Khan
# Original comments below

# Boyd & Vandenberghe, "Convex Optimization"
# Joelle Skaf - 08/29/05
# (a figure is generated)
#
# Let p_star(u) denote the optimal value of:
#           minimize    x^2 + 1
#               s.t.    (x-2)(x-2)<=u
# Finds p_star(u) and plots it versus u

u = Parameter()
x = Variable()

objective = Minimize( quad_form(x,1) + 1 )
constraint = [ quad_form(x,1) - 6*x + 8 <= u ]
p = Problem(objective, constraint)

# Assign a value to gamma and find the optimal x.
def get_x(u_value):
    u.value = u_value
    result = p.solve()
    return x.value

u_values = np.linspace(-0.9,10,num=50);
# Serial computation.
x_values = [get_x(value) for value in u_values]

# Parallel computation.
pool = Pool(processes = 4)
x_values = pool.map(get_x, u_values)

# Plot the tradeoff curve
plot(u_values, x_values)
# label
title('Sensitivity Analysis: p*(u) vs u')
xlabel('u')
ylabel('p*(u)')
axis([-2, 10, -1, 3])
show()
