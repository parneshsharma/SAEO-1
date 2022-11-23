import Routing
import pandas as pd
import numpy as np

def callmain(Dataset,Vehicles):

    Data=pd.read_csv("Dataset\\Results_"+Dataset+".csv")
    Data=np.array(Data)
    Retailers,N_R = Data[:, 0] ,5   #Retailers

    Time = Data[:, 1]                #Time Period
    Transportation_Capacity = Data[:, 2]   # Transportation Capacity

    TotalCost, TransportCost, TranshipCost, sr = Routing.phase(Vehicles,Retailers,Transportation_Capacity,Time,N_R) #

    return TransportCost,TotalCost,  TranshipCost, sr

