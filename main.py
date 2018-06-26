

"""
Este script permite generar un reporte para el centro de ventas de el globo.
Dadas los target para cada una de las categorias en cada uno de los centros de 
venta, este script evalua el total de productos vendidos para cada uno de los
categorias en todos los centros de venta y los compara con el target.

Cuando la suma de los ventas se encuentra por debajo del target entonces se
propone una nueva distribución de ventas. Esta distribución busca aumentar la
demanda de determinados productos de manera eficiete utilizando los factores 
de la empresa, los factores del producto y el target final (a un nivel de 
categoria)

El script se divide en tres partes:


"""

import pandas as pd 
import numpy as np 


def preprocessFiles():
	"""
	Esta funcion se debe correr cada vez que la tabla principal ppto2018 sea actualizada.
	Esta funcion cambia el nombre de las variables y agerga a infromacion para que el nivel
	de cada observacion sea el total de productos vendidos en una mes determinado para un
	centro de venta determinado.

	La operacion puede ser un poco tardada por lo que es mejor guardar el ppto2018_preprocessed 
	una vez que termina de realizarse la agregacion.


	"""
	df = pd.read_csv("ppto2018.csv")
	df = df[["SUCURSAL", "NOMBRE", "MES", "CATEGORIA", "CODIGO","PRODUCTO", "PZAS 2018", "PESOS 2018"]]
	df = df.rename( columns= {"PZAS 2018": "PZAS2018", "PESOS 2018": "PESOS2018"})
	df = df.groupby(["SUCURSAL", "NOMBRE", "MES", "CATEGORIA", "CODIGO", "PRODUCTO"]).sum()
	df = df.reset_index()
	df["PESOS2018"] = df.PESOS2018.str.replace( "$", "")
	df["PESOS2018"] = pd.to_numeric( df.PESOS2018.str.replace( ",", ""), errors = "corce")
	df["PESOS2018"] = df.PESOS2018.replace(np.nan,  0)
	df["PZAS2018"] = pd.to_numeric(df.PZAS2018.str.replace( "-", "0"), errors = "corce")
	df = df.dropna()
	df["SUCURSAL"] = df.SUCURSAL.apply(str)

	priceList = pd.read_csv("PriceList.csv")
	priceList = priceList[["Item ", "AMCM"]]
	priceList = priceList.rename(columns = {"Item ": "CODIGO", "AMCM":"PRECIO"})
	priceList["CODIGO"] = pd.to_numeric( priceList.CODIGO, errors= "corce")
	priceList = priceList.dropna()
	priceList["PRECIO"] = pd.to_numeric( priceList.PRECIO.str.replace( "$", ""), errors = "corce")

	presupuesto = pd.read_csv("pptoNuevo.csv")
	presupuesto = presupuesto.rename( columns = {'AreaNeg':"SUCURSAL", 
	 'Sucursal':"NOMBRE", 'Anterior':"ANTERIOR", 'Mes':"MES",  
	 'Nuevo':"NUEVO", 'Estatus':"ESTATUS"})
	presupuesto = presupuesto[["SUCURSAL", "MES", "ANTERIOR", "NUEVO", "ESTATUS"]]
	presupuesto["NUEVO"] = presupuesto.NUEVO.str.replace("$", "")
	presupuesto["NUEVO"] = pd.to_numeric( presupuesto.NUEVO.str.replace(",", ""), errors = "corce" )
	presupuesto["ANTERIOR"] = presupuesto.ANTERIOR.str.replace("$", "")
	presupuesto["ANTERIOR"] = pd.to_numeric( presupuesto.ANTERIOR.str.replace(",", ""), errors = "corce" )


	df.to_csv("ppto2018_preprocessed.csv")
	priceList.to_csv("priceList_preprocessed.csv")
	presupuesto.to_csv("presupuesto_preprocessed.csv")

#Aqui deberiamos preguntar algo asi como "Desea actualizar el archivo???"

df = pd.read_csv("ppto2018_preprocessed.csv", index_col = 0 )
priceList = pd.read_csv("priceList_preprocessed.csv", index_col = 0 )
presupuesto =  pd.read_csv("presupuesto_preprocessed.csv" , index_col = 0 )

sumapesos_categoria = df.groupby(["SUCURSAL", "MES", "CATEGORIA"])["PESOS2018"].sum()
sumapesos_categoria = sumapesos_categoria.reset_index()
sumapesos_categoria = sumapesos_categoria.rename(columns= {"PESOS2018": "PESOS2018_CAT"})

sumapesos_mes = df.groupby(["SUCURSAL", "MES"])["PESOS2018"].sum()
sumapesos_mes = sumapesos_mes.reset_index()
sumapesos_mes = sumapesos_mes.rename(columns ={"PESOS2018": "PESOS2018_MES"})

df = df.merge(priceList, on = "CODIGO", how = "left")
df["SUCURSAL"] = df.SUCURSAL.apply(str)
df = df.merge(presupuesto, on =["SUCURSAL","MES"], how = "left")
df = df.merge(sumapesos_categoria, on=["SUCURSAL", "MES", "CATEGORIA"])
df = df.merge(sumapesos_mes, on = ["SUCURSAL", "MES"])


df["PESOS2018_PCT"] = df["PESOS2018_CAT"] / df["PESOS2018_MES"]

#generar porcentajes por mes por categoria

