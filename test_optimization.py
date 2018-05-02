

#--------------MULTIPLE ITERATION TEST -------------------------
import copy #copy.deepcopy() for objects 

#First we have to iterate multiple times in order to obtain an ubiased measure of time and cost of the algorithm
TEST_ITERATIONS = 100
N_ITERATION = 
#for iter in range(TEST_ITERATIONS):
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
FLEET_SECONDARY = copy.deepcopy(FLEET)
MIN_COST = 10000000

#1) ITERATION MODEL FUNCTION
for i in  N_ITERATION: 
    #This part change for optimization
    FLEET_SECONDARY.assignArea(MAP)                #Assign subsystem to each car
    FLEET_SECONDARY.solve_subsystems(MAP)
    if FLEET_SECONDARY.accumalated_cost < MIN_COST:
        FLEET_MIN = copy.deepcopy(FLEET_SECONDARY)
        MIN_COST = FLEET_MIN.accumalated_cost
        print("New min cost {}".format(MIN_COST))


#2) GRADIENT MODEL FUNTION

#We know the first element in cost_fleet dictionary is the car incurring in more cost. 
#We will change this car distribution chnaging the station with the higher avg cost
#for an other station in the available_stations list.
#if the available_stations list is empty then we will change with the
#the highest avg cost station of the  second element
#in dictionary (second most expensive car).


#----------------------------------------------------------------------
stillChange = True
firstIteration = True
FLEET_SECONDARY = copy.deepcopy(FLEET)
cont = 0
while stillChange:
	if firstIteration:
		start_cost = FLEET_SECONDARY.accumalated_cost
		print("START COST" + str(start_cost))
		firstIteration =  False

	FLEET_SECONDARY.set_cost_distribution()
	cost_fleet = FLEET_SECONDARY.cost_distribution
	most_expensive_car = cost_fleet.head(1).index[0] #Id of car with the route with more cost.
	most_expensive_car = FLEET_SECONDARY.fleet[most_expensive_car]

	most_expensive_station = most_expensive_car.get_mostExpensive_station()
	most_expensive_car.subsystem_list.remove(most_expensive_station)
	most_expensive_car.set_subsystem(MAP)

	MAP.update_available_stations(FLEET_SECONDARY)
	MAP.change_station(most_expensive_car, MAP) #this function must change the worst station for car i to another station
	
	FLEET_SECONDARY.solve_subsystems(MAP)
	if FLEET_SECONDARY.accumalated_cost < FLEET.accumalated_cost:
		FLEET = copy.deepcopy(FLEET_SECONDARY)
		stillChange =  True
		cont = 0
		print("New FLEET_MIN cost: {}".format(FLEET.accumalated_cost))
	else:
		if cont >= 10:
			stillChange = False	
		else:
			cont += 1
FLEET_MIN = FLEET
print("The subsystem distribution was optimized:\n\t Initial Cost: {} \n\t Final Cost: {}".format(start_cost, FLEET_MIN.accumalated_cost))




SCORES["iteration_model"]["total_cost"]+= FLEET_MIN.accumalated_cost 
SCORES["iteration_model"]["min_cost"] = FLEET_MIN.accumalated_cost
SCORES["iteration_model"]["max_cost"] = FLEET_MIN.accumalated_cost
SCORES["iteration_model"]["avg_cost"] = SCORES["iteration_model"]["total_cost"] / TEST_ITERATIONS

SCORES["gradient_model"]["total_cost"]+= FLEET_MIN.accumalated_cost 
SCORES["gradient_model"]["min_cost"] = FLEET_MIN.accumalated_cost
SCORES["gradient_model"]["max_cost"] = FLEET_MIN.accumalated_cost
SCORES["gradient_model"]["avg_cost"] = SCORES["gradient_model"]["total_cost"] / TEST_ITERATIONS

SCORES["iteration_gradient_model"]["total_cost"]+= FLEET_MIN.accumalated_cost 
SCORES["iteration_gradient_model"]["min_cost"] = FLEET_MIN.accumalated_cost
SCORES["iteration_gradient_model"]["max_cost"] = FLEET_MIN.accumalated_cost
SCORES["iteration_gradient_model"]["avg_cost"] = SCORES["iteration_gradient_model"]["total_cost"] / TEST_ITERATIONS



#--------------GRADIENT TEST -------------------------

#--------------MULTIPLE ITERATION + GRADIENT TEST -------------------------

#--------------GENETIC ALGORITHM -----------------------------------