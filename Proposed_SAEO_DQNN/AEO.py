import numpy as np
import random, math
from Proposed_SAEO_DQNN import fitness


def optimize(InventaryholdingCost,Lostscale,TranshipmentCost,TransportationCost, n_V, n_r,opt_nodes,Retailers,Transport_Capacity,Time):
    t, Tmax = 0, 5  # t->initial iteration, # Tmax-> Maximum number of iteration

    N , M= n_r , n_V   # Solution Encoding

    lb, ub = 0, 1  # lower bound and upper bound
    n_clans = M
    alpha = random.uniform(0, 1)
    beta = random.uniform(0, 1)  # scale factor
    r = random.uniform(0, 1)



    def generate(n, m, l, u):  # Vulture position
        data = []
        for i in range(n):
            tem = []
            for j in range(m):
                tem.append(random.uniform(l, u))
            data.append(tem)
        return data


    def find_center(Pos):
        S = []
        s = 0
        for i in range(len(Pos)):
            for j in range(len(Pos[i])):
                s += Pos[i][j]
            S.append(s)
        S = np.asarray(S)
        c = (1 / n_clans) * S
        return c

    Position = generate(N,M,lb,ub)
    best_soln = np.zeros([4, 1], dtype=float)  # initializing the best soln as zero 4X1 matrix
    fit,TranshipCost,TotalCost,TransportCost= fitness.func(Position, opt_nodes,InventaryholdingCost,Lostscale,TranshipmentCost,TransportationCost,Retailers,Transport_Capacity,Time,n_V)
    nXL = np.argmin(fit)

    best_soln = Position[nXL]  # best solution
    best_fit = np.max(fit)
    x_max = random.uniform(0, 1)
    x_min = random.uniform(0, 1)
    worst_pos = random.randint(1, M)
    n = 2
    SD_init, SD_fin = 0.5, 0.001  # SD initial and SD final
    mu = random.uniform(0, 4)
    z = random.uniform(0, 1)
    zt = mu * z * (1 - z)  # chaotic mapping
    C = random.uniform(0,1)
    rand = random.uniform(0,1)
    C3 = random.uniform(0,1)
    Temparature=180
    while t < Tmax:
        n_Position = []
        sigma = ((Tmax - t) / (Tmax)) ** n * (SD_init - SD_fin) + (SD_fin * zt)
        pvX_1,pvX_2 = [[0] * N]*M,[[0] * N]*M
        pvx_f1,pvx_f2 = 0,0
        for i in range(N):
            for j in range(M):
                if (i > 0):
                    pvX_2 = pvX_1.copy()  # Xi(t-2)
                    pvx_f2 = pvx_f1
                if (i > 0):
                    pvX_1 = Position.copy()  # Xi(t-1)
                    pvx_f1 = best_fit
                # Proposed_SAEO_DQNN AEO updated equation

                new_pos=(pvx_f1*(1+C3*Temparature*rand)*(1+C)-1*C*pvx_f1*(C3*Temparature*rand))/(C3*Temparature*rand+C+1) #
                if Position[i][j] == best_fit:
                    c = find_center(Position)
                    new_pos = (beta * c).tolist()
            n_Position.append(new_pos)
        #n_Position = bound(n_Position)
        for i in range(N):
            worst_pos = int(x_min + (x_max - x_min + 1) * r)



        fit,TranshipCost,TotalCost,TransportCost = fitness.func(n_Position, opt_nodes,InventaryholdingCost,Lostscale,TranshipmentCost,TransportationCost,Retailers,Transport_Capacity,Time,n_V)

        new_fit = fit.copy()
        NF = np.argmin(new_fit)
        nXL = np.argmax(new_fit)
        if (np.max(new_fit) > best_fit):  # comparing maximum of new_fit and fit
            XL = n_Position[NF]  # assigning XL value as the row value of NF
            best_fit = np.max(new_fit)
        t = t + 1

    return best_soln,TranshipCost,TotalCost,TransportCost
