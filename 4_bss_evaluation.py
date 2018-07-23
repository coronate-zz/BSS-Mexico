"""
In this section we use the bicycles routes database that contains the routes performed
by each bike thorough the day. The basic structure of the database is:
    
    BIKE ID || DATE( DAY, HOUR, MINUTES) ||  STATION ||  ARRIVE/LEFT 

We can use this iformation to test the solutions of the BSSDynamic. Mainly, this information 
will help us to identify how good is our model vs the current implemented model.

This is the description of the process to use the solution:

INITIAL STATE:
    All the vehicles are allocated in their initial position V_0. 
    Given this initial position all the vehicles at the same time will
    start to solve the dynamic system for bike reallocation.
        Each vehicle will have it's own cost matrix that tell us how expensive is for this particular
        vehicle to travel from station V_0 to station A:
            This function take into acount:
                 The traveling time from point V_0 -> A_i.
                 The number of available bicycles in station A_i.
                     The expected demand of bicycles in station A at T:= t_0 + t(V_0 -> A_i)
                     ***TO DO: This function must be a conditional poisson(Mu,Var) | Weekday, Hour.
                 The number of available parking spots in station A.
                     The expected demand of parking spots in station A at T:= t_0 + t(V_0 -> A_i)
            ***TO DO: Write this function.

    2. After solving the system each vehicle will perform a movemen to next station A_v.
        Every car takes different amount of time to travel from station V_0 to station A_v.
        The next iteration for vehicle V will be at:
            T_next = t_0 + T(V_0) + T_rebalancing(A) i.e 
            Is the time of car V to travel from it's starting point to the next station and perform
            a rebalance of the station.

    3. The numer of bicycles and available spots that a vehicle assigns to a particular station
    must be optimal.
        3.1 Initially leaving the station with an equal number of spots and bicycles was sugested.
        3.2 Other approach is to calculate the number of bicycles that will arrive in the next X
        minutes (Where X is the expected time until the same station will be visited again)

    4. Eventually some car will need to perform a new rebalance at a different station B. 
    When this happens T >< t_0 so we need to update the matrix cost for this vehicle because 
    while the vehicle was travel and making the rebalance other bicycles arrive and leave different
    stations.
        The car update the MAP parking_bicycles_spots matrix for all the available stations.
            The available stations are all the stations that are not being occupied by any car.
            ***TO DO: After solving the dynamic system we need to take out all the bicycles in the
            solution of car X from the unavailable list of MAP.
        While a car is performing a rebalance in a given station until it leaves we will assuma that 
        the numer of available spots and bicycles stay at the optimum level.

    5. Using the updated matrix we can now solve the dynamic rebalancing problem for the available vechicle. 

    6. While the time passes new vechicles will become available and the will upadate the MAP in order to 
    find the next station to be rebalance.

['Unnamed: 0', 'Edad_Usuario', 'Bici', 'Ciclo_Estacion_Retiro',
       'date_removed', 'Hora_Retiro', 'Ciclo_Estacion_Arribo', 'Fecha_Arribo',
       'Hora_Arribo']


"""

from utils_xgboost import get_complete_dates, label_timeblocks,\
                           feature_engineering
import pandas as pd
import numpy as np 
import datetime

df = pd.read_csv("Datos/dataRecorridos.csv")

#df = df.sample(100)
#df = pd.read_csv("sample.csv")
#test_dates = ['01/01/2018', '02/01/2018', 
#              '01/01/2018']
#df = df[ df.Fecha_Arribo.apply( lambda x: x in test_dates)   ]

df = df [[ 'Bici', 'Ciclo_Estacion_Retiro',
           'Hora_Retiro', 'Ciclo_Estacion_Arribo', 
           "Fecha_Retiro" , 'Fecha_Arribo', 'Hora_Arribo']]

df["date_arrived"] = pd.to_datetime(df.Fecha_Arribo + " " + df.Hora_Arribo, format = "%Y-%m-%d %H:%M:%S")
df["date_removed"] = pd.to_datetime(df.Fecha_Retiro + " " + df.Hora_Retiro, format = "%Y-%m-%d %H:%M:%S")

df["tiempo_traslado"] = df["date_arrived"] - df["date_removed"]
df = df[df.tiempo_traslado < datetime.timedelta(days = 1)]
df["tiempo_traslado"] = df.tiempo_traslado.apply(lambda x: x.total_seconds())
df = df[df.tiempo_traslado > 0]
del df["tiempo_traslado"]
print(df.shape) 

#df.to_csv("checkpoint.csv")
df = df.read_csv("checkpoint.csv")

#df = df.sample(100)

df["ITERATION"]       = np.nan
df["iteration_start"] = np.nan
df["iteration_end"]   = np.nan
df["day_counter"]     = np.nan

df_arrived = df [['Bici', 'Ciclo_Estacion_Arribo', "date_arrived",
           		  'Fecha_Arribo', 'Hora_Arribo', "day_counter", 
                  "ITERATION", "iteration_start", "iteration_end"]]

df_arrived = df_arrived.rename(columns = {"Ciclo_Estacion_Arribo": "Ciclo_Estacion", 
                             "date_arrived": "date" ,
                             "Hora_Arribo": "hora"})

df_removed = df[['Bici', 'Ciclo_Estacion_Retiro', "date_removed",
          		  'Fecha_Retiro', 'Hora_Retiro', "day_counter",
                  "ITERATION", "iteration_start", "iteration_end"]]

df_removed = df_removed.rename(columns = {"Ciclo_Estacion_Retiro": "Ciclo_Estacion", 
                             "date_removed": "date" ,
                             "Hora_Retiro" : "hora"})

min_date = min(df.date_arrived.min(), df.date_removed.min())
max_date = max(df.date_arrived.max(), df.date_removed.max())
    
#----------------------------------------------------------------
df_removed, df_arrived = label_timeblocks(df_removed, df_arrived, min_date, max_date)
#----------------------------------------------------------------

#-------------------------------------------------------
complete_dates = get_complete_dates(min_date, max_date)
complete_dates.to_csv("complete_dates.csv")
#-------------------------------------------------------

#-------------------------------------------------------
df_arrived = feature_engineering(df_arrived, complete_dates)
df_arrived.to_csv("df_arrived_flow.csv")
df_removed = feature_engineering(df_removed, complete_dates)
df_removed.to_csv("df_removed_flow.csv")
#-------------------------------------------------------


print("TEST removed : {}   == {} ".format( len(df_removed), len(df_removed.Ciclo_Estacion.unique())*len(complete_dates)))
print("TEST arrived : {}   == {} ".format( len(df_arrived), len(df_arrived.Ciclo_Estacion.unique())*len(complete_dates)))