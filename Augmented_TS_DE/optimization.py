import numpy, random
from Proposed_SAEO_DQNN import fitness


def algm(InventaryholdingCost,Lostscale,TranshipmentCost,TransportationCost, n_V, n_r,opt_nodes,Retailers,Transport_Capacity,Time):

    def step_gradient(b_current, m_current, points, learningRate):
        b_gradient = 0
        m_gradient = 0
        N = float(len(points))
        ft, TranshipCost,TotalCost,TransportCost= numpy.array(fitness.func(points, opt_nodes, InventaryholdingCost,Lostscale,TranshipmentCost,TransportationCost,Retailers,Transport_Capacity,Time,n_V))
        for i in range(0, len(points)):
            x = points[i, 0]
            y = points[i, 1]
            b_gradient += -(2 / N) * (y - ((m_current * x) + b_current))
            m_gradient += -(2 / N) * x * (y - ((m_current * x) + b_current))

        new_b = b_current - (learningRate * b_gradient)
        new_m = m_current - (learningRate * m_gradient)
        return ft,TranshipCost,TotalCost,TransportCost

    def gradient_descent_runner(points, starting_b, starting_m, learning_rate, num_iterations):
        b = starting_b
        m = starting_m
        for i in range(num_iterations):
            ft,TranshipCost, TotalCost, TransportCost = step_gradient(b, m, points, learning_rate)

        return ft,TranshipCost,TotalCost,TransportCost

    def ran_Array(n, lb, ub):  # function that return random array with a bound
        rd = []
        for i in range(n):
            rd.append(int(lb - (lb - ub) * (random.random())))
        return rd

    ## Solution
    def init(n, pd, l, u):  # init the matrix problem
        x = []
        for i in range(0, n):
            x.append([])
            for j in range(0, pd):
                x[i].append(random.randint(l, u))
        return x

    def run():
        learning_rate = 0.0001
        initial_b = 0  # initial y-intercept guess
        initial_m = 0  # initial slope guess
        num_iterations = 10
        ft,TranshipCost,TotalCost,TransportCost = gradient_descent_runner(points, initial_b, initial_m, learning_rate, num_iterations)
        return ft,TranshipCost,TotalCost,TransportCost

    n = n_r
    pd = n_V
    l = 0
    u = 1
    points = numpy.array(init(n, pd, l, u))
    Fit,TranshipCost,TotalCost,TransportCost = run()
    best_solution = points[0]
    return best_solution,TranshipCost,TotalCost,TransportCost
