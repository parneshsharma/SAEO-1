import random, numpy as np
from Proposed_SAEO_DQNN import fitness

def algm(InventaryholdingCost,Lostscale,TranshipmentCost,TransportationCost, n_V, n_r,opt_nodes,Retailers,Transport_Capacity,Time):
    N, M = n_r, n_V  # row, column
    lb, ub = 0,1   # lower & upper bound
    g, max_itr = 0, 10  # initial value, max. of iteration

    def bound(value):
        value = int(value)
        if value<lb or value>ub:
            value = random.randint(lb, ub)
        return value

    # Initial solution
    def generate_soln(n, m, Xmin, Xmax):
        data = []
        for i in range(n):
            tem = []
            for j in range(m):
                tem.append(random.randint(Xmin, Xmax))  # initial position
            data.append(tem)
        return data

    X = generate_soln(N, M, lb, ub)  # generate initial soln.


    overall_fit, overall_best = [], []  # best fitness & soln.
    while g < max_itr:

        Fit,TranshipCost, TotalCost, TransportCost = fitness.func(X, opt_nodes, InventaryholdingCost,Lostscale,TranshipmentCost,TransportationCost,Retailers,Transport_Capacity,Time,n_V)
        best_fit = np.max(Fit)
        #if g == 0: overall_best.append(X[np.argmax(Fit)])

        overall_fit.append(best_fit)
        overall_best.append(X[np.argmin(Fit)])
        X = generate_soln(N, M, lb, ub)
        g += 1
    return TranshipCost, TotalCost, TransportCost