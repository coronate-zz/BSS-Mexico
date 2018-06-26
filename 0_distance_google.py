"""
Se explora la libreria de googlemaps usando los API de Google.
https://github.com/googlemaps/google-maps-services-python

TO DO:  Agregar feature for walking time 
MODE = WALKING, la desicion de consumo cambia dependiendo de la distancia en carro y la distancia caminando 
transit_routing_preference: LESS WALKING, asumimos que la gente es floja
results =gmaps.distance_matrix( origins =  originCordenadas , destinations =  destinationsCordenadas, mode = "walking", transit_routing_preference= "less_walking" )

"""
import googlemaps
import pandas as pd
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyDnT4Mu6Pf9gi2ZbWkBOLTbzJPo8njqAeA')
gmaps = googlemaps.Client(key='AIzaSyAFwWe_JFT7NDbW280Wrm8z1PjVtMYdYlQ')


dataCordenadas = pd.read_csv("coordenadas.csv", encoding='utf-16')
dataCordenadas = dataCordenadas.reset_index()
dataCordenadas = dataCordenadas[["ID", "Latitud", "Longitud"]]
dataCordenadas["Latitud"] = dataCordenadas["Latitud"].apply(str)
dataCordenadas["Longitud"] = dataCordenadas["Longitud"].apply(str)
dataCordenadas["cordenadas"] = dataCordenadas[['Latitud', 'Longitud']].apply(lambda x: ' , '.join(x), axis=1)

#dataDistaces = pd.DataFrame( index=dataCordenadas["ID"] , columns= dataCordenadas["ID"])
#dataDuration = pd.DataFrame( index=dataCordenadas["ID"] , columns= dataCordenadas["ID"])
#dataStatus   = pd.DataFrame( index=dataCordenadas["ID"] , columns= dataCordenadas["ID"])

dataStatus   = pd.read_csv( "dataStatus.csv")
dataDuration = pd.read_csv( "dataDuration.csv")
dataDistaces = pd.read_csv( "dataDistaces.csv")

#dataStatus   = pd.DataFrame( columns = dataCordenadas.ID , index = dataCordenadas.ID)
#dataDuration = pd.DataFrame( columns = dataCordenadas.ID , index = dataCordenadas.ID)
#dataDistaces = pd.DataFrame( columns = dataCordenadas.ID , index = dataCordenadas.ID)

#dataDistaces_directions = pd.DataFrame( index=results["origin_addresses"] , columns= dataCordenadas["origin_addresses"])
#dataDuration_directions = pd.DataFrame( index=results["origin_addresses"] , columns= dataCordenadas["origin_addresses"])
#dataStatus_directions   = pd.DataFrame( index=results["origin_addresses"] , columns= dataCordenadas["origin_addresses"])

#Como el API no puede descargar mas de cierta cantidad de direcciones al mismo tiempo vamos a limitar el
#numero de solicitudes de 100 en 100 
totalFilas = len(dataCordenadas["ID"])
totalColumnas = totalFilas 
filaProcesando = 0

while filaProcesando < totalFilas:
	print( "PROCESANDO FILA " + str( filaProcesando))
	missingDestinations = True
	#COORDENADA DEL LUGAR DE ORIGEN
	originCordenadas = dataCordenadas.cordenadas[filaProcesando] 
	columnasProcesando_start = 0
	columnasProcesando = 0 

	while columnasProcesando < totalColumnas:
		#PROCESAMOS DE 100 en 100 para cada lugar de origen
		columnasProcesando_end = columnasProcesando_start + 100
		if columnasProcesando_end > totalColumnas:
			columnasProcesando_end = totalColumnas 

		#CORDENADAS DE LOS 100 LUGARES DE DESTINO
		print( "\n\n\tPROCESANDO DE LA COLUMNA " + str( columnasProcesando_start) +" A LA " + str(columnasProcesando_end))

		destinationsCordenadas = dataCordenadas.cordenadas[ columnasProcesando_start : columnasProcesando_end]
		destinationsID = dataCordenadas.ID[ columnasProcesando_start : columnasProcesando_end]

		#print( "\n\t---------EJECUCION API GOOGLE MAPS-----------------") 
		results =gmaps.distance_matrix( origins =  originCordenadas , destinations =  destinationsCordenadas, mode = "driving")
		#gmaps.distance_matrix( origin =  origin , destinations =  destinations, mode = "driving",  traffic_model = "optimistic")
		#gmaps.distance_matrix( origin =  origin , destinations =  destinations, mode = "driving",  traffic_model = "pessimistic")

		idOrigin = dataCordenadas.loc[ filaProcesando]["ID"]
		j = 0
		i = 0 #DADO QUE SOLO TENEMOS UN ORIGIN

		for destination in results["destination_addresses"]: 
			
			#print( "\tDestintion: {}".format( destination ))
			#VALORES ARROJADOS DEL RECORRIDO DE i HASTA  j
			idDestination  = dataCordenadas.loc[j + columnasProcesando_start]["ID"]
			distance     = results["rows"][i]["elements"][j]["distance"]["value"] #reportado en metros
			duration = results["rows"][i]["elements"][j]["duration"]["value"] #reportado en segundos
			status  = results["rows"][i]["elements"][j]["status"]
			#print( "\t\tStatus: {}".format( status))
			#print( "\t\tDuration: {}".format( duration))
			#print( "\t\tDistance: {}".format( distance ))

			dataStatus.loc[ idOrigin, idDestination]   = status
			dataDuration.loc[ idOrigin, idDestination] = duration
			dataDistaces.loc[ idOrigin, idDestination] = distance
			j+=1

		#para la siguiente iteracion movemos la cabeza a la cola 
		columnasProcesando_start = columnasProcesando_end
		columnasProcesando += 100

	#END WHILE
	filaProcesando +=1
	dataStatus.to_csv  ( "dataStatus.csv")
	dataDuration.to_csv( "dataDuration.csv")
	dataDistaces.to_csv( "dataDistaces.csv")





