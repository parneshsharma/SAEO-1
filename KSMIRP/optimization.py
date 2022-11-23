import random, numpy as np
from Proposed_SAEO_DQNN import fitness


def algm(InventaryholdingCost,Lostscale,TranshipmentCost,TransportationCost, n_V, n_r,opt_nodes,Retailers,Transport_Capacity,Time):

    N, M = n_r, n_V  # row(sheep), column(search space)
    lb, ub = 0, 1  # lower & upper bound
    g, max_itr = 0, 100  # initial value, max. of iteration
    a0, b0, bmax = 1, 1, 5  # alpha & beta value

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
    alpha, beta = a0, b0  # initial alpha & beta value

    def short_sheep(x, fit):
        fit_sort = np.sort(fit).tolist( )  # minimization
        list.reverse(fit_sort)  # maximization

        X_sorted = []  # sorted X
        for i in range(len(fit)):
            X_sorted.append(x[fit.index(fit_sort[0])])  # sorting sheep
        return X_sorted

    def calc_stepsize(X, winner):
        step_size = []
        for i in range(len(X)):
            d, j = random.randint(0, len(X) - 1), random.randint(0, len(X) - 1)  # random horse & sheep
            SS, rand = [], random.random()  # tem. list, ran[0,1]
            theta = np.random.uniform(-np.pi / 6, np.pi / 6)
            U = np.random.uniform(-1, 1)
            R1 = np.array(winner).T.reshape(len(np.array(winner).T), )
            start_position = np.array(X[0]).T.reshape(len(np.array(X[0]).T), )
            R1 = R1 - start_position
            D = np.linalg.norm(R1 - X) / np.linalg.norm(ub - lb)    # distance is a percetage of the maximum distance in the search space
            R2 = np.zeros((len(R1)))[np.random.randint(0, len(R1))] = 1
            R1 = R1.tolist()
            D = D.tolist()
            for k in range(len(X[i])):

                SS.append((1/((beta+alpha)*rand))*((((beta*X[d][k])+(alpha*X[j][k]))*rand)\
                            -((2*D*rand*R1[k])+(U*np.tan(theta)*D*R2)) * (1-(beta*rand)-(alpha*rand))))
            step_size.append(SS)
        return step_size

    def _soln(X, SS):
        temple_solution = []
        for i in range(len(X)):
            tem = []
            for j in range(len(X[i])):
                tem.append(bound(X[i][j] + SS[i][j]))  #  solution formula
            temple_solution.append(tem)
        return temple_solution

    overall_fit, overall_best = [], []  # best fitness & soln.
    data, label = [], []
    data.append(0.0)
    while g < max_itr:

        # Evaluations the Sheep (Objective function)
        Fit, TranshipCost, TotalCost, TransportCost = fitness.func(X, opt_nodes, InventaryholdingCost,Lostscale,TranshipmentCost,TransportationCost,Retailers,Transport_Capacity,Time,n_V)
        best_fit = np.max(Fit)
        if g == 0:
            overall_best.append(X[np.argmin(Fit)])

        '''# Build herds: The sheep are divided into herds
        X = short_sheep(X, Fit)

        # Calculate the step size: for each sheep - eqn (1)
        Stepsize = calc_stepsize(X, overall_best[len(overall_best) - 1])

        # Calculate the  solution vector - eqn (4)
        X_ = _soln(X, Stepsize)'''
        Fit,TranshipCost,TotalCost,TransportCost= fitness.func(X, opt_nodes, InventaryholdingCost,Lostscale,TranshipmentCost,TransportationCost,Retailers,Transport_Capacity,Time,n_V)
        _bst = np.max(Fit)

        # Update the agent and merge
        if _bst > best_fit:
            #X = X_
            overall_fit.append(_bst)
            overall_best.append(X[np.argmin(Fit)])
        else:
            overall_fit.append(best_fit)
            overall_best.append(X[np.argmin(Fit)])
        # Update the parameters - eqn (2) & (3)
        itr = g + 1  # current iteration
        alpha = a0 - ((a0 / max_itr) * (itr))  # alpha update
        beta = b0 + (((bmax - b0) / max_itr) * (itr))  # beta update
        g += 1
        return TranshipCost,TransportCost,TransportationCost