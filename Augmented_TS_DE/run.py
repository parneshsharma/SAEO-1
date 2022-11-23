import numpy, random
from Augmented_TS_DE import optimization

#Calculating Inventory Holding Cost
def Inv_holdCost(Inventary_HoldingTime,UnitInventary):
    HPI=[]
    for i in range(len(Inventary_HoldingTime)):
        Hpi=Inventary_HoldingTime[i]*UnitInventary[i]
        HPI.append(Hpi)
    return HPI

# Calculating Transhipment Cost
def Transhipment_Cost(N_V,TransporationCapacity):
    Vehicle=[]
    for n_V in range(N_V):
        Vehicle.append(random.uniform(1,n_V))

    TC=numpy.sum(Vehicle)/TransporationCapacity

    return TC

#Calculating Lost Scale (Lp it)

def LostSale(UnitInventory):
    LOST_SALE=[]
    SALES_Exp,SALES_Done=[],[]
    for i in range(len(UnitInventory)):
        Sales_Exp=UnitInventory[i]*max(UnitInventory)   #Sales Expected
        SALES_Exp.append(Sales_Exp)
        Sales_Done= (max(UnitInventory)-i) *UnitInventory[i]
        SALES_Done.append(Sales_Done)
    for j in range(len(SALES_Exp)):
        Lostsales= SALES_Exp[j] - SALES_Done[j]
        LOST_SALE.append(Lostsales)

    return LOST_SALE

def Distance_Cal(list1, list2):  #Distance Calculation betweenn retailer and Inventory
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union



#Calculating Transportation Cost

def Transportation_Cost(retailers,Inventory):
    TRANSPORT_COST=[]
    retailers = retailers.tolist()
    trans=random.random()
    for i in range(len(retailers)):

        TransCost = Distance_Cal(retailers,Inventory)
        TransCost= TransCost+trans
        TRANSPORT_COST.append(TransCost)

    return TRANSPORT_COST
def func(Transport_Capacity,Retailers,Time,n_V,TransportationCost,bs,x_value,y_value,TranshipmentCost,TotalCost,n_r,i,col_n):


    def normal_dis(Vehicle): # normal distribution
        mu, sigma = 0.5, 0.1
        norm = numpy.random.normal(mu, sigma,Vehicle)
        return norm

    def count(n): # error count
        c = 0
        for i in range(len(n)):
            if n[i] < 0.4:
                c += 1
        return c
    def cal_error(opt_vehicle):
        err = [] # error of sensor nodes
        for i in range(n_V):
            norm = normal_dis(n_V)
            error = (count(norm) / (n_V + count(norm)))
            err.append(error)
        T = 0.3 # threshold
        for i in range(len(err)):
            if err[i] > T: # if error of Vehicle is high then it is in sleep mode and will not involve in txn
                print("error")
                opt_vehicle.remove(i)
        return opt_vehicle,err

     # Vehicle other than dead nodes

    def get_active_nodes(en):
        opt_n = []
        for o in range(len(en)):
            if (o > 0) and (en[o] > 0):  # Vehicle with energy(not the dead node)
                opt_n.append(o)  # nodes other than source & destination
        return opt_n
    # get non dead nodes
    opt_n = get_active_nodes(TransportationCost)
    opt_nodes, error = cal_error(opt_n)  # error of sensor Vehicle, and finding the sleep Vehicle


    TranshipmentCost = Transhipment_Cost(n_V, Transport_Capacity)  # energy of nodes after the transmission

    InventaryholdingCost=Inv_holdCost(Time,Transport_Capacity)

    Lostscale=LostSale(Transport_Capacity)

    TransportationCost=Transportation_Cost(Retailers,Transport_Capacity)

    Retailers,round_TranshipCost,round_TotalCost,round_TransportCost=optimization.algm(InventaryholdingCost,Lostscale,TranshipmentCost,TransportationCost, n_V, n_r,opt_nodes,Retailers,Transport_Capacity,Time)

    return round_TransportCost,round_TotalCost,round_TranshipCost
