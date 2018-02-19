
"""
Para la primera parte de la solución se tomara un sistema y se intentara resolver siuiendo
"""
import itertools
import pandas as pd  
import numpy as np 

columnas = ['A', 'B', 'C', 'D']
S = pd.DataFrame( columns = columnas, index=  columnas)
for i in columnas:
	for j in columnas:
		if i == j:
			S.loc[i, j] = np.nan
		else:	
			S.loc[i, j] = np.random.randint(1, 10)



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
	global SOLUCIONES
	l = len(code)
	code = ' '.join(code)
	print("\n\n  --------Ingresando solucion sobre {}: => {} ------".format(l, code ))
	SOLUCIONES[l][code] = dict()
	SOLUCIONES[l][code]["cost"] = min_cost
	SOLUCIONES[l][code]["sequence"] = optimal_mov
	#TO DO: Exixten varios sistemas que son equivalentes. Es posible obtener todas las permutaciones
	#de las columnas para obtener los sistemas equivalentes.



def solveSystem(S):
	global SOLUCIONES
	codeS        = getCode(S)
	solutionS    = getSolution( codeS )
	startingNode = S.columns[0]
	nodesList    = list(S.columns)
	movementList = nodesList.copy()
	movementList.remove(startingNode)
	print("\n\n Evaluando el Sistema:\n\n {} \n\n CODIGO {} ".format(S, codeS))

	if solutionS:
		return solutionS

	else: #No existe solucion guaradda para code en SOLUCIONES
		if len( codeS ) <= 4: #El codigo corresponde a una matriz de 2X2 y solo hay una opciond e moviento
			print("\n***Se ha llegado al minimo sistema***")
			optimal_mov = list(startingNode + movementList[0])
			print(optimal_mov)
			min_cost = S.loc[startingNode, movementList[0]]
			insertSolution( codeS, optimal_mov, min_cost)

		else:
			min_cost = 10000000
			for mov in movementList:
				print("\n\tMoviendo camion de {}  a {} ".format( startingNode, mov))
				#list(itertools.permutations([1, 2, 3]))
				mov_cost  = S.loc[startingNode, mov]
				SminiusMov = getSystem( S, mov)
				SminiusMov_movments, SminiusMov_cost= solveSystem(SminiusMov)
				total_cost = mov_cost + SminiusMov_cost
				print("\n\tRuata evaluda: mov_cost {} total_cost {} ".format( mov_cost, total_cost))

				if total_cost < min_cost:
					print( "\n\t\tNUEVO MINIMO")
					min_cost    = total_cost
					print(SminiusMov_movments)
					SminiusMov_movments.insert(0, mov)
					SminiusMov_movments.insert(0, startingNode)
					optimal_mov = SminiusMov_movments
		insertSolution( codeS, optimal_mov, min_cost)
		return optimal_mov, min_cost



def getSystem(S, mov):
	startingNode = S.columns[0]
	columnsMinusA = list(S.columns)
	columnsMinusA.remove(startingNode)
	S_minusA = S[columnsMinusA]
	S_minusA = S_minusA.loc[columnsMinusA]

	newStartingNode = S_minusA.columns[0]
	return transformMatrix( S_minusA, newStartingNode, mov)


def transformMatrix(S, a, b ):
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




res1, res2 =  solveSystem(S)






