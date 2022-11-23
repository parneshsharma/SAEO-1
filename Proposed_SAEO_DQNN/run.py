import numpy, random
from Proposed_SAEO_DQNN import AEO

#Calculating Inventory Holding Cost
def Inv_holdCost(Inventary_HoldingTime,UnitInventary):
    a=3000+random.random()
    THPI,T=[],numpy.square(a) #Normalized Feactor
    for i in range(len(Inventary_HoldingTime)):
        Hpi=Inventary_HoldingTime[i]*UnitInventary[i]
        Total_Cost = numpy.sum(Hpi)
        THPI.append(Total_Cost/T)
    return THPI

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
#    retailers = retailers.tolist()
    trans=random.random()
    for i in range(len(retailers)):

        TransCost = Distance_Cal(retailers,Inventory)
        TransCost= TransCost+trans
        TRANSPORT_COST.append(TransCost)

    return TRANSPORT_COST
def func(Transport_Capacity,Retailers,Time,n_V,TransportationCost,bs,x_value,y_value,TranshipmentCost,TotalCost,n_r,simulation_result,i,col_n,data_packet,xt,xr):


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

    # distance between nodes
    def distance(p1, p2):
        dist = numpy.sqrt((numpy.square(x_value[p2] - x_value[p1])) + (numpy.square(y_value[p2] - y_value[p1])))
        return dist
        # Path detection
    def detection(opt_nodes, base, n_c,InventaryholdingCost,Lostscale,TranshipmentCost,TransportationCost, n_V,Retailers,Transport_Capacity,Time):

        pth = []
        pth.append(0)  # source
        if (n_c > len(opt_nodes)): n_c = len(opt_nodes)  # non dead Vehicles

        # Path detection by Proposed AEO
        opt_path, TranshipCost, TotalCost, TransportCost = AEO.optimize(InventaryholdingCost,Lostscale,TranshipmentCost,TransportationCost, n_V, n_r,opt_nodes,Retailers,Transport_Capacity,Time)
        for op in range(len(opt_path)):
            pth.append(opt_path[op])

        pth.append(base)  # destination

        pth = numpy.unique(pth)
        pth.sort()
        return  pth.tolist()

    # calculate Vehicle energy
    def calc_vehicle_en(np, prev_en, x_t, x_r):

        en = prev_en.copy()  # copy of previous round energy
        m, n = 0.0006, 1000  # normalizing factor

        # energy drop for all vehicle
        for ed in range(len(np) - 1):
            y = data_packet[int(np[ed])]  # no. of transmitted bits
            if ed == 0:  # source vehicle
                if en[int(np[ed])] > 0:
                    dt = distance(np[ed], np[ed + 1]) / n  # distance to send the data
                    E = en[np[ed]] - (x_t * y) * dt  # only send the data to head
                    if E > 0:
                        en[np[ed]] = E
                    else:
                        en[np[ed]] = 0
                else:
                    en[int(np[ed])] = 0

            else:  # other nodes in path
                if np[ed] > 0:  # if 0 then no path
                    if en[int(np[ed])] > 0:
                        dt, dr = distance(np[ed], np[ed + 1]) / n, distance(np[ed], np[
                            ed - 1]) / n  # distance to send & receive the data
                        E = en[np[ed]] - (x_r * y) * dr - (x_t * y) * dt  # receive & send
                        if E > 0:
                            en[np[ed]] = E
                        else:
                            en[np[ed]] = 0
                    else:
                        en[int(np[ed])] = 0
        return en

     # Vehicle other than dead nodes

    def get_active_Vehicle(en):
        opt_n = []
        for o in range(len(en)):
            if (o > 0) and (en[o] > 0):  # Vehicle with energy(not the dead Vehicle)
                opt_n.append(o)  # Vehicle other than source & destination
        return opt_n
    # get non dead nodes
    opt_n = get_active_Vehicle(TransportationCost)
    opt_nodes, error = cal_error(opt_n)  # error of sensor Vehicle, and finding the sleep Vehicle

    TranshipmentCost = Transhipment_Cost(n_V, Transport_Capacity)  # energy of nodes after the transmission

    InventaryholdingCost=Inv_holdCost(Time,Transport_Capacity)

    Lostscale=LostSale(Transport_Capacity)

    TransportationCost=Transportation_Cost(Retailers,Transport_Capacity)

    Retailers,round_TranshipCost,round_TotalCost,round_TransportCost=AEO.optimize(InventaryholdingCost,Lostscale,TranshipmentCost,TransportationCost, n_V, n_r,opt_nodes,Retailers,Transport_Capacity,Time)

    #result for simulation
    path = detection(opt_n, bs, n_r,InventaryholdingCost,Lostscale,TranshipmentCost,TransportationCost, n_V,Retailers,Transport_Capacity,Time)
    round_energy = calc_vehicle_en(path, TotalCost, xt, xr)  # energy of Vehicle after the transmission


    dead_vehicle = []  # Vehicle with no energy
    for j in range(len(round_energy)):
        if (round_energy[j] == 0):
            dead_vehicle.append(j)

    simulation_result.append(x_value)  # nodes x-axis value
    simulation_result.append(y_value)  # nodes y-axis value
    simulation_result.append(n_V)
    simulation_result.append(i)  # no. of iteration
    simulation_result.append(bs)  # Base station
    simulation_result.append(col_n)  # no. of grid columns in simulation window
    simulation_result.append(n_r)
    simulation_result.append(dead_vehicle)  #Vehicle with Zero energy
    simulation_result.append(path)

    return round_TransportCost,round_TotalCost,round_TranshipCost
