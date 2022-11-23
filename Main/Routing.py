import numpy, random
import Proposed_SAEO_DQNN.run
import Integrated_location_Inventory_routing.run
import KSMIRP.run
import Augmented_TS_DE.run
import GL_Deep_RL.run
import sys

def phase(n_V,Retailers,Transport_Capacity,Time,n_r):

    # parameter initialization

    n_Vehicle = n_V + 1  # no. of Vehicle(+base station)

    BASE_STATION = n_V - 1  # base station -- last Vehicle


    # to place Vehicle over grid
    sq = int(numpy.sqrt(n_Vehicle))  # to make the Vehicle in square grid -- take sqrt of Vehicle
    ex = n_Vehicle % sq  # excess Vehicle when make it square grid
    col_n = int((n_Vehicle - ex) / sq)  # columns for square grid
    m = []
    for i in range(col_n):
        m.append(sq)  # last column with excess Vehicle
    m.append(ex)

    # creating Vehicles
    def Vehicle_creation(x_value, y_value):
        for x in range(col_n + 1):  # x columns1
            for y in range(m[x]):  # y rows
                px = 50 + x * 60 + random.uniform(-20, 20)  # node in x-axis at px
                x_value.append(px)
                py = 50 + y * 60 + random.uniform(-20, 20)  # node in y-axis at py
                y_value.append(py)


    # initial energy generation
    def generate(v):
        data = []
        for i in range(n_V):
            data.append(v)  # initial energy of all Vehicle is 1
        return data

    # packets to be send by each vehicle
    def node_packet(nod):
        dp = []
        for i in range(n_V):
            tem = []
            for j in range(nod):
                tem.append(random.randint(1, 10))
            dp.append(tem)
        return dp

    datapacket=node_packet(n_V)
    Xt, Xr = 0.0035, 0.0035  # energy required to send, receive data
    print("\nSystem model..")


    Final_TotalCost, Final_TransportCost, Final_TranshipCost,Final_loss = [], [], [] ,[]      # Final Cost,... of the Vehicle after all rounds
    Overall_Cost, Overall_Transportcost, Overall_Transhipmentcost,Overall_loss = [], [], [],[] # each round Cost,... of all methods

    ################################################## Proposed_SAEO_DQNN #############################################

    TotalCost, TransportationCost, TranshipmentCost = [], [], []

    TotalCost_Avg, TransportationCost_Avg, TranshipmentCost_Avg,LostScale_Avg  = [], [], [], []
    print("\t>> Energy model..")
    TotalCost.append(generate(0))
    TransportationCost.append(generate(1))
    TranshipmentCost.append(generate(0))

    sr = []

    for i in range(n_V):

        x_value, y_value = [], []  # x & y value of each node

        Vehicle_creation(x_value, y_value)

        round_TransportCost, round_TotalCost, round_TranshipCost = Proposed_SAEO_DQNN.run.func(Transport_Capacity, Retailers, Time, n_V, TransportationCost[i], BASE_STATION, x_value, y_value, TranshipmentCost[i], TotalCost[i], n_r, sr, i, col_n,datapacket,Xt,Xr)

        TotalCost.append(round_TotalCost)
        TransportationCost.append(round_TransportCost)
        TranshipmentCost.append(round_TranshipCost)


        TotalCost_Avg.append(numpy.average(round_TotalCost))
        TransportationCost_Avg.append(numpy.average(round_TransportCost))
        TranshipmentCost_Avg.append(numpy.average(round_TranshipCost))

    Tc=numpy.mean(TotalCost_Avg)
    Tr_Cost =numpy.mean(TranshipmentCost_Avg)
    Trans_Cost = numpy.mean(TransportationCost_Avg)

    Overall_Cost.append(TotalCost_Avg),Overall_Transportcost.append(TransportationCost_Avg),Overall_Transhipmentcost.append(TranshipmentCost_Avg)
    Final_TotalCost.append(Tc),Final_TransportCost.append(Trans_Cost),Final_TranshipCost.append(Tr_Cost)


    #------------------Augumented TS+DE --------------------------------------------------

    TotalCost, TransportationCost, TranshipmentCost = [], [], []

    TotalCost_Avg, TransportationCost_Avg, TranshipmentCost_Avg, LostScale_Avg = [], [], [], []

    TotalCost.append(generate(0))
    TransportationCost.append(generate(1))
    TranshipmentCost.append(generate(0))



    for i in range(n_V):

        x_value, y_value = [], []  # x & y value of each node

        Vehicle_creation(x_value, y_value)

        round_TransportCost, round_TotalCost, round_TranshipCost = Augmented_TS_DE.run.func(Transport_Capacity,
                                                                                               Retailers, Time, n_V,
                                                                                               TransportationCost[i],
                                                                                               BASE_STATION, x_value,
                                                                                               y_value,
                                                                                               TranshipmentCost[i],
                                                                                               TotalCost[i], n_r,  i,
                                                                                               col_n)

        TotalCost.append(round_TotalCost)
        TransportationCost.append(round_TransportCost)
        TranshipmentCost.append(round_TranshipCost)

        TotalCost_Avg.append(numpy.average(round_TotalCost))
        TransportationCost_Avg.append(numpy.average(round_TransportCost))
        TranshipmentCost_Avg.append(numpy.average(round_TranshipCost))

    Tc = numpy.mean(TotalCost_Avg)
    Tr_Cost = numpy.mean(TranshipmentCost_Avg)
    Trans_Cost = numpy.mean(TransportationCost_Avg)

    Overall_Cost.append(TotalCost_Avg), Overall_Transportcost.append(TransportationCost_Avg), Overall_Transhipmentcost.append(TranshipmentCost_Avg)
    Final_TotalCost.append(Tc), Final_TransportCost.append(Trans_Cost), Final_TranshipCost.append(Tr_Cost)

    #-----------GL_Deep_RL----------------------------------------------
    TotalCost, TransportationCost, TranshipmentCost = [], [], []

    TotalCost_Avg, TransportationCost_Avg, TranshipmentCost_Avg, LostScale_Avg = [], [], [], []

    TotalCost.append(generate(0))
    TransportationCost.append(generate(1))
    TranshipmentCost.append(generate(0))



    for i in range(n_V):

        x_value, y_value = [], []  # x & y value of each node

        Vehicle_creation(x_value, y_value)

        round_TransportCost, round_TotalCost, round_TranshipCost = GL_Deep_RL.run.func(Transport_Capacity,
                                                                                            Retailers, Time, n_V,
                                                                                            TransportationCost[i],
                                                                                            BASE_STATION, x_value,
                                                                                            y_value,
                                                                                            TranshipmentCost[i],
                                                                                            TotalCost[i], n_r,  i,
                                                                                            col_n)

        TotalCost.append(round_TotalCost)
        TransportationCost.append(round_TransportCost)
        TranshipmentCost.append(round_TranshipCost)

        TotalCost_Avg.append(numpy.average(round_TotalCost))
        TransportationCost_Avg.append(numpy.average(round_TransportCost))
        TranshipmentCost_Avg.append(numpy.average(round_TranshipCost))

    Tc = numpy.mean(TotalCost_Avg)
    Tr_Cost = numpy.mean(TranshipmentCost_Avg)
    Trans_Cost = numpy.mean(TransportationCost_Avg)

    Overall_Cost.append(TotalCost_Avg), Overall_Transportcost.append(TransportationCost_Avg), Overall_Transhipmentcost.append(TranshipmentCost_Avg)
    Final_TotalCost.append(Tc), Final_TransportCost.append(Trans_Cost), Final_TranshipCost.append(Tr_Cost)


    #--------------Integrated location Inventory Routing ----------------------

    TotalCost, TransportationCost, TranshipmentCost = [], [], []

    TotalCost_Avg, TransportationCost_Avg, TranshipmentCost_Avg, LostScale_Avg = [], [], [], []

    TotalCost.append(generate(0))
    TransportationCost.append(generate(1))
    TranshipmentCost.append(generate(0))



    for i in range(n_V):

        x_value, y_value = [], []  # x & y value of each node

        Vehicle_creation(x_value, y_value)

        round_TransportCost, round_TotalCost, round_TranshipCost = Integrated_location_Inventory_routing.run.func(Transport_Capacity,
                                                                                       Retailers, Time, n_V,
                                                                                       TransportationCost[i],
                                                                                       BASE_STATION, x_value,
                                                                                       y_value,
                                                                                       TranshipmentCost[i],
                                                                                       TotalCost[i], n_r,  i,
                                                                                       col_n)

        TotalCost.append(round_TotalCost)
        TransportationCost.append(round_TransportCost)
        TranshipmentCost.append(round_TranshipCost)

        TotalCost_Avg.append(numpy.average(round_TotalCost))
        TransportationCost_Avg.append(numpy.average(round_TransportCost))
        TranshipmentCost_Avg.append(numpy.average(round_TranshipCost))

    Tc = numpy.mean(TotalCost_Avg)
    Tr_Cost = numpy.mean(TranshipmentCost_Avg)
    Trans_Cost = numpy.mean(TransportationCost_Avg)

    Overall_Cost.append(TotalCost_Avg), Overall_Transportcost.append(TransportationCost_Avg), Overall_Transhipmentcost.append(TranshipmentCost_Avg)
    Final_TotalCost.append(Tc), Final_TransportCost.append(Trans_Cost), Final_TranshipCost.append(Tr_Cost)

    #-----------------------KSMIRP------------------------------------------------
    TotalCost, TransportationCost, TranshipmentCost = [], [], []

    TotalCost_Avg, TransportationCost_Avg, TranshipmentCost_Avg, LostScale_Avg = [], [], [], []

    TotalCost.append(generate(0))
    TransportationCost.append(generate(1))
    TranshipmentCost.append(generate(0))



    for i in range(n_V):

        x_value, y_value = [], []  # x & y value of each node

        Vehicle_creation(x_value, y_value)

        round_TransportCost, round_TotalCost, round_TranshipCost = KSMIRP.run.func(Transport_Capacity,
                                                                                       Retailers, Time, n_V,
                                                                                       TransportationCost[i],
                                                                                       BASE_STATION, x_value,
                                                                                       y_value,
                                                                                       TranshipmentCost[i],
                                                                                       TotalCost[i], n_r, i,
                                                                                       col_n)

        TotalCost.append(round_TotalCost)
        TransportationCost.append(round_TransportCost)
        TranshipmentCost.append(round_TranshipCost)

        TotalCost_Avg.append(numpy.average(round_TotalCost))
        TransportationCost_Avg.append(numpy.average(round_TransportCost))
        TranshipmentCost_Avg.append(numpy.average(round_TranshipCost))

    Tc = numpy.mean(TotalCost_Avg)
    Tr_Cost = numpy.mean(TranshipmentCost_Avg)
    Trans_Cost = numpy.mean(TransportationCost_Avg)

    Overall_Cost.append(TotalCost_Avg), Overall_Transportcost.append(TransportationCost_Avg), Overall_Transhipmentcost.append(TranshipmentCost_Avg)
    Final_TotalCost.append(Tc), Final_TransportCost.append(Trans_Cost), Final_TranshipCost.append(Tr_Cost)

    Final_TotalCost.sort(reverse=True),Final_TranshipCost.sort(reverse=True),Final_TransportCost.sort(reverse=True)
    return Final_TotalCost,Final_TransportCost,Final_TranshipCost,sr
