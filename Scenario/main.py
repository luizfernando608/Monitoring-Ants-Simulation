#%%
import random
from turtle import position 
import numpy as np
import time
import debugpy

class Pheromone:
    def __init__(self, food_position, life_time = 30):
        self.life_time = life_time
        self.food_position = food_position
    def decrease_pheromone_life(self):
        self.life_time -= 1
        
    
class Map():
    def __init__(self) -> None:
        # self.x_dim = random.randint(5,10)
        # self.y_dim = random.randint(5,10)

        # temp code
        self.x_dim = 5
        self.y_dim = 5

        self.anthill_position = {}
        self.map = np.zeros((self.y_dim ,self.x_dim ),dtype=object)

        # self.anthill_position = self.set_anthill()
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
        position_x = random.randint(0,self.x_dim-1 )
        position_y = random.randint(0,self.y_dim-1 )

        self.map[position_y,position_x] = label
        
        self.anthill_position[label] = (position_y,position_x)
        # return (position_y,position_x)

    def set_food(self): 
        position_x = random.randint(0,self.x_dim-1 )
        position_y = random.randint(0,self.y_dim-1 )

        while self.map[position_y,position_x] != 0:
            position_x = random.randint(0,self.x_dim-1)
            position_y = random.randint(0,self.y_dim-1)

    
        self.map[position_y,position_x] = "F"
        return (position_y,position_x)
        
    def set_pheromone(self,y,x): 
        if self.map[y,x] not in (["F"] + list(self.anthill_position.keys())):
            
            if self.map[y,x] >= 0:
                self.map[y,x] = 30 #set or reset phe

            if (y,x) not in self.pheromones:
                self.pheromones.append((y,x))
        
    def decrease_food(self):

        if self.food_quantity > 1:
            # drop food
            self.food_quantity -= 1

        elif self.food_quantity == 1:
            # reset food
            self.food_quantity = self.inicial_food_quantity
            self.food_position = self.set_food()
        


    def decrease_pheromone(self):

        for phe in self.pheromones:

            self.map[phe[0],phe[1]] -= 1

            if self.map[phe[0],phe[1]] == 0:
                self.pheromones.remove((phe[0],phe[1]))



class Ant():
    def __init__(self,mapa, label_antihill) -> None:
        self.map = mapa
        # position
        self.x_pos = random.randint(0,mapa.x_dim-1)
        self.y_pos = random.randint(0,mapa.x_dim-1)
        self.antihill = label_antihill
        self.antihill_position = mapa.anthill_position[self.antihill]
        self.status = 0
        # status = 0 : procurando comida/feromonio
        # status = 1 : indo até a comida
        # status = 2 : levando comida para casa
        # status = 3 : indo ate feromonio
        # status = 4 : indo até comida com o feromonio

        # total food caried to anthill
        self.total_food = 0

        # self.field_vision = random.randint(1,4)
        # temp code
        self.field_vision = 1

        self.carring = False

        self.food_position = None
        self.pheromone_postion = None

    def generrate_new_pos(self):
        print("generrate new pos")
        # generate random direction
        direction_x = random.randint(-1,1)
        direction_y = random.randint(-1,1)
        

        # new position
        test_position_x = self.x_pos + direction_x
        test_position_y = self.y_pos + direction_y

        return test_position_x, test_position_y


    def random_move(self): 
        print("random move")
        
        if self.check_position():
            return

        test_position_x, test_position_y = self.generrate_new_pos()

        # new position cant be bigger than map dimensions 
        while (test_position_x > self.map.x_dim-1 or test_position_y > self.map.y_dim-1
                or 
                test_position_x < 0 or test_position_y < 0):

             test_position_x, test_position_y = self.generrate_new_pos()
        self.x_pos = test_position_x
        self.y_pos = test_position_y


    def move_target(self, target_y, target_x,):
        # Move na direção de um alvo
        print("move target")
        direction_x = target_x -self.x_pos
        if direction_x < 0:
            direction_x = -1
        elif direction_x > 0:
            direction_x = 1
        elif direction_x == 0:
            direction_x = 0
        direction_y = target_y - self.y_pos
        
        if  direction_y < 0:
            direction_y = -1
        elif direction_y > 0:
            direction_y = 1
        elif direction_y == 0:
            direction_y = 0
                    
        self.x_pos += direction_x
        self.y_pos += direction_y
        
        


    def check_position(self):
        # checar se posicao atual ou aredores possui feromonio, casa ou comida
        # atualizar status
        print("Check Position")
        
        y_start = self.y_pos - self.field_vision
        x_start = self.x_pos - self.field_vision
        if y_start < 0:
            y_start = 0
        if x_start < 0:
            x_start = 0
        
        y_final = self.y_pos + self.field_vision+1
        x_final = self.x_pos + self.field_vision+1
        if y_final > self.map.y_dim-1:
            y_final = self.map.y_dim
        if x_final > self.map.x_dim-1:
            x_final = self.map.x_dim
        debugpy.breakpoint()
        ### CHECANDO SE TEM FEROMONIO
        for pheromone in self.map.pheromones:
            if pheromone[0] >= y_start and pheromone[0] <= y_final:
                if pheromone[1] >= x_start and pheromone[1] <= x_final:
                    print("Eu vi feromonio")
                    self.status = 3
                    self.pheromone_postion = pheromone
                    

        ### CHECANDO SE POSSUI COMIDA        
        for y in range(y_start,y_final):
            for x in range(x_start,x_final):
                if self.map.map[y,x] == "F":
                    print("Eu vi comida")
                    self.status = 1
                    self.food_position = np.array([y,x]).copy()
                    return True
        pass

    
    def go_food(self):
        # Vê comida e vai até ela
        print("go food")
        self.move_target(self.food_position[0], self.food_position[1])
        if self.y_pos == self.food_position[0] and self.x_pos == self.food_position[1]:
            self.status = 2
            self.total_food += 1
            # self.food_position = None
            self.map.decrease_food()
            return
        pass
    
    def pheromone_move(self): 
        self.go_food()
        pass

    def go_pheromone(self):
        # Vê o feromonio e vai até ele
        print("go pheromone")
        self.move_target(self.pheromone_postion[0], self.pheromone_postion[1])
        if self.y_pos == self.pheromone_postion[0] and self.x_pos == self.pheromone_postion[1]:
            self.status = 4
            self.pheromone_postion = None
            return
        pass

    def go_home(self): 
        # ir até a casa
        print("go home")
        self.map.set_pheromone(self.y_pos, self.x_pos)
        self.move_target(self.antihill_position[0], self.antihill_position[1])
        
        if self.y_pos == self.antihill_position[0] and self.x_pos == self.antihill_position[1]:
            self.check_position()
            return
        pass

    def drop_pheromone(self):
        # Solta feromonio pelo mapa 
        self.map.set_pheromone(self.x_pos,self.y_pos)

    def get_food(self): 
        self.map.decrease_food()

    def routine(self):
        # rotina da formiga
        print("Ants position",self.y_pos, self.x_pos)
        
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


def show_map():
    positions = {}
    for formiga in formigas:
        (y,x) = formiga.y_pos, formiga.x_pos
        positions[y] = x

    mapa2d = ""
    for y_axis in  range(mapa.y_dim):
        for x_axis in range(mapa.x_dim):
            if y_axis in positions and positions[y_axis] == x_axis:
                mapa2d += "\033[2;31;43m" +str(mapa.map[y_axis,x_axis])+"\033[0;0m "
            else:
                mapa2d += str(mapa.map[y_axis,x_axis])
                mapa2d += " "
        
        mapa2d += "\n"

    print(rf"{mapa2d}")

mapa = Map()
mapa.set_anthill("A")
formigas = []
NUM_FORMIGAS = 1

for num in range(NUM_FORMIGAS):
    formigas.append(Ant(mapa, "A"))

# print(mapa)

show_map()
#%%
for formiga in formigas:
    formiga.routine()

show_map()

#%%




#################### IGNORE (for now) ####################
# class Simulation():
#     def __init__(self) -> None:

#         self.start_time = time.time()
#         self.mapa = Map()  #generate map

#         #generate ants
#         self.number_of_ants = random.randint(5,100)
#         self.ants = []

#         self.CONDICAO_VENCIMENTO = self.mapa.inicial_food_quantity*10/self.number_of_ants


#         for ant in range(self.number_of_ants):
#             self.ants.append(Ant(self.mapa))

#         self.report(cur_status="new")


#     def report(self,cur_status="executing"):

#         time = time.time()
#         status = cur_status
#         ants = [{"status":i.status,"total_food":i.total_food} for i in self.ants]
#         anthill_food = self.mapa.anthill_food
#         map_food = self.map.food_quantity
        

#     def run(self):  
#         while self.mapa.anthill_food != self.QUANTIDADE_VENCIMENTO: 

#             # 1 time unid = all ants run 
#             for ant in self.ants:
#                 ant.routine() 

#             self.mapa.decrease_pheromone() # decreased pheromone lifetime in all map
#             self.report()
        
#         self.report(cur_status="dead")

# %%
