

"""
In this test we want to compare the how efficient is the iteration_model versus the
gradient_model and the iteration_gradient_model.

To make this compairson we will run many scenarios using diferents sizes of STATES
and different subsytem sizes.

In each scenario we solve 100 = SECUENTIAL_ITERATIONS secuential problems (We don't reset the SOLUCIONES dictionary).

In each iteration:
    *A new subsytem is assigned to each car.
        #In Map we have 444 stations and we assign area->n_subsystems stations to each car.
    *The SOLUTION dictionary is saved in memory simulation a real case.
    *Each subsytem is solved for each car running the dynamicSolution with
    the dynamic algorithm.
    *Many subsystems are tested in order to find the sub-optimal subsystem distribution.
    *We assume that all the cars are equal so the weight vector for each car will be
    the same of the weight of the COST_MATRIX. 
    *We save the results un SCORES dictionary to find how long it take for each mdoel 
    to solve the secuential problems
        SCORES:
            -min_cost
            -max_cost
            -total_cost
            -min_time
            -max_time
            -total_time

    The metasytem still doesn't so we are going to test solving random systems
    secuetilly however the time of solving those systems is an upper bound to solve 
    secuetial problems in the metasystem.

TO DO: Each scenario is repated 100 = TEST_ITERATIONS so our results are unbiased.
            **It could be the case that the 100 SECUENTIAL_ITERATIONS have eassier 
            problems for some of the results.

"""

#--------------MULTIPLE ITERATION TEST -------------------------
import copy #copy.deepcopy() for objects 
import utils_solver
#First we have to iterate multiple times in order to obtain an ubiased measure of time and cost of the algorithm
#TO DO: Define the system we want to test. How many statiosn, how many states, what is the distribution 
#those states.


#n_estados = [5, 7, 8, 10] 
#n_subsystems= [5, 7 8,10]
n_estados    = [5, 7, 10]
n_subsystems = [5, 10, 15, 20]
N_STATIONS = 444
SCORES = dict()
estado = 100000
SECUENTIAL_ITERATIONS = 2


#------------------------------ START DICTIONARY0 --------------------------------------
for estado in n_estados:
    SCORES[estado] =dict()
    for area in n_subsystems:
        print("ESTADO: {} \n\tSUBSYSTEM SIZE: {}".format(estado, area))
        SCORES[estado][area] = {'gradient_model': dict(),
                  'iteration_model': dict(),
                  'iteration_gradient_model':dict()}

        SCORES[estado][area]["gradient_model"]["min_cost"]  = 10000000
        SCORES[estado][area]["gradient_model"]["max_cost"]  = -1
        SCORES[estado][area]["gradient_model"]["total_cost"] = 0 
        SCORES[estado][area]["gradient_model"]["min_time"]  = 10000000
        SCORES[estado][area]["gradient_model"]["max_time"]  = -1
        SCORES[estado][area]["gradient_model"]["total_time"] = 0 

        SCORES[estado][area]["iteration_gradient_model"]["min_cost"]  = 10000000
        SCORES[estado][area]["iteration_gradient_model"]["max_cost"]  = -1
        SCORES[estado][area]["iteration_gradient_model"]["total_cost"] = 0 
        SCORES[estado][area]["iteration_gradient_model"]["min_time"]  = 10000000
        SCORES[estado][area]["iteration_gradient_model"]["max_time"]  = -1
        SCORES[estado][area]["iteration_gradient_model"]["total_time"] = 0 

        SCORES[estado][area]["iteration_model"]["min_cost"]  = 10000000
        SCORES[estado][area]["iteration_model"]["max_cost"]  = -1
        SCORES[estado][area]["iteration_model"]["total_cost"] = 0 
        SCORES[estado][area]["iteration_model"]["min_time"]  = 10000000
        SCORES[estado][area]["iteration_model"]["max_time"]  = -1
        SCORES[estado][area]["iteration_model"]["total_time"] = 0 



"""
-----------------------------------GRADIENT TEST--------------------------------
We know the first element in cost_fleet dictionary is the car incurring in more cost. 
We will change this car distribution chnaging the station with the higher avg cost
for an other station in the available_stations list.
if the available_stations list is empty then we will change with the
the highest avg cost station of the  second element
in dictionary (second most expensive car). 

"""

for estado in tqdm(n_estados, ascii= True, desc= "GRADIENT TEST"):
    for area in n_subsystems:
        SOLUCIONES = dict()
        #We are going to delete the stations that are over the 7 decil.
        MAX_COBERTURE = round(estado*.7)

        for iter in range(SECUENTIAL_ITERATIONS):
            #The FLEET.position (position of each car) and the System must be constant for the optimization of S
            #but they have to change for each iter in SECUENTIAL_ITERATIONS.

            MAP = Map(N_STATIONS, estado) #Always the same size.
            FLEET = Fleet(area, MAX_COBERTURE)

            # We assign a random station for each car
            car_position = random.sample( list(MAP.weights.columns) , N_CARS)

            #In each iteration we assign a new subsytem to each car.
            for i in range(N_CARS):
                id_car = i
                position = car_position[i]
                capacity = random.randint(5,20) #TO DO: each car have their on capcity
                car = Car( id_car, position, capacity )
                FLEET.insertCar(car)

            FLEET.update_carsPosition()          #Save car positions in FLEET.positions
            MAP.update_available_stations(FLEET) #Remove car positio and car subsytem from available_stations
            FLEET.assignArea(MAP)                #Assign subsystem to each car
            FLEET.solve_subsystems(MAP)

            #-----------------------------------GRADIENT-------------------------------
            start_time = time.time()
            MIN_COST, FLEET_MIN  = utils_solver.subsystem_distribution_gradientOptimization(FLEET, MAP)
            end_time = time.time()
            execution_time =  end_time - start_time

            SCORES[estado][area]["gradient_model"]["total_cost"] += MIN_COST
            SCORES[estado][area]["gradient_model"]["total_time"] += execution_time

            if SCORES[estado][area]["gradient_model"]["min_cost"] > MIN_COST:
                SCORES[estado][area]["gradient_model"]["min_cost"] = MIN_COST

            if SCORES[estado][area]["gradient_model"]["max_cost"] < MIN_COST:
                SCORES[estado][area]["gradient_model"]["max_cost"] = MIN_COST


            if SCORES[estado][area]["gradient_model"]["min_time"] > execution_time:
                SCORES[estado][area]["gradient_model"]["min_time"] = execution_time

            if SCORES[estado][area]["gradient_model"]["max_time"] < execution_time:
                SCORES[estado][area]["gradient_model"]["max_time"] = execution_time

utils_solver.save_obj(SCORES, 'SCORES_optimization')



for estado in tqdm(n_estados, ascii= True, desc= "ITERATION TEST"):
    for area in n_subsystems:
        SOLUCIONES = dict()
        #We are going to delete the stations that are over the 7 decil.
        MAX_COBERTURE = round(estado*.7)

        for iter in range(SECUENTIAL_ITERATIONS):
            #The FLEET.position (position of each car) and the System must be constant for the optimization of S
            #but they have to change for each iter in SECUENTIAL_ITERATIONS.

            MAP = Map(N_STATIONS, N_STATES) #Always the same size.
            FLEET = Fleet(area, MAX_COBERTURE)
            MAP.update_available_stations(FLEET) #Remove car positio and car subsytem from available_stations

            # We assign a random station for each car
            car_position = random.sample( list(MAP.weights.columns) , N_CARS)

            #In each iteration we assign a new subsytem to each car.
            for i in range(N_CARS):
                id_car = i
                position = car_position[i]
                capacity = random.randint(5,20) #TO DO: each car have their on capcity
                car = Car( id_car, position, capacity )
                FLEET.insertCar(car)

            FLEET.update_carsPosition()          #Save car positions in FLEET.positions
            MAP.update_available_stations(FLEET) #Remove car positio and car subsytem from available_stations
            FLEET.assignArea(MAP)                #Assign subsystem to each car
            FLEET.solve_subsystems(MAP)


            #-----------------------------------ITERATION-------------------------------

            start_time = time.time()
            MIN_COST, FLEET_MIN  = utils_solver.subsytem_distribution_iterativeOptimization(100,FLEET, MAP)
            end_time = time.time()
            execution_time =  end_time - start_time


            SCORES[estado][area]["iteration_model"]["total_cost"] += MIN_COST
            SCORES[estado][area]["iteration_model"]["total_time"] += execution_time

            if SCORES[estado][area]["iteration_model"]["min_cost"] > MIN_COST:
                SCORES[estado][area]["iteration_model"]["min_cost"] = MIN_COST

            if SCORES[estado][area]["iteration_model"]["max_cost"] < MIN_COST:
                SCORES[estado][area]["iteration_model"]["max_cost"] = MIN_COST

            if SCORES[estado][area]["iteration_model"]["min_time"] > execution_time:
                SCORES[estado][area]["iteration_model"]["min_time"] = execution_time

            if SCORES[estado][area]["iteration_model"]["max_time"] < execution_time:
                SCORES[estado][area]["iteration_model"]["max_time"] = execution_time


utils_solver.save_obj(SCORES, 'SCORES_optimization')


for estado in tqdm(n_estados, ascii= True, desc= "ITERATION + GRADIENT TEST"):
    for area in n_subsystems:
        SOLUCIONES = dict()
        #We are going to delete the stations that are over the 7 decil.
        MAX_COBERTURE = round(estado*.7)

        for iter in range(SECUENTIAL_ITERATIONS):
            print("\n\n\n-------------------------NEW ITERATION---------------")
            #The FLEET.position (position of each car) and the System must be constant for the optimization of S
            #but they have to change for each iter in SECUENTIAL_ITERATIONS.

            MAP = Map(N_STATIONS, N_STATES) #Always the same size.
            FLEET = Fleet(area, MAX_COBERTURE)
            MAP.update_available_stations(FLEET) #Remove car positio and car subsytem from available_stations
            # We assign a random station for each car
            car_position = random.sample( list(MAP.weights.columns) , N_CARS)

            #In each iteration we assign a new subsytem to each car.
            for i in range(N_CARS):
                id_car = i
                position = car_position[i]
                capacity = random.randint(5,20) #TO DO: each car have their on capcity
                car = Car( id_car, position, capacity )
                FLEET.insertCar(car)

            FLEET.update_carsPosition()          #Save car positions in FLEET.positions
            MAP.update_available_stations(FLEET) #Remove car positio and car subsytem from available_stations
            FLEET.assignArea(MAP)                #Assign subsystem to each car
            FLEET.solve_subsystems(MAP)

            #-----------------------------------ITERATION + GRADIENT--------------------------
            start_time = time.time()
            MIN_COST, FLEET_MIN  = utils_solver.subsystem_distribution_iterativeGradientOptimization(20, FLEET, MAP)
            end_time = time.time()
            execution_time =  end_time - start_time

            SCORES[estado][area]["iteration_gradient_model"]["total_cost"] += MIN_COST
            SCORES[estado][area]["iteration_gradient_model"]["total_time"] += execution_time

            if SCORES[estado][area]["iteration_gradient_model"]["min_cost"] > MIN_COST:
                SCORES[estado][area]["iteration_gradient_model"]["min_cost"] = MIN_COST

            if SCORES[estado][area]["iteration_gradient_model"]["max_cost"] < MIN_COST:
                SCORES[estado][area]["iteration_gradient_model"]["max_cost"] = MIN_COST


            if SCORES[estado][area]["iteration_gradient_model"]["min_time"] > execution_time:
                SCORES[estado][area]["iteration_gradient_model"]["min_time"] = execution_time

            if SCORES[estado][area]["iteration_gradient_model"]["max_time"] < execution_time:
                SCORES[estado][area]["iteration_gradient_model"]["max_time"] = execution_time


for estado in tqdm(n_estados, ascii= True, desc= "ITERATION + GRADIENT TEST"):
    for area in n_subsystems:
        SCORES[estado][area]["iteration_model"]["avg_cost"] = SCORES[estado][area]["iteration_model"]["total_cost"] / SECUENTIAL_ITERATIONS
        SCORES[estado][area]["gradient_model"]["avg_cost"] = SCORES[estado][area]["gradient_model"]["total_cost"] / SECUENTIAL_ITERATIONS
        SCORES[estado][area]["iteration_gradient_model"]["avg_cost"] = SCORES[estado][area]["iteration_gradient_model"]["total_cost"] / SECUENTIAL_ITERATIONS

        SCORES[estado][area]["iteration_model"]["avg_time"] = SCORES[estado][area]["iteration_model"]["total_time"] / SECUENTIAL_ITERATIONS
        SCORES[estado][area]["gradient_model"]["avg_time"] = SCORES[estado][area]["gradient_model"]["total_time"] / SECUENTIAL_ITERATIONS
        SCORES[estado][area]["iteration_gradient_model"]["avg_cost"] = SCORES[estado][area]["iteration_gradient_model"]["total_time"] / SECUENTIAL_ITERATIONS


utils_solver.save_obj(SCORES, 'SCORES_optimization')
    