#%%
from tracemalloc import start
from sqlalchemy import MetaData, and_, create_engine, update, insert, select
from celery import Celery
from colorama import Fore, Back, Style
from celery.signals import worker_process_init, worker_process_shutdown

from billiard import current_process

def print_blue(text:str):
    print(Fore.BLUE + str(text)+ Style.RESET_ALL)

#### DATABASE POSTGRES CONNECTION
database_type = "postgresql"
user_database = "ympevcvwzchqwr"
password  = "34d49e45118ea441d83d827b2c4cb63831f8ec847444a950c53b5b2232c87996"
hostname = "ec2-34-198-186-145.compute-1.amazonaws.com"
port = "5432"
database_name = "d6rl9e5tvp50sh"


#### DATABASE POSTGRESS LOCAL CONNECTION
# database_type = "postgresql"
# user_database = "postgres"
# password  = "1234"
# hostname = "localhost"
# port = "5432"
# database_name = "ants"



#%%
app = Celery('tasks', broker='amqp://localhost')

@worker_process_init.connect
def init_worker(**kwargs):
    global engine
    global meta
    engine = create_engine(f"{database_type}://{user_database}:{password}@{hostname}:{port}/{database_name}")
    meta = MetaData(bind=engine)
    MetaData.reflect(meta)
    print_blue("Comecei")

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
        where(and_(anthill.c.scenario_id == id_scenario, 
                   anthill.c.id=="A")).
        values(
            food_quantity = food_quantity
        )
    )
    
    engine.execute(update_anthill)
    return True


def update_ants(ants_info:list, scenario_id:str):
    ant_table = meta.tables['ant']
    anthill_table = meta.tables['anthill']
    scenario_table = meta.tables['scenario']
    with engine.begin() as conn:
        for i, ant in enumerate(ants_info):    
            update_ant = (
                update(ant_table).
                where(and_(ant_table.c.id==i, 
                           ant_table.c.scenario_id==scenario_id, 
                            ant_table.c.anthill_id=="A")).
                values(
                    status = ant['status'],
                    total_food = ant['total_food']))
        
        conn.execute(update_ant)
        

@app.task
def publish_data(data:dict):
    # VERIFY IF EXIST SCENARIO
    scenario_instance = meta.tables['scenario']
    scenario_instance_query = (select([scenario_instance.c.id]).where(scenario_instance.c.id == data['id_scenario_instance']))
    ids_scenario_instance = engine.execute(scenario_instance_query).fetchall()
    
    print_blue(ids_scenario_instance)
    if len(ids_scenario_instance) == 0:
        print("publish data")
        insert_scenario(
                        id = data['id_scenario_instance'],
                        ants_quantity = len(data['ants_info']), 
                        total_food = data['total_food'], 
                        map_food = data['map_food'], 
                        elapsed = data['elapsed'],
                        status=0) 

        insert_anthill(
                        id ="A",
                        food_quantity = data['anthill_food'], 
                        scenario_id = data['id_scenario_instance'])

        for i in range(len(data['ants_info'])):
            ant = data['ants_info'][i]
            insert_ant( 
                        id=i,
                        scenario_id=data['id_scenario_instance'],
                        status=ant['status'], 
                        total_food=ant['total_food'], 
                            anthill_id= "A")
            

    else:
        print("update data")
        print("update scenario")
        update_scenario(
                        id=data["id_scenario_instance"],
                        status=data["status"],
                        elapsed=data["elapsed"],
                        map_food=data["map_food"],
                        total_food=data["total_food"],
                        ants_quantity=len(data["ants_info"])
                        ) #status
        print("update anthill")
        update_antihill(
                        id_scenario=data["id_scenario_instance"],
                        food_quantity=data['anthill_food'])
       
        print("update ants")
        update_ants(data['ants_info'], data['id_scenario_instance'])        

