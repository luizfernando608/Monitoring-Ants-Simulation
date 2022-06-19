"""
Generates te ants simulation and sent messages to the publisher
"""
import random
import numpy as np
from time import time, sleep
from consumer import publish_data
import uuid
from colorama import Fore, Style

def print_blue(text:str):
    print(Fore.BLUE + str(text)+ Style.RESET_ALL)

class Pheromone:
    def __init__(self, food_position, label_antihill, life_time = 20,):
        self.default_life_time = life_time
        self.life_time = life_time
        self.food_position = food_position
        self.antihill = label_antihill
        
    def decrease_pheromone_life(self):
        self.life_time -= 1
    
    def __str__(self):
        return str(self.life_time)
    

class Map():
    def __init__(self) -> None:

        self.x_dim = random.randint(5,10)
        self.y_dim = random.randint(5,10)

        self.anthill_position = {}
        self.map = np.zeros((self.y_dim ,self.x_dim ),dtype=object)
        
        self.anthill_food = 0

        self.food_position = self.set_food()
        self.inicial_food_quantity = random.randint(0,200)
        self.food_quantity = self.inicial_food_quantity

        self.pheromones = []
    
    def __str__(self) -> str:
        mapa = ""
        for y in self.map:
            for x in y:
                mapa += str(x) + " "
            mapa += '\n'
        return mapa

    def set_anthill(self, label): 
        position_x = 0
        position_y = 0
    
        self.map[position_y,position_x] = label
        
        self.anthill_position[label] = (position_y,position_x)

    def set_food(self): 
        position_x = random.randint(0,self.x_dim-1 )
        position_y = random.randint(0,self.y_dim-1 )

        while self.map[position_y,position_x] != 0:
            position_x = random.randint(0,self.x_dim-1)
            position_y = random.randint(0,self.y_dim-1)

    
        self.map[position_y,position_x] = "F"
        return (position_y,position_x)
        
    def set_pheromone(self,y,x, food_position, label_antihill): 
        if self.map[y,x] not in (["F"] + list(self.anthill_position.keys())):
            if type(self.map[y,x]) != Pheromone:
                self.map[y,x] = Pheromone(food_position, label_antihill)
            else:
                self.map[y,x].life_time = self.map[y,x].default_life_time
            
            if (y,x) not in self.pheromones:
                self.pheromones.append((y,x))
        
    def decrease_food(self):

        if self.food_quantity > 1:
            self.food_quantity -= 1  # drop food

        elif self.food_quantity == 1:
            self.food_quantity -= 1

            #reset food
            self.map[self.food_position[0],self.food_position[1]] = 0
            self.food_quantity = self.inicial_food_quantity
            self.inicial_food_quantity += self.inicial_food_quantity
            self.food_position = self.set_food()

        
    def decrease_pheromone(self):

        for phe in self.pheromones:

            self.map[phe[0],phe[1]].decrease_pheromone_life()

            if self.map[phe[0],phe[1]].life_time == 0:
                self.pheromones.remove(phe)
                self.map[phe[0],phe[1]] = 0


class Ant():
    def __init__(self,mapa, label_antihill) -> None:
        self.map = mapa
        self.x_pos = random.randint(0,mapa.x_dim-1)
        self.y_pos = random.randint(0,mapa.x_dim-1)
        self.antihill = label_antihill
        self.antihill_position = mapa.anthill_position[self.antihill]
        self.dropping = False

        self.status = 0
        # status = 0 : procurando comida/feromonio
        # status = 1 : indo até a comida
        # status = 2 : levando comida para casa
        # status = 3 : indo ate feromonio
        # status = 4 : indo até comida com o feromonio

        self.total_food = 0
        self.field_vision = random.randint(1,4)
        self.food_position = None
        self.pheromone_postion = None

    def generrate_new_pos(self):
        direction_x = random.randint(-1,1)
        direction_y = random.randint(-1,1)
        
        test_position_x = self.x_pos + direction_x
        test_position_y = self.y_pos + direction_y
        if test_position_x > self.map.x_dim-1:
            test_position_x = self.map.x_dim-1
        elif test_position_x < 0:
            test_position_x = 0
        if test_position_y > self.map.y_dim-1:
            test_position_y = self.map.y_dim-1
        elif test_position_y < 0:
            test_position_y = 0

        return test_position_x, test_position_y


    def random_move(self): 
        if self.check_position(): return
        test_position_x, test_position_y = self.generrate_new_pos()
        self.x_pos = test_position_x
        self.y_pos = test_position_y


    def move_target(self, target_y, target_x, inverse_order = False):
        direction_x = target_x -self.x_pos
        direction_y = target_y - self.y_pos
        
        if inverse_order:
            temp_x = direction_x
            direction_x = direction_y
            direction_y = temp_x

        # Moving like manhatan
        if direction_x != 0:
            direction_y = 0 
            if direction_x < 0:
                direction_x = -1
            elif direction_x > 0:
                direction_x = 1
        else: 
            direction_x = 0 
        

        if direction_y < 0:
            direction_y = -1
        elif direction_y > 0:
            direction_y = 1
        elif direction_y == 0:
            direction_y = 0

        if inverse_order:
            temp_x = direction_x
            direction_x = direction_y
            direction_y = temp_x

        self.x_pos += direction_x
        self.y_pos += direction_y
        
        


    def check_position(self):
        """
        Check for pheromone or food in ant field of vision
        """

        y_start = self.y_pos - self.field_vision
        x_start = self.x_pos - self.field_vision

        if y_start < 0: y_start = 0
        if x_start < 0: x_start = 0
        
        y_final = self.y_pos + self.field_vision+1
        x_final = self.x_pos + self.field_vision+1

        if y_final > self.map.y_dim-1:  y_final = self.map.y_dim
        if x_final > self.map.x_dim-1:  x_final = self.map.x_dim

        # check for pheromone
        for pheromone in self.map.pheromones:
            if pheromone[0] >= y_start and pheromone[0] <= y_final:
                if pheromone[1] >= x_start and pheromone[1] <= x_final:
                    self.status = 3
                    self.pheromone_postion = pheromone
                    
        # check for food
        for y in range(y_start,y_final):
            for x in range(x_start,x_final):
                if self.map.map[y,x] == "F":
                    self.status = 1
                    self.food_position = np.array([y,x]).copy()
                    return True

        return False
        

    
    def go_food(self):
        """
        Go get food
        """
        
        self.move_target(self.food_position[0], self.food_position[1])

        if (self.y_pos == self.food_position[0] and self.x_pos == self.food_position[1]):
            if (self.map.map[self.y_pos,self.x_pos]=="F"):
                # reched food
                self.map.decrease_food()
                self.status = 2
                self.total_food += 1
                self.dropping = True
            else:
                self.check_position()
                self.dropping = False
         
    
    def pheromone_move(self): 
        """
        Follow the pheromone trail 
        """

        try:
            self.food_position = self.map.map[self.y_pos,self.x_pos].food_position
        except:
            self.status = 0
            self.dropping = False
            self.random_move()
            return 

        self.move_target(self.food_position[0], self.food_position[1], inverse_order=True)
        
        if (self.y_pos == self.food_position[0] and self.x_pos == self.food_position[1]):
            if (self.map.map[self.y_pos,self.x_pos]=="F"):
                self.map.decrease_food()
                self.status = 2
                self.total_food += 1
                self.dropping = True
                return
            else:
                self.check_position()
                self.dropping = False
        

    def go_pheromone(self):

        self.move_target(self.pheromone_postion[0], self.pheromone_postion[1])

        if self.y_pos == self.pheromone_postion[0] and self.x_pos == self.pheromone_postion[1]:
            self.status = 4
            self.pheromone_postion = None
            return
        

    def go_home(self): 
        if self.dropping:
            self.map.set_pheromone(self.y_pos, self.x_pos, self.food_position,self.antihill)
        
        self.move_target(self.antihill_position[0], self.antihill_position[1])
        
        if self.y_pos == self.antihill_position[0] and self.x_pos == self.antihill_position[1]:
            self.map.anthill_food += 1
            self.check_position()
            return
        pass

    def drop_pheromone(self):
        self.map.set_pheromone(self.x_pos,self.y_pos,self.food_position, self.antihill)


    def routine(self):
        
        if self.status == 0:
            self.random_move()
        elif self.status == 1:
            self.go_food()
        elif self.status == 2:
            self.go_home()
        elif self.status == 3:
            self.go_pheromone()
        elif self.status == 4:
            self.pheromone_move()

        self.map.decrease_pheromone()
        
        pass


class SimulationServer():

    def __init__(self) -> None:
        # Generate an unique id for the simulation
        print("Start new simulatio")
        self.id_scenario_instance= str(uuid.uuid4())
        
    
    def StartScenario(self ):
        self.mapa = Map()
        self.mapa.set_anthill("A")

        self.formigas = []
        self.NUM_FORMIGAS = random.randint(10,30)

        for num in range(self.NUM_FORMIGAS):
            self.formigas.append(Ant(self.mapa, "A"))


        ### SEND FIRST DATA ###
        self.start_time = time()
        ants_report = []
        for formiga in self.formigas:
            formiga.routine()
            ants_report.append({"status":formiga.status, "total_food":formiga.total_food})
        
        self.publish(status="start", ants_info=ants_report)

        return True


    def publish(self,status="executing",ants_info=[]): 
        self.data = dict(
                    id_scenario_instance = self.id_scenario_instance,
                    elapsed = time() - self.start_time,
                    status = status,
                    total_food = self.mapa.inicial_food_quantity,
                    map_food = self.mapa.food_quantity,
                    anthill_food = self.mapa.anthill_food,
                    ants_info = ants_info)

        try:
            publish_data.delay(self.data)
        except:
            pass
        
        


    def RunSimulation(self):    
        count = 0
        # while self.mapa.anthill_food <= self.NUM_FORMIGAS*30:
        for i in range(5000):
            ants_report = []

            for formiga in self.formigas:
                formiga.routine()
                ants_report.append({"status":formiga.status, "total_food":formiga.total_food})
        
            
            if i%10 == 0:
                self.publish(ants_info=ants_report, status="executing")

        

        self.publish(status="end", ants_info=ants_report)
        
        

#%%


start_time = time()
print_blue(start_time)
simulation = SimulationServer()
simulation.StartScenario()
print("Scenario started")
simulation.RunSimulation()
print("Scenario ended")

# print("Total time: ", time() - start_time)