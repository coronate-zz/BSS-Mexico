import pandas as pd
import numpy as np

ecoData = pd.read_csv("ecobici.csv")
ecoData = ecoData.dropna()
ecoData = ecoData.drop_duplicates()
ecoData["date_arrived"] = pd.to_datetime(ecoData["date_arrived"])
ecoData["date_removed"] = pd.to_datetime(ecoData["date_removed"])
ecoData["travel_time"]  = (ecoData["date_arrived"]  -ecoData["date_removed"] )/ np.timedelta64(1, 's')
ecoData["travel_time"]  = ecoData["travel_time"].apply(int)
ecoData["day_Month"]    = ecoData["date_arrived"].dt.day
ecoData["day_Week"]     = ecoData.date_arrived.dt.dayofweek
ecoData["year"]         = ecoData["date_arrived"].dt.year

dayOfWeek={0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
ecoData['day_Week'] = ecoData['day_Week'].map(dayOfWeek)


"""
Es necesario comprobar que la abse de datos sea congruente. 
Una manera de comprobar esto es usando el tiempo de traslado y
asegurarnos de que sean consistentes, es decir que no sean
mayores a un dia.

1760 observaciones se elimnan al aplicar este filtro
"""
print(len(ecoData))
ecoData =  ecoData[ecoData["travel_time"] < 86400]
ecoData = ecoData.dropna()
print(len(ecoData))


ecoData = ecoData[ np.abs(ecoData["travel_time"]-ecoData["travel_time"].mean() )<=(2.5*ecoData["travel_time"].std())  ]  
ecoData = ecoData.reset_index()



minute_bin = list( range( ecoData.travel_time.min()-1, \
 					ecoData.travel_time.max(), 300) )

labels_min = minute_bin.copy()
del labels_min[-1]

#De este tipo de viajes solo se registrarn 1760
ecoData["travel_label_5min"] = pd.cut(ecoData["travel_time"],\
 minute_bin, minute_bin, labels_min)

minute_bin = list( range( ecoData.travel_time.min()-1, \
 	ecoData.travel_time.max(), 1800) )
labels_min = minute_bin.copy()
del labels_min[-1]

#De este tipo de viajes solo se registrarn 1760
ecoData["travel_label_30min"] = pd.cut(ecoData["travel_time"],\
 minute_bin, minute_bin, labels_min)


ecoData.to_csv("ecoData.csv")




