#%%
from sqlalchemy import MetaData, create_engine, update, insert
from celery import Celery


#%%

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

#%%
def insert_scenario(ID:str,ants_quantity:int,total_food:int,map_food:int,elapsed:float,status:str)-> bool:
     scenario = meta.tables['scenario']
     insert_scenario = (
         insert(scenario).
         values(
             id = ID,
             ants_quantity=ants_quantity,
             total_food=total_food,
             map_food=map_food,
             elapsed=elapsed,
             status=status
         )
     )
     engine.execute(insert_scenario)
     return True

def insert_anthill(ID:str,food_quantity:int,scenario_id:str)->bool:
    anthill = meta.tables['anthill']
    insert_anthill=(
        insert(anthill).
        values(
            id=ID,
            food_quantity=food_quantity,
            scenario_id=scenario_id
        )
    )
    engine.execute(insert_anthill)
    return True

def insert_ant(ID:str,status:int,total_food:int,anthill_id:str)->bool:
    ant = meta.tables['ant']
    insert_ant=(
        insert(ant).
        values(
            id=ID,
            status=status,
            total_food=total_food,
            anthill_id=anthill_id
        )    
    )
    engine.execute(insert_ant)
    return True

def update_scenario(ID:str,total_food:int,map_food:int,elapsed:float,status:str)-> bool:
    scenario = meta.tables["scenario"]
    update_scenario_status = (
         update(scenario).
         where(scenario.c.id == ID).
         values(
             status=status,
             elapsed=elapsed,
             map_food=map_food
        )
     )
    engine.execute(update_scenario_status)
    return True

def update_antihill(ID:str,food_quantity:int)->bool:
    anthill = meta.tables['anthill']
    update_anthill = (
        update(anthill).
        where(anthill.c.id == ID).
        values(
            food_quantity = food_quantity
        )
    )
    engine.execute(update_anthill)
    return True

def update_ant(ID:str,status:str,total_food:int)->bool:
    ant = meta.tables['ant']
    update_ant = (
        update(ant).
        where(ant.c.id==ID).
        values(
            status = status,
            total_food = total_food
        )
    )
    engine.execute(update_ant)
    return True
#%%

@app.task
def publish_data(data:dict):
    if data["status"] == "start":
        ## Insert scenario
        pass
    elif data["status"] == "executing":
        ## Update
        pass
    elif data["end"] == "end":
        ## Update
        pass
        
    print(data) 

#%%
def publish_data(data:dict):
    if data["status"] == "start":
        insert_scenario(data['scenario_id'], len(data['ants_info']), data['total_food'], data['map_food'], data['elapsed'],0)# status
        insert_anthill(data['anthill_id'], data['anthill_food'], data['scenario_id'])
        for i in range(0,len(data['ants_info'])):
            ant = data['ants_info'][i]
            ID = "_".join([str(data['scenario_id']),str(data['anthill_id']),str(i)])
            insert_ant(i, ant['status'], ant['total_food'], data['anthill_id'])
    else:
        update_scenario(data['scenario_id'], data['total_food'], data['map_food'], data['elapsed'], 1) #status
        update_antihill(data['anthill_id'], data['anthill_food'])
        for i in range(0,len(data['ants_info'])):
            ant = data['ants_info'][i]
            ID = "_".join([str(data['scenario_id']),str(data['anthill_id']),str(i)])
            update_ant(i, data['status'], data['total_food'])
        
    print(data)
#%%

start_data = {'elapsed': 0.0, 
            'status': 'start', 
            'total_food': 151, 
            'map_food': 151, 
            'anthill_food': 0, 'ants_info': []}

executing_data = {'elapsed': 76.73803091049194, 
                'status': 'executing', 
                'total_food': 151, 
                'map_food': 148, 
                'anthill_food': 0, 
                'ants_info': [{'status': 1, 'total_food': 0}, 
                              {'status': 0, 'total_food': 0}, 
                              {'status': 0, 'total_food': 0}, 
                              {'status': 1, 'total_food': 0}, 
                              {'status': 0, 'total_food': 0}, 
                              {'status': 2, 'total_food': 1}, 
                              {'status': 0, 'total_food': 0}, 
                              {'status': 2, 'total_food': 1}, 
                              {'status': 0, 'total_food': 0}, 
                              {'status': 0, 'total_food': 0}, 
                              {'status': 1, 'total_food': 0}, 
                              {'status': 0, 'total_food': 0}, 
                              {'status': 1, 'total_food': 0}, 
                              {'status': 0, 'total_food': 0}, {'status': 0, 'total_food': 0}, {'status': 0, 'total_food': 0}, {'status': 1, 'total_food': 0}, {'status': 2, 'total_food': 1}]}




