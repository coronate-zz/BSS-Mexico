
import random
import pandas as pd 
import numpy as np  

import random
import pandas as pd 
import numpy as np  
from tqdm import tqdm




class Map(object):
    def __init__(self, num_estaciones, num_estados):
        #TO DO: use bycicle_slots_cost and parking_slots_cost 
        #to upadte self.weights
        self.distances = mapaAleatorio( num_estaciones, num_estados)
        self.available_stations = list(self.distances.columns)
        self.parking_slots_cost = list()
        self.bycicle_slots_cost = list()
        self.weights = self.calculateWeights()
    def __repr__(self):
        print("\nMap: \n\tmatrix\n\t available_stations \
         \n\t parking_slots_cost \n\t bycicle_slots_cost\n\t distances,weights: matrix")

    def update_available_stations( self, FLEET):
        # For all car it remove from available_stations list all the spots in which cars
        #are allocated the it remove the already-route-assigned stations.
        for i in FLEET.fleet:
            car = FLEET.fleet[i]
            if car.position in self.available_stations:
                self.available_stations.remove(car.position)
            for occupied_area_stations in car.area:
                if occupied_area_stations in self.available_stations:
                    self.available_stations.remove(occupied_area_stations)

    def calculateWeights(self):
        """
        In this function we use all the available infromation to represent the expected cost
        of traveling from stattion A to station B

        for i in self.distances.columns:
            for j in self.distances.columns:
                distance =  self.distance.loc[i,j]
                parking_cost = self.parking_slots_cost[j]
                bycicle_cost = self.bycicle_slots_cost[j]

                weight = bycicle_cost + parking_cost + distances
        """
        return  self.distances #En lo que encontramos una funcion que represente
        
        
class Fleet(object):
    """
    This class cointain all the vehicles that perform that allocate the bycles to
    each station.
    """
    global MAX_COBERTURE, AREA_SIZE

    def __init__(self):
        self.fleet = dict()

    def insertCar (self,car):
        self.fleet[car.id_car] = car

    def __repr__(self):
        repr_str = "\n\t---------PRINTING FLEET--------------"
        cont = 0
        for i in self.fleet:
            repr_str = print(i)
        return repr_str
    def update_carsPosition(self ):
        """
        Returns a list with the position of each car so this station can be deleated
        from available spots
        """
        self.positions = list()
        for car in self.fleet:
            self.positions.append(self.fleet[car].position)

    def assignArea(self,MAP):
        """
        For each car we select randomly a station inside their coberture area
        to be taken in consideration for rebalancing. This process is repeated
        until each car has AREA_SIZE assiged stations.
        """
        for i in range(AREA_SIZE): #number of statitions assigned to each car
            print("---------------------------NEXT AREA--------------------------------".format(i))
            for j in random.sample(self.fleet.keys(), len(self.fleet.keys())): #car are selected randomly
                print("----------------------------FLEET KEY------------------------------".format(j))
                car = self.fleet[j]
                #For each car we want to know which stations it can visit
                car_stations = MAP.weights[car.position] #row in weight matriz
                
                car_stations = car_stations[MAP.available_stations] #select just the available stations
                print("TEST 1:  \n{}".format(car_stations))
                car_stations_weights = self.car_cost(car, car_stations) #for this particular car how expensive is to travel from it's possition to all available stations
                car.set_stations_weight( car_stations_weights )
                print("TEST 1.1:  \n{}".format(car_stations_weights))

                car_possible_area = car_stations_weights[car_stations_weights <= MAX_COBERTURE]
                print("TEST 2:  \n{}".format(car_possible_area))

                if len(car_possible_area) > 0:
                    car_select = random.choice(car_possible_area.index)
                    car.set_area(car_select)
                    print("TEST 3 car select: \n{}".format(car_select))
                    #We have to take out the selected station from the available list
                    MAP.update_available_stations(self)
                    print("TEST 4 available_stations: \n{}".format(MAP.available_stations))
                else:
                    print("Not available stations for car \n{} ".format(j))

        print("END Area assignation")

    def car_cost(self,car,car_stations, ):
        """
        This function user the Car information to upadate the cost
        for a paricular car C to travel to station J. Taking into account 
        the size of the car.
        """
        car_cost = car.capacity # Aqui le deberiamos aumentar el peso
        #de acuerdo a la capacidad del carro y la cantidad de lugares 
        #en la estacion
        return car_stations

class Car(object):
    """docstring for ClassName"""
    def __init__(self, id_car, position, capacity):
        self.id_car = id_car
        self.position = position
        self.capacity = capacity
        self.area = list()
        self.car_stations_weights = np.nan
    def __repr__(self):
         return "CLASS Car: \n\tposition \n\tcapacity\n\tnumber\n\tarea\n\tcar_stations_weight\n\n "
    def __str__(self):
         return "CLASS Car: \n\tid_car: {}\n\tposition: {} \n\tcapacity: {}\
         \n\tcar_stations_weight: {}\n\narea: \n\t\t{}\n\n".format(self.id_car, \
            self.position, self.capacity, self.car_stations_weights, self.area)

    def set_stations_weight(self,car_stations_weights):
        """
        The weight from traveling from station A to B change depending on
        the car that is performing that trip.
        """
        self.car_stations_weights = car_stations_weights
    def set_area(self,area):
        if len(self.area) ==0:
            self.area = [area]
        else:
            self.area.append(area)


AREA_SIZE = 8
MAX_COBERTURE = 5
N_CARS = 5
N_STATES = 5
N_STATIONS = 40
MAX_COBERTURE = 8

"""
Note that N_STATIONS <= N_CARS * AREA_SIZE
"""


MAP = Map(N_STATIONS, N_STATES)
FLEET = Fleet()
# We assign a random station for each car
car_position = random.sample( list(MAP.weights.columns) , N_CARS)

for i in range(N_CARS):
    id_car = i
    position = car_position[i]
    capacity = random.randint(5,20) #TO DO: each car have their on capcity

    car = Car( id_car, position, capacity )
    FLEET.insertCar(car)

FLEET.update_carsPosition()
MAP.update_available_stations(FLEET)
FLEET.assignArea(MAP)





