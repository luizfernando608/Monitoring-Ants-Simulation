#%%
from sqlalchemy import MetaData, and_, create_engine, update, insert, select
from celery import Celery
from colorama import Fore, Back, Style

from billiard import current_process

def print_blue(text:str):
    print(Fore.BLUE + str(text)+ Style.RESET_ALL)



#### DATABASE CONNECTION
database_type = "postgresql"
user_database = "ympevcvwzchqwr"
password  = "34d49e45118ea441d83d827b2c4cb63831f8ec847444a950c53b5b2232c87996"
hostname = "ec2-34-198-186-145.compute-1.amazonaws.com"
port = "5432"
database_name = "d6rl9e5tvp50sh"
engine = create_engine(f"{database_type}://{user_database}:{password}@{hostname}:{port}/{database_name}")
meta = MetaData(bind=engine)
MetaData.reflect(meta)



#%%
app = Celery('tasks', broker='amqp://localhost')



def insert_scenario(id:int,ants_quantity:int,total_food:int,map_food:int,elapsed:float,status:str)-> int:
     scenario = meta.tables['scenario']
     insert_scenario = (
         insert(scenario).
         values(
             id = id,
             ants_quantity=ants_quantity,
             total_food=total_food,
             map_food=map_food,
             elapsed=elapsed,
             status=status
         )
     ).returning(scenario.c.id)
     
     id_scenario = engine.execute(insert_scenario)
     return id_scenario.fetchone()[0]

def insert_anthill(food_quantity:int,scenario_id:str, id=str)->bool:
    anthill = meta.tables['anthill']
    insert_anthill=(
        insert(anthill).
        values(
            id=id,
            food_quantity=food_quantity,
            scenario_id=scenario_id
        )
    ).returning(anthill.c.id)
    id_anthill = engine.execute(insert_anthill)
    return id_anthill.fetchone()[0]


def insert_ant(id, status:int,total_food:int,anthill_id:str,scenario_id)->bool:
    ant = meta.tables['ant']
    insert_ant=(
        insert(ant).
        values(
            id=id,
            scenario_id=scenario_id,
            anthill_id=anthill_id,
            status=status,
            total_food=total_food
        )    
    ).returning(ant.c.id)

    id_ant = engine.execute(insert_ant)
    return id_ant.fetchone()[0]

def update_scenario(id:str,total_food:int,map_food:int,elapsed:float,status:str,ants_quantity:int)-> bool:
    scenario = meta.tables["scenario"]
    update_scenario_status = (
         update(scenario).
         where(scenario.c.id == id).
         values(
             id = id,
             ants_quantity=ants_quantity,
             total_food=total_food,
             map_food=map_food,
             elapsed=elapsed,
             status=status
        )
     )
    engine.execute(update_scenario_status)
    return True

def update_antihill(id_scenario:str,food_quantity:int, id_anthill="A")->bool:
    anthill = meta.tables['anthill']
    scenario = meta.tables['scenario']
    update_anthill = (
        update(anthill).
        where(and_(scenario.c.id == id_scenario,anthill.c.id==id_anthill)).
        values(
            food_quantity = food_quantity
        )
    )
    
    engine.execute(update_anthill)
    return True

def update_ant(id:str,id_scenario,status:str,total_food:int,id_anthill="A")->bool:
    ant = meta.tables['ant']
    anthill = meta.tables['anthill']
    scenario = meta.tables['scenario']
    update_ant = (
        update(ant).
        where(and_(ant.c.id==id, scenario.c.id==id_scenario, anthill.c.id==id_anthill)).
        values(
            status = status,
            total_food = total_food
        )
    )
    engine.execute(update_ant)
    return True


@app.task(bind=True)
def publish_data(self, data:dict):
    # VERIFY IF EXIST SCENARIO
    scenario_instance = meta.tables['scenario']
    scenario_instance_query = (select([scenario_instance.c.id]).where(scenario_instance.c.id == data['id_scenario_instance']))
    ids_scenario_instance = engine.execute(scenario_instance_query).fetchall()
    
    print_blue(ids_scenario_instance)
    if len(ids_scenario_instance) == 0:
        print("publish data")
        id_scenario = insert_scenario(
                        id = data['id_scenario_instance'],
                        ants_quantity = len(data['ants_info']), 
                        total_food = data['total_food'], 
                        map_food = data['map_food'], 
                        elapsed = data['elapsed'],
                        status=0) 

        id_anthill = insert_anthill(
                        id ="A",
                        food_quantity = data['anthill_food'], 
                        scenario_id = id_scenario)

        for i in range(len(data['ants_info'])):
            ant = data['ants_info'][i]
            id_ant = insert_ant( 
                            id=i,
                            scenario_id=data['id_scenario_instance'],
                            status=ant['status'], 
                            total_food=ant['total_food'], 
                            anthill_id= "A")
            

    else:
        print("update data")
        
        update_scenario(
                        id=data["id_scenario_instance"],
                        status=data["status"],
                        elapsed=data["elapsed"],
                        map_food=data["map_food"],
                        total_food=data["total_food"],
                        ants_quantity=len(data["ants_info"])
                        ) #status
        
        update_antihill(
                        id_scenario=data["id_scenario_instance"],
                        food_quantity=data['anthill_food'])

        for i in range(0,len(data['ants_info'])):
            ant = data['ants_info'][i]
            update_ant(id=i, status= data['status'], total_food= data['total_food'], id_scenario=data["id_scenario_instance"])
        


start_data = {'id_scenario_instance' : 6,
            'elapsed': 0.0, 
            'status': 'executing', 
            'total_food': 151, 
            'map_food': 151, 
            'anthill_food': 10, 
            'ants_info': [
                {'status': 1, 'total_food': 0}, 
                {'status': 0, 'total_food': 0}]}






#%%


# @app.task
# def insert_scenario(status:str, tempo_execucao:float, quantidade_total_comida:int)-> bool:
#     scenario = meta.tables['cenario']
#     insert_scenario = (
#         insert(scenario).
#         values(
#             status=status,
#             tempo_execucao=tempo_execucao,
#             quantidade_total_comida=quantidade_total_comida
#         )
#     )
#     engine.execute(insert_scenario)
#     return True

# @app.task
# def insert_antihill(quantidade_comida:int, quantidade_formiga_carregando:int, quantidade_formiga_procurando:int, maximo_carregado_formiga:int, id_cenario:int):
#     antihill = meta.tables['formigueiro']
#     insert_antihill= (
#     insert(antihill).
#     values(
#         quantidade_comida=quantidade_comida,
#         quantidade_formiga_carregando=quantidade_formiga_carregando,
#         quantidade_formiga_procurando=quantidade_formiga_procurando,
#         maximo_carregado_formiga=maximo_carregado_formiga,
#         id_cenario=id_cenario)
#     )
#     engine.execute(insert_antihill)
#     return True


# @app.task
# def update_scenario_status(id_scenario:int ,status:str, tempo_execucao:float=0)->bool:
#     scenario = meta.tables["cenario"]
#     update_scenario_status = (
#         update(scenario).
#         where(scenario.c.id_cenario == id_scenario).
#         values(status=status,
#             tempo_execucao=tempo_execucao)
#     )
#     engine.execute(update_scenario_status)
#     return True


# #%%
# @app.task
# def update_scenario_food(id_scenario:int, total_comida:int)->bool:
#     scenario = meta.tables["cenario"]
#     update_scenario_quantidade_comida = (
#         update(scenario).
#         where(scenario.c.id_cenario == id_scenario).
#         values(quantidade_total_comida=total_comida)
#     )
#     engine.execute(
#         update_scenario_quantidade_comida
#     )
#     return True

# #%%
# @app.task
# def update_antihill(id_antihill:int,quantidade_comida:int, quantidade_formiga_carregando:int, quantidade_formiga_procurando:int, maximo_carregado_formiga:int, id_cenario:int)->bool:
#     anthill = meta.tables["formigueiro"]
#     update_antihill = (
#         update(anthill).
#         where(anthill.c.id_formigueiro == id_antihill).
#         values(
#             quantidade_comida=quantidade_comida,
#             quantidade_formiga_carregando=quantidade_formiga_carregando,
#             quantidade_formiga_procurando=quantidade_formiga_procurando,
#             maximo_carregado_formiga = maximo_carregado_formiga,
#             id_cenario=id_cenario
#         )
#     )
#     engine.execute(update_antihill)