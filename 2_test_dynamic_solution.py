
"""
In this section different size systems are solved andthe amount of time taken
by the algorithm so find a slution is reported. A brute force algorithm is used as 
bechmark to test how efficient is the algorithm

TO DO: Imporve algorithm for level4 dictionary and maybe level 2
"""

import pandas as pd 
import numpy as numpy
import time

RESULTS = dict()
RESULTS["bruteSolution"] = dict()
RESULTS["dynamicSolution"] = dict()
RESULTS["dynamicSolution_memory"] = dict()              #Using the same dictionary in all iterations.
RESULTS["dynamicSolution_memory_equivalent"] = dict()  #Getting solutions using equivalent systems that increase the number of solution in the dictionary

solutions_size = dict()

for systemSize in range(8): 
    systemSize_name = "size_" + str(systemSize+2)
    print(systemSize_name)
    RESULTS["bruteSolution"][systemSize_name] = dict()
    RESULTS["dynamicSolution"][systemSize_name] = dict()
    RESULTS["dynamicSolution_memory"][systemSize_name] = dict()
    RESULTS["dynamicSolution_memory_equivalent"][systemSize_name] = dict()

    for stateNumber in range(7):
        stateNumber_name = "state_" + str(stateNumber+3)
        print(stateNumber_name)

        RESULTS["bruteSolution"][systemSize_name][stateNumber_name] = np.nan  #Time required by the bruteForce solution to solve the System
        RESULTS["dynamicSolution"][systemSize_name][stateNumber_name] = np.nan #Time required by the dynamiSolution to solve the System
        RESULTS["dynamicSolution_memory"][systemSize_name][stateNumber_name] = np.nan #Time required by the dynamiSolution to solve the System
        RESULTS["dynamicSolution_memory_equivalent"][systemSize_name][stateNumber_name] = np.nan #Time required by the dynamiSolution to solve the System


results = pd.DataFrame( RESULTS["bruteSolution"]) 
#mov, cost = solveSystem(S)
#mov_brute, cost_brute = solveSystem_bruteForce(S)

#S = mapaAleatorio( 10,10 )
#seq, cost =  solveSystem(S)


"""
In this first iteration we just want to test if there is a significative advantage of the dynamic algorithm 
refreshing the dictionary in each iteration. We expect that for very small sizeSystems we are just going to
find disadvatages but as the size of the system increases it's more probable that the 

"""
systemSize_names = RESULTS["dynamicSolution"].keys()
stateNumber_names = RESULTS["dynamicSolution"]["size_10"].keys()

SOLUCIONES  = dict()
ITERATION_COUNT = 0
solutions_size[ITERATION_COUNT] = sys.getsizeof(SOLUCIONES)


for systemSize in systemSize_names: 
    for stateNumber in stateNumber_names:
        print( "SOLVING =>  SIZE:{} stateNumber{} ".format( systemSize, stateNumber ))
        for iteration in range( 10 ): 
            ITERATION_COUNT += 1

            S = mapaAleatorio( systemSize, stateNumber) 
            #1000 iterations are performed in order to obtain a more accurate measure of the time required by
            #each algorithm to solve the System.
            dynamicStart = time.time()
            dynamicMov, dynamicCost = solveSystem(S, equivalent_systems =False, start_solutions = False )
            dynamicEnd = time.time()

            bruteStart = time.time()
            bruteMov, bruteCost = solveSystem_bruteForce(S)
            bruteEnd = time.time()

            if bruteMov != dynamicMov:
                print( "WARNING: Algorithms differ in optimal solution")

            if bruteCost != dynamicCost:
                print( "WARNING: Algorithms differ in optimal cost")

            bruteTime = bruteEnd - bruteStart
            bruteTime_total += bruteTime

            dynamicTime = dynamicEnd - dynamicStart
            dynamicTime_total += dynamicTime


            solutions_size[ITERATION_COUNT] = sys.getsizeof(SOLUCIONES)

        resultDynamic = dynamicTime_total / 10
        resultBrute   = bruteTime_total / 10
        RESULTS["dynamiSolution"][systemSize][stateNumber] = resultDynamic
        RESULTS["bruteSolution"][systemSize][stateNumber]  = resultBrute
        print( "\tREPORTING SOLUTION => DYNAMIC: {} BRUTE: {}".format(resultDynamic, resultBrute))



for systemSize in systemSize_names: 
    for stateNumber in stateNumber_names:
        print( "SOLVING =>  SIZE:{} stateNumber{} ".format( systemSize, stateNumber ))
        for iteration in range( 10 ): 
            ITERATION_COUNT += 1


            S = mapaAleatorio( systemSize, stateNumber) 
            #1000 iterations are performed in order to obtain a more accurate measure of the time required by
            #each algorithm to solve the System.
            dynamicStart = time.time()
            dynamicMov, dynamicCost = solveSystem(S, equivalent_systems =False, start_solutions = False )
            dynamicEnd = time.time()

            dynamicTime = dynamicEnd - dynamicStart
            dynamicTime_total += dynamicTime
            solutions_size[ITERATION_COUNT] = sys.getsizeof(SOLUCIONES)

        resultDynamic = dynamicTime_total / 10
        RESULTS["dynamicSolution_equivalent"][systemSize][stateNumber] = resultDynamic
        print( "\tREPORTING SOLUTION => DYNAMIC: {} ".format(resultDynamic)


SOLUCIONES  = dict()
ITERATION_COUNT = 0
solutions_size[ITERATION_COUNT] = sys.getsizeof(SOLUCIONES)
for systemSize in systemSize_names: 
    for stateNumber in stateNumber_names:
        print( "SOLVING =>  SIZE:{} stateNumber{} ".format( systemSize, stateNumber ))
        for iteration in range( 100 ): 


            S = mapaAleatorio( systemSize, stateNumber) 
            ss =  np.power(systemSize, 2) 
            #1000 iterations are performed in order to obtain a more accurate measure of the time required by
            #each algorithm to solve the System.
            dynamicStart = time.time()
            dynamicMov, dynamicCost = solveSystem(S, equivalent_systems =True, start_solutions = 9 )
            dynamicEnd = time.time()

            dynamicTime = dynamicEnd - dynamicStart
            dynamicTime_total += dynamicTime
            solutions_size[ITERATION_COUNT] = sys.getsizeof(SOLUCIONES)

        resultDynamic = dynamicTime_total / 100
        RESULTS["dynamicSolution_memory_equivalent"][systemSize][stateNumber] = resultDynamic
        print( "\tREPORTING SOLUTION => DYNAMIC: {} ".format(resultDynamic)




