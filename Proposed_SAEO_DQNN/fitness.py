import  numpy as np
from Proposed_SAEO_DQNN import DQNN,run

# distance between nodes
def distance(p1, p2, x_value, y_value):
    dist = np.sqrt((np.square(x_value[p2] - x_value[p1])) + (np.square(y_value[p2] - y_value[p1])))  # distance formula
    return dist


def Distance_Cal(list1, list2):  # Distance Calculation betweenn retailer and Inventory
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union

# Cost calculation
def calc_Cost(CH, Transh_Cost, n):
    en_summ = 0
    for i in range(len(CH)):

        en_summ += Transh_Cost[int(CH[i])]
    E = 1 / (n) * en_summ
    return E



def find_error(Vehicle,err):
    Err = []
    for i in range(len(Vehicle)):
        Err.append(err[int(Vehicle[i])])
    error = np.mean(Err)
    return error

def power(Vehicle, en):
    En = []
    for i in range(Vehicle):
        En.append(en[i])
    Pm = np.mean(En)  # power -> constant between transmitter and receiver
    return Pm


def dist(Vehicle, x, y):
    D = []
    for i in range(Vehicle):
        D.append(distance(i, i + 1, x, y))  # distance between Vehicle
    Dis = np.mean(D)
    return Dis


# Transhipment calculation
def cal_TranshipmentCost(nodes_ch, n, m):
    s = 0
    for i in range(n):

        s += (len(nodes_ch[i])) / m
    Tranship = (1 / n) * s
    return Tranship

# calculation of Link quality
def Link_quality(nodes, en, x, y):
    Pm = power(nodes, en)
    D = dist(nodes, x, y)
    Lq = Pm / D
    return Lq


# fitness calculation

def func(soln, opt_nodes, InventaryholdingCost,Lostscale,TranshipmentCost,TransportationCost,Retailers,Transport_Capacity,Time,n_V):
    m = len(opt_nodes)  # Total number of nodes

    Fit = []
    Data=np.column_stack((InventaryholdingCost,Lostscale,TranshipmentCost,TransportationCost))
    Label=[]
    for i in range(len(Data[:,-2])):
        if Data[:,-2][i]<1.5 :
            Label.append(0)
        else:
            Label.append(1)

    Alpha = DQNN.qdnn_classify(Data, Label)

    for i in range(len(soln)):


        F = np.sum((InventaryholdingCost[i]+Lostscale[i]+TransportationCost[i]+TranshipmentCost[i])/4) +Alpha # fitness calculation
        Fit.append(F)
        TranshipCost = run.Transhipment_Cost(n_V, Transport_Capacity)  # Transhipment Cost of Vehicle

        TotalCost = run.Inv_holdCost(Time, Transport_Capacity)        #Total Cost of Vehicle

        TransportCost = run.Transportation_Cost(Retailers, Transport_Capacity) #Transportation Cost of Vehiucle

    return Fit,TranshipCost,TotalCost,TransportCost
