import pandas as pd
import numpy as np 
import datetime

def feature_engineering(df, complete_dates):

    df = df.groupby( ["Ciclo_Estacion", "day_counter", "ITERATION", "iteration_start", "iteration_end"])["hora"].count()
    df = df.sort_index()
    df = df.reset_index()
    df = df.rename( columns = {"hora": "flow"})

    df_append = pd.DataFrame()
    for station in df.Ciclo_Estacion.unique():
        df_station = df[df.Ciclo_Estacion == station]
        df_merge = complete_dates.merge( df_station, on= ["day_counter", "ITERATION", "iteration_start", "iteration_end"], how ="left" )
        df_merge["Ciclo_Estacion"] = station
        df_merge.loc[pd.isnull(df_merge.flow), "flow"] =0 

        if len(df_append) ==0 :
            df_append = df_merge
        else:
            df_append = df_append.append(df_merge)

    df = df_append

    #ITERATION (15 minutes) LAG VALUES
    df["flow_lag1"] = df.groupby(["Ciclo_Estacion"])["flow"].shift(1)
    df["flow_lag2"] = df.groupby(["Ciclo_Estacion"])["flow"].shift(2)
    df["flow_lag3"] = df.groupby(["Ciclo_Estacion"])["flow"].shift(3)
    df["flow_lag4"] = df.groupby(["Ciclo_Estacion"])["flow"].shift(4)
    df["flow_lag5"] = df.groupby(["Ciclo_Estacion"])["flow"].shift(5)
    df["flow_lag6"] = df.groupby(["Ciclo_Estacion"])["flow"].shift(6)
    df["flow_lag7"] = df.groupby(["Ciclo_Estacion"])["flow"].shift(7)
    df["flow_lag8"] = df.groupby(["Ciclo_Estacion"])["flow"].shift(8)

    df["flow_rollingmean_lag1_4"]  = pd.rolling_mean( df["flow_lag1"], 4)
    df["flow_rollingmean_lag1_8"]  = pd.rolling_mean( df["flow_lag1"], 8)
    df["flow_rollingmean_lag1_12"] = pd.rolling_mean( df["flow_lag1"], 12)
    df["flow_rollingmean_lag1_16"] = pd.rolling_mean( df["flow_lag1"], 16)

    df["flow_rollingmean_lag4_4"]  = pd.rolling_mean( df["flow_lag4"], 4)
    df["flow_rollingmean_lag4_8"]  = pd.rolling_mean( df["flow_lag4"], 8)
    df["flow_rollingmean_lag4_12"] = pd.rolling_mean( df["flow_lag4"], 12)
    df["flow_rollingmean_lag4_16"] = pd.rolling_mean( df["flow_lag4"], 16)

    df["flow_rollingmean_lag8_4"]  = pd.rolling_mean( df["flow_lag8"], 4)
    df["flow_rollingmean_lag8_8"]  = pd.rolling_mean( df["flow_lag8"], 8)
    df["flow_rollingmean_lag8_12"] = pd.rolling_mean( df["flow_lag8"], 12)
    df["flow_rollingmean_lag8_16"] = pd.rolling_mean( df["flow_lag8"], 16)

    df["flow_ewma_lag1_4"]  = pd.ewma( df["flow_lag1"], 4)
    df["flow_ewma_lag1_8"]  = pd.ewma( df["flow_lag1"], 8)
    df["flow_ewma_lag1_12"] = pd.ewma( df["flow_lag1"], 12)    
    df["flow_ewma_lag1_16"] = pd.ewma( df["flow_lag1"], 16)

    df["flow_ewma_lag4_4"]  = pd.ewma( df["flow_lag4"], 4)
    df["flow_ewma_lag4_8"]  = pd.ewma( df["flow_lag4"], 8)
    df["flow_ewma_lag4_12"] = pd.ewma( df["flow_lag4"], 12)    
    df["flow_ewma_lag4_16"] = pd.ewma( df["flow_lag4"], 16)

    df["flow_ewma_lag8_4"]  = pd.ewma( df["flow_lag4"], 4)
    df["flow_ewma_lag8_8"]  = pd.ewma( df["flow_lag8"], 8)
    df["flow_ewma_lag8_12"] = pd.ewma( df["flow_lag8"], 12)    
    df["flow_ewma_lag8_16"] = pd.ewma( df["flow_lag8"], 16)

    #DAYs LAG VALUES
    df["flow_lag1day"] = df.groupby(["Ciclo_Estacion"])["flow"].shift(94)
    df["flow_lag2day"] = df.groupby(["Ciclo_Estacion"])["flow"].shift(95)
    df["flow_lag3day"] = df.groupby(["Ciclo_Estacion"])["flow"].shift(96)
    df["flow_lag4day"] = df.groupby(["Ciclo_Estacion"])["flow"].shift(97)
    df["flow_lag5day"] = df.groupby(["Ciclo_Estacion"])["flow"].shift(98)
    df["flow_lag6day"] = df.groupby(["Ciclo_Estacion"])["flow"].shift(99)
    df["flow_lag7day"] = df.groupby(["Ciclo_Estacion"])["flow"].shift(100)
    df["flow_lag8day"] = df.groupby(["Ciclo_Estacion"])["flow"].shift(101)

    df["flow_rollingmean_lag1day_4"]  = pd.rolling_mean( df["flow_lag1day"], 4)
    df["flow_rollingmean_lag1day_8"]  = pd.rolling_mean( df["flow_lag1day"], 8)
    df["flow_rollingmean_lag1day_12"] = pd.rolling_mean( df["flow_lag1day"], 12)
    df["flow_rollingmean_lag1day_16"] = pd.rolling_mean( df["flow_lag1day"], 16)


    df["flow_rollingmean_lag4day_4"]  = pd.rolling_mean( df["flow_lag4day"], 4)
    df["flow_rollingmean_lag4day_8"]  = pd.rolling_mean( df["flow_lag4day"], 8)
    df["flow_rollingmean_lag4day_12"] = pd.rolling_mean( df["flow_lag4day"], 12)
    df["flow_rollingmean_lag4day_16"] = pd.rolling_mean( df["flow_lag4day"], 16)


    df["flow_rollingmean_lag8day_4"]  = pd.rolling_mean( df["flow_lag8day"], 4)
    df["flow_rollingmean_lag8day_8"]  = pd.rolling_mean( df["flow_lag8day"], 8)
    df["flow_rollingmean_lag8day_12"] = pd.rolling_mean( df["flow_lag8day"], 12)
    df["flow_rollingmean_lag8day_16"] = pd.rolling_mean( df["flow_lag8day"], 16)

    df["flow_ewma_lag1day_4"]  = pd.ewma( df["flow_lag1day"], 4)
    df["flow_ewma_lag1day_8"]  = pd.ewma( df["flow_lag1day"], 8)
    df["flow_ewma_lag1day_12"] = pd.ewma( df["flow_lag1day"], 12)    
    df["flow_ewma_lag1day_16"] = pd.ewma( df["flow_lag1day"], 16)

    df["flow_ewma_lag4day_4"]  = pd.ewma( df["flow_lag4day"], 4)
    df["flow_ewma_lag4day_8"]  = pd.ewma( df["flow_lag4day"], 8)
    df["flow_ewma_lag4day_12"] = pd.ewma( df["flow_lag4day"], 12)    
    df["flow_ewma_lag4day_16"] = pd.ewma( df["flow_lag4day"], 16)

    df["flow_ewma_lag8day_4"]  = pd.ewma( df["flow_lag8day"], 4)
    df["flow_ewma_lag8day_8"]  = pd.ewma( df["flow_lag8day"], 8)
    df["flow_ewma_lag8day_12"] = pd.ewma( df["flow_lag8day"], 12)    
    df["flow_ewma_lag8day_16"] = pd.ewma( df["flow_lag8day"], 16)

    #WEEK LAG VALUES
    df["month"]     = df.iteration_start.apply(lambda x: x.date().month)
    df["day_month"] = df.iteration_start.apply(lambda x: x.date().day)

    return df




def label_timeblocks(df_removed, df_arrived, min_date, max_date):
    #LABEL DATAFRAME
    """
    In thsi first process we take divide each day in intervals of 15minutues. 
    Then each block of 15minutes is labeled with an ID. The first day of the data set
    is assigned 0 and the next 15 minutes is assigned to 1 an so on.
    Then all the information is grouped at a block level in order to count how many bicycles
    arrived at a particular interval. 

    The number of arrived/removed bicycles is the variable that we want to predict.

    """

    iteration_number = 0 
    day_end = np.nan
    day_counter = 0

    while True:
        if iteration_number == 0:
            print("Primera Iteracion")
            iteration_start  = pd.to_datetime(min_date.date())
            iteration_end    = iteration_start + datetime.timedelta(minutes = 15)
            break_while      = pd.to_datetime(max_date.date()) + datetime.timedelta(days = 1)
            day_end          = pd.to_datetime(min_date.date()) + datetime.timedelta(days = 1)

        else:
            iteration_start  = iteration_end
            iteration_end    = iteration_start + datetime.timedelta(minutes = 15)

        if iteration_end >= day_end:
            print("\n\n\tNEW DAY: \n\t\t day_end: {} \n\t\t iteration_end: {} ".format(day_end, iteration_end))
            day_end  = pd.to_datetime(day_end) + datetime.timedelta(days = 1)
            day_counter +=1 
            iteration_number = 0 

        if iteration_end > break_while:
            print("BREAK : {} ".format(iteration_end))
            break 

        df_arrived.loc[(df_arrived.date >= iteration_start) & (df_arrived.date < iteration_end) , "ITERATION"]       = iteration_number
        df_arrived.loc[(df_arrived.date >= iteration_start) & (df_arrived.date < iteration_end) , "iteration_start"] = iteration_start
        df_arrived.loc[(df_arrived.date >= iteration_start) & (df_arrived.date < iteration_end) , "iteration_end"]   = iteration_end
        df_arrived.loc[(df_arrived.date >= iteration_start) & (df_arrived.date < iteration_end) , "day_counter"]     = day_counter

        df_removed.loc[(df_removed.date >= iteration_start) & (df_removed.date < iteration_end) , "ITERATION"]       = iteration_number
        df_removed.loc[(df_removed.date >= iteration_start) & (df_removed.date < iteration_end) , "iteration_start"] = iteration_start
        df_removed.loc[(df_removed.date >= iteration_start) & (df_removed.date < iteration_end) , "iteration_end"]   = iteration_end
        df_removed.loc[(df_removed.date >= iteration_start) & (df_removed.date < iteration_end) , "day_counter"]     = day_counter

        #print("\n\nDAY: {}  - ITERATION: {} \n\t start: {} \n\t end: {}".format(day_counter, iteration_number, iteration_start, iteration_end))
        iteration_number += 1

    return df_removed, df_arrived


def get_complete_dates(min_date, max_date):
    complete_dates = pd.DataFrame()
    iteration_number = 0 
    n_obs = 0 
    day_counter = 0
    while True:
        if iteration_number == 0:
            print("Primera Iteracion")
            iteration_start  = pd.to_datetime(min_date.date())
            iteration_end    = iteration_start + datetime.timedelta(minutes = 15)
            break_while      = pd.to_datetime(max_date.date()) + datetime.timedelta(days = 1)
            day_end          = pd.to_datetime(min_date.date()) + datetime.timedelta(days = 1)
            print("\t\tDAY: {}  - ITERATION: {} \n\t start: {} \n\t end: {}".format(day_counter, iteration_number, iteration_start, iteration_end))

        else:
            iteration_start  = iteration_end
            iteration_end    = iteration_start + datetime.timedelta(minutes = 15)

        if iteration_end >= day_end:
            #print("\n\n\tNEW DAY: \n\t\t day_end: {} \n\t\t iteration_end: {} ".format(day_end, iteration_end))
            day_end  = pd.to_datetime(day_end) + datetime.timedelta(days = 1)
            day_counter +=1 
            iteration_number = 0 

        if iteration_end > break_while:
            print("\n\nBREAK : {} ".format(iteration_end))
            print("\t\tDAY: {}  - ITERATION: {} \n\t start: {} \n\t end: {}".format(day_counter, iteration_number, iteration_start, iteration_end))
            break 

        complete_dates.loc[n_obs, "iteration_start"] = iteration_start
        complete_dates.loc[n_obs, "iteration_end"] = iteration_end
        complete_dates.loc[n_obs, "day_counter"] = day_counter
        complete_dates.loc[n_obs, "day_counter"] = day_counter            
        complete_dates.loc[n_obs, "ITERATION"]   = iteration_number
        n_obs+=1 
        iteration_number +=1
    return complete_dates



