
import random
import pandas as pd 
import numpy as np  
import tqdm as tqdm

N_CARS = 15
N_STATES = 10
N_STATIONS = 400
MAX_COBERTURE = 8



class Map(object):
    def __init__(self, num_estaciones, num_estados):
        #TO DO: use bycicle_slots_cost and parking_slots_cost 
        #to upadte self.weights
        self.distances = mapaAleatorio( num_estaciones, num_estados)
        self.available_stations = list(self.distances.columns)
        self.parking_slots_cost = list()
        self.bycicle_slots_cost = list()
        self.weights = self.calculateWeights()

    def update_available_stations( self, FLEET):
        for car in FLEET:
            if car.postion in self.available_stations:
                self.available_stations.remove(car.postion)
            for occupied_area_stations in car.area:
                if occupied_area_stations in self.available_stations:
                    self.available_stations.remove(occupied_area_stations)

    def calculateWeights():
        """
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
    global MAX_COBERTURE, ARE_SIZE

    def __init__(self):
        self.fleet = dict()

    def insertCar (car):
        self.fleet[car.id_car] = car

    def update_carsPosition( ):
        """
        Returns a list with the position in each car so this station can be deleated
        with in the possible assignation spots to perform routes
        """
        self.postions = list()
        for car in self.fleet:
            car.postion.append(car.postion)

    def assignArea(MAP):
        """
        For each car we select randomly a station inside their coberture area
        to be taken in consideration for rebalancing. This process is repeated
        until each car has ARE_SIZE assiged stations.
        """
        for i in tqdm(range(ARE_SIZE)):
            for j in random.sample(self.fleet.keys(), len(self.fleet.keys())):
                car = self.fleet[j]
                #For each car we want to know which stations it can visit
                car_stations = MAP.weights[car.postion]
                car_stations = car_stations[MAP.available_stations]
                car_stations_weights = car_cost(car_stations, car)
                car.set_stations_weight( car_stations_weights )
                car_possible_area = car_stations_weights[car_stations_weights <= MAX_COBERTURE]
                car_select = random.choice(car_possible_area)
                car.set_area(car_select)

                #We have to take out the selected station from the available list
                MAP.update_available_stations()
        print("END Area assignation")

    def car_cost(car_stations):
        """
        This function user the Car information to upadate the cost
        for a paricular car C to travel to station J.
        """
        car_cost = car.capacity # Aqui le deberiamos aumentar el peso
        #de acuerdo a la capacidad del carro y la cantidad de lugares 
        #en la estacion
        return car_stations

class Car(object):
    """docstring for ClassName"""
    def __init__(self, id_car, postion, capacity):
        self.postion = postion
        self.capacity = capacity
        self.number = id_car
    def set_stations_weight(car_stations_weights):
        """
        The weight from traveling from station A to B change depending on
        the car that is performing that trip.
        """
        self.car_stations_weights = car_stations_weights
    def set_area(area):
        self.area = area


ARE_SIZE = 15

MAP = Map(N_STATIONS, N_STATES)
FLEET = Fleet()
car_position = random.sample( list(S.columns) , N_CARS)

for i in N_CARS:
    id_car = i
    postion = car_position[i]
    capacity = random.randint(5,20) #TO DO: each car have their on capcity

    car = Car( id_car, postion, capacity )
    FLEET.insertCar(car)

FLEET.update_carsPosition()
MAP.update_available_stations(FLEET)
FLEET.assignArea(MAP)



