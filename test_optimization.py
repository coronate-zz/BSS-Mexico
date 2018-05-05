

#--------------MULTIPLE ITERATION TEST -------------------------
import copy #copy.deepcopy() for objects 
import utils_solver
#First we have to iterate multiple times in order to obtain an ubiased measure of time and cost of the algorithm
#TO DO: Define the system we want to test. How many statiosn, how many states, what is the distribution 
#those states.

TEST_ITERATIONS = 300

SCORES = {'gradient_model': dict(),
		  'iteration_model': dict(),
		  'iteration_gradient_model':dict()}

SCORES["gradient_model"]["min_cost"]  = 10000000
SCORES["gradient_model"]["max_cost"]  = -1
SCORES["gradient_model"]["total_cost"] = 0 
SCORES["gradient_model"]["min_time"]  = 10000000
SCORES["gradient_model"]["max_time"]  = -1
SCORES["gradient_model"]["total_time"] = 0 

SCORES["iteration_gradient_model"]["min_cost"]  = 10000000
SCORES["iteration_gradient_model"]["max_cost"]  = -1
SCORES["iteration_gradient_model"]["total_cost"] = 0 
SCORES["iteration_gradient_model"]["min_time"]  = 10000000
SCORES["iteration_gradient_model"]["max_time"]  = -1
SCORES["iteration_gradient_model"]["total_time"] = 0 

SCORES["iteration_model"]["min_cost"]  = 10000000
SCORES["iteration_model"]["max_cost"]  = -1
SCORES["iteration_model"]["total_cost"] = 0 
SCORES["iteration_model"]["min_time"]  = 10000000
SCORES["iteration_model"]["max_time"]  = -1
SCORES["iteration_model"]["total_time"] = 0 



for iter in range(TEST_ITERATIONS):
	#The FLEET.position (position of each car) and the System must be constant for the optimization of S
	#but they have to change for each iter in TEST_ITERATIONS.


	MAP = Map(N_STATIONS, N_STATES) #Always the same size.
	FLEET = Fleet()
	# We assign a random station for each car
	car_position = random.sample( list(MAP.weights.columns) , N_CARS)

	for i in range(N_CARS):
	    id_car = i
	    position = car_position[i]
	    capacity = random.randint(5,20) #TO DO: each car have their on capcity

	    car = Car( id_car, position, capacity )
	    FLEET.insertCar(car)

	FLEET.update_carsPosition()          #Save car positions in FLEET.positions
	MAP.update_available_stations(FLEET) #Remove car positio and car subsytem from available_stations

	#-----------------------------------ITERATION--------------------------
	start_time = time.time()
	MIN_COST, FLEET_MIN  = utils_solver.subsytem_distribution_iterativeOptimization(100,FLEET, MAP)
	end_time = time.time()
	execution_time =  end_time - start_time

	SCORES["iteration_model"]["total_cost"] += FLEET_MIN.accumalated_cost
	SCORES["iteration_model"]["total_time"] += execution_time

	if SCORES["iteration_model"]["min_cost"] > FLEET_MIN.accumalated_cost:
		SCORES["iteration_model"]["min_cost"] = FLEET_MIN.accumalated_cost

	if SCORES["iteration_model"]["max_cost"] < FLEET_MIN.accumalated_cost:
		SCORES["iteration_model"]["max_cost"] = FLEET_MIN.accumalated_cost


	if SCORES["iteration_model"]["min_time"] > execution_time:
		SCORES["iteration_model"]["min_time"] = execution_time

	if SCORES["iteration_model"]["max_time"] < execution_time:
		SCORES["iteration_model"]["max_time"] = execution_time


	#-----------------------------------GRADIENT-------------------------------
	start_time = time.time()
	MIN_COST, FLEET_MIN  = utils_solver.subsystem_distribution_gradientOptimization(FLEET, MAP)
	end_time = time.time()
	execution_time =  end_time - start_time

	SCORES["gradient_model"]["total_cost"] += FLEET_MIN.accumalated_cost
	SCORES["gradient_model"]["total_time"] += execution_time

	if SCORES["gradient_model"]["min_cost"] > FLEET_MIN.accumalated_cost:
		SCORES["gradient_model"]["min_cost"] = FLEET_MIN.accumalated_cost

	if SCORES["gradient_model"]["max_cost"] < FLEET_MIN.accumalated_cost:
		SCORES["gradient_model"]["max_cost"] = FLEET_MIN.accumalated_cost


	if SCORES["gradient_model"]["min_time"] > execution_time:
		SCORES["gradient_model"]["min_time"] = execution_time

	if SCORES["gradient_model"]["max_time"] < execution_time:
		SCORES["gradient_model"]["max_time"] = execution_time


	#-----------------------------------ITERATION + GRADIENT--------------------------
	start_time = time.time()
	MIN_COST, FLEET_MIN  = utils_solver.subsystem_distribution_iterativeGradientOptimization(20, FLEET, MAP)
	end_time = time.time()
	execution_time =  end_time - start_time

	SCORES["iteration_gradient_model"]["total_cost"] += FLEET_MIN.accumalated_cost
	SCORES["iteration_gradient_model"]["total_time"] += execution_time

	if SCORES["iteration_gradient_model"]["min_cost"] > FLEET_MIN.accumalated_cost:
		SCORES["iteration_gradient_model"]["min_cost"] = FLEET_MIN.accumalated_cost

	if SCORES["iteration_gradient_model"]["max_cost"] < FLEET_MIN.accumalated_cost:
		SCORES["iteration_gradient_model"]["max_cost"] = FLEET_MIN.accumalated_cost


	if SCORES["iteration_gradient_model"]["min_time"] > execution_time:
		SCORES["iteration_gradient_model"]["min_time"] = execution_time

	if SCORES["iteration_gradient_model"]["max_time"] < execution_time:
		SCORES["iteration_gradient_model"]["max_time"] = execution_time



SCORES["iteration_model"]["avg_cost"] = SCORES["iteration_model"]["total_cost"] / TEST_ITERATIONS
SCORES["gradient_model"]["avg_cost"] = SCORES["gradient_model"]["total_cost"] / TEST_ITERATIONS
SCORES["iteration_gradient_model"]["avg_cost"] = SCORES["iteration_gradient_model"]["total_cost"] / TEST_ITERATIONS

SCORES["iteration_model"]["avg_time"] = SCORES["iteration_model"]["total_time"] / TEST_ITERATIONS
SCORES["gradient_model"]["avg_time"] = SCORES["gradient_model"]["total_time"] / TEST_ITERATIONS
SCORES["iteration_gradient_model"]["avg_cost"] = SCORES["iteration_gradient_model"]["total_time"] / TEST_ITERATIONS


utils_solver.save_obj(SCORES, 'SCORES_optimization')
