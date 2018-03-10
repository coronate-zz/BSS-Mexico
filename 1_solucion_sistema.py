
"""
Para la primera parte de la solución se tomara un sistema y se intentara resolver siuiendo
"""
import itertools
import pandas as pd  
import numpy as np 
import random

columnas = ['A', 'B', 'C', 'D']
S = pd.DataFrame( columns = columnas, index=  columnas)
for i in columnas:
	for j in columnas:
		if i == j:
			S.loc[i, j] = 'X'
		else:	
			S.loc[i, j] = np.random.randint(1, 10)

NUM_ESTACIONES =  5
NUM_ESTADOS =  5
def mapaAleatorio( NUM_ESTACIONES, NUM_ESTADOS ): 
	print("-------CREACION DE LISTA CON NOMBRES ESTACION---------")

	listaNombres = list()
	for i in range( NUM_ESTACIONES ): 
		nombre  =  "estacion_" +  str(i+1)
		listaNombres.append( nombre)
	#Matriz con columnas == numero de estaciones e index  ==  numero de estaciones

	estacionesMap = pd.DataFrame(  index=  listaNombres , columns= listaNombres )
	print("-------CREACION DE MAPA ALEATORIO----------")

	for i in range( len( estacionesMap )):
		fila  = estacionesMap.index[i]
		for j in range( len( estacionesMap )):
				columna =  estacionesMap.columns[ j]
				if fila == columna:
					estacionesMap.loc[ fila, columna ] = "X"
				else:
					estacionesMap.loc[ fila, columna ] = random.randint( 1, NUM_ESTADOS ) 
	return estacionesMap




def getCode( S ):
	lista =  []
	for i in S.columns:
		for j in S.columns:
			lista.append(str(S.loc[i, j] ))
	
	return lista

"""
Es necesario crear unos diccionarios globales para poder insertar las soluciones y que puedan ser consultados en
cualquier scope del codigo.
SOLUCIONES

 L     SYSTEM        CODE 

[2]   [X][p1]   == [][][][] => CODE
	  [p2][X]

[3]   [][][]    == [][][][][][][][][] => CODE
      [][][]
      [][][]

[4]   [][][][]  == [][][][][][][][][][][][][][][][] => CODE
      [][][][]
      [][][][]
      [][][][]
...

"""

global SOLUCIONES
SOLUCIONES = dict()

def getSolution( code ):
	"""
	Return the solution of the system if the code of the system is saved in the dictionary.
	1. Look for the dictionary -> L
	2. If L is found the this dictionary have all the previous solved systems of length L
	3. Look for the code s of system S in L

	""" 
	global SOLUCIONES
	l = len(code)
	try:
		type(SOLUCIONES[l] )
		try:
			solution_sequence = SOLUCIONES[l][code]['sequence'] 
			solution_cost = SOLUCIONES[l][code]['cost'] 
			return solution_sequence, solution_cost
		except Exception as e:
			print("No existe respuesta para code = {}".format(code))
			return False

	except Exception as e:
		print( "No existe el nivel L = {} en el diccionario".format(l))
		SOLUCIONES[l] = dict()
		return False

def insertSolution(code, optimal_mov, min_cost):
	"""
	Once we solve the system S we save the optimal transition route in SOLUCIONES
	in the L index.
	"""
	global SOLUCIONES
	l = len(code)
	code = ' '.join(code)
	level = int(np.sqrt(l))
	tab = "\t"
	#for i in range(level):
	#	tab = tab + "\t"
	#print("\n\n"+tab+"  --------Ingresando solucion sobre {}: => {} ------".format(l, code ))
	SOLUCIONES[l][code] = dict()
	SOLUCIONES[l][code]["cost"] = min_cost
	SOLUCIONES[l][code]["sequence"] = optimal_mov
	#TO DO: Exixten varios sistemas que son equivalentes. Es posible obtener todas las permutaciones
	#de las columnas para obtener los sistemas equivalentes.


def getSystem(S, movement_node):
	"""
	Delete the first column and the first row in order to remove one node from the system

	[a,a][a,b][a,c][a,d]
	[b,a] [][][]
	[b,c] [][][]
	[b,d] [][][]

	After this transformMatrix reorder ht matrix so the movement_node is at the column 0, 
	row 0. 

	"""
	starting_node = S.columns[0]
	columnsMinusA = list(S.columns)
	columnsMinusA.remove(starting_node)
	S_minusA = S[columnsMinusA]
	S_minusA = S_minusA.loc[columnsMinusA]

	s_minusA_start = S_minusA.columns[0]
	return transformMatrix( S_minusA, s_minusA_start, movement_node)


def transformMatrix(S, a, b ):
	"""
	[a][B][C][b] => [b][B][C][a]

	   [a][B][C][b] 	          [b][B][C][a]                 [b][B][C][a] 

	[a]  [a,a] [] [a,b]	     [a]  [a,b] [a,] [a,a]        [b]  [b,b] [b,] [b,a]
	[B]  [a]   [] [b]   =>   [B]  [b]   []   [a]    =>    [B]  [b]   []   [a]   
	[C]  [a]   [] [b]        [C]  [b]   []   [a]          [C]  [b]   []   [a]   
	[b]  [b,a] [] [b,b]      [b]  [b,b] [b,] [b,a]        [a]  [a,b] [a,] [a,a]


	"""
	order =  list(S.columns)
	aPosition = order.index(a)
	bPosition = order.index(b)
	#Changing columns order
	order[bPosition] = a
	order[aPosition] = b
	#Changing rows order

	newMatrix = S[order]
	newMatrix = newMatrix.loc[order]

	return newMatrix


####################################################################################################################

def solveSystem(S):
	"""
	Given a System S of NxN nodes. This function returns the optimal sequence of nodes that minimize the cost of 
	traveling through al the nodes.
	"""

	global SOLUCIONES
	codeS        = getCode(S)           #GeneticCode that represent's the system [A, B, A D np.nan ... ]
	solutionS    = getSolution( codeS ) #False if system haven't been solved.
	starting_node = S.columns[0]         #
	nodesList    = list(S.columns)      # A, B , C , D
	movementList = dict()     # 0->NA,  1->B, 2->C, ... n->N

	#Print function so we ean diferenciate levels
	level = len(S.columns)
	tab = "\t"
	for i in range(level):
		tab = tab + "\t"


	for i in range(len(nodesList)):
		if i != 0:
			movementList[ i ] =  nodesList[i]


	print("\n\n Evaluando el Sistema:\n\n {} \n\n CODIGO {} ".format(S, codeS))

	if solutionS:
		return solutionS

	else: #No existe solucion guaradda para code en SOLUCIONES
		if len( codeS ) <= 4: #El codigo corresponde a una matriz de 2X2 y solo hay una opciond e moviento
			print("\n" + tab + "***Se ha llegado al minimo sistema***")
			optimal_mov =[ [0,1]  ]
			movement_node = movementList[1]
			min_cost = S.loc[starting_node, movement_node]
			#print(optimal_mov)

		else:
			min_cost = 10000000
			for mov in movementList.keys():
				movement_node = movementList[mov]
				print("\n" +tab+ "Moviendo camion de {}  a {} ".format( starting_node, movement_node))
				#list(itertools.permutations([1, 2, 3]))
				mov_cost  = S.loc[starting_node, movement_node]

				#Delete the starting node and transform the system so movement_node -> starting_node
				SminiusMov = getSystem( S, movement_node)
				SminiusMov_movements, SminiusMov_cost= solveSystem(SminiusMov)
				print(SminiusMov_movements)

				total_cost = mov_cost + SminiusMov_cost

				print("\n" +tab+ "Ruta evaluda: mov_cost {} total_cost {} ".format( mov_cost, total_cost))

				if total_cost < min_cost:
					min_cost    = total_cost

					optimal_mov = SminiusMov_movements +  [[0,mov]]
					print( "\n"+tab+"NUEVO MINIMO: {}   =>  {} xxxx {} ".format(min_cost, optimal_mov, SminiusMov_movements) )


		insertSolution( codeS, optimal_mov, min_cost)
		return optimal_mov, min_cost







seq, cost =  solveSystem(S)






