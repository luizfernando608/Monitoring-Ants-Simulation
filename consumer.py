#%%
from sqlalchemy import MetaData, and_, create_engine, update, insert, select
from celery import Celery
from colorama import Fore, Style
from celery.signals import worker_init, after_task_publish, task_postrun, task_prerun, worker_shutdown

def print_red(text:str):
    print(Fore.BLUE + str(text)+ Style.RESET_ALL)


#%%
app = Celery("tasks")
app.broker_connection('amqps://b-ee432138-0b79-4f52-885d-19d4d18361d7.mq.us-east-1.amazonaws.com:5671',
                      userid="allc", password='formigueiro123')

#%%
@worker_init.connect
def init_worker(**kwargs):
    print_red("Worker initialized")
    global engine
    global meta
    engine = create_engine(f"{database_type}://{user_database}:{password}@{hostname}:{port}/{database_name}")
    meta = MetaData(bind=engine)
    MetaData.reflect(meta)
    print_red("Comecei")



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
             status=status))
     
     engine.execute(insert_scenario)
     return True

def insert_anthill(food_quantity:int,scenario_id:str, id=str)->bool:
    anthill = meta.tables['anthill']
    insert_anthill=(
        insert(anthill).
        values(
            id=id,
            food_quantity=food_quantity,
            scenario_id=scenario_id
        )
    )
    engine.execute(insert_anthill)
    return True


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
    )

    engine.execute(insert_ant)
    return True

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
    return True

def does_scenario_exists(id_scenario:str, meta)->bool:
    scenario_instance = meta.tables['scenario']
    scenario_instance_query = (select([scenario_instance.c.id]).where(scenario_instance.c.id == id_scenario))
    ids_scenario_instance = engine.execute(scenario_instance_query).fetchall()
    if len(ids_scenario_instance) == 0:
        return False
    else:
        return True

@app.task
def publish_data(data:dict):
    # VERIFY IF EXIST SCENARIO
    scenario_exist = does_scenario_exists(data['id_scenario_instance'], meta)
    print_red("scenario_exist: " + str(scenario_exist))
    if not scenario_exist:
        insert_scenario(id = data['id_scenario_instance'],
                        ants_quantity = len(data['ants_info']), 
                        total_food = data['total_food'], 
                        map_food = data['map_food'], 
                        elapsed = data['elapsed'],
                        status=0)

        print_red("Foi até scenario")
        insert_anthill(id ="A",
                       food_quantity = data['anthill_food'], 
                       scenario_id = data['id_scenario_instance'])

        print("Foi até anthill")

        for i in range(len(data['ants_info'])):
            ant = data['ants_info'][i]
            insert_ant( id=i,
                        scenario_id=data['id_scenario_instance'],
                        status=ant['status'], 
                        total_food=ant['total_food'], 
                        anthill_id= "A")
        
        print_red("Foi até ant")
        
    else:
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

