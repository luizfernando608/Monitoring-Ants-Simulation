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

@app.task
def insert_scenario(status:str, tempo_execucao:float, quantidade_total_comida:int)-> bool:
    scenario = meta.tables['cenario']
    insert_scenario = (
        insert(scenario).
        values(
            status=status,
            tempo_execucao=0,
            quantidade_total_comida=1000
        )
    )
    engine.execute(insert_scenario)
    return True



@app.task
def insert_antihill(quantidade_comida:int, quantidade_formiga_carregando:int, quantidade_formiga_procurando:int, maximo_carregado_formiga:int, id_cenario:int):
    antihill = meta.tables['formigueiro']
    insert_antihill= (
    insert(antihill).
    values(
        quantidade_comida=quantidade_comida,
        quantidade_formiga_carregando=quantidade_formiga_carregando,
        quantidade_formiga_procurando=quantidade_formiga_procurando,
        maximo_carregado_formiga=maximo_carregado_formiga,
        id_cenario=id_cenario)
    )
    engine.execute(insert_antihill)
    return True


@app.task
def update_scenario_status(id_scenario:int ,status:str, tempo_execucao:float=0)->bool:
    scenario = meta.tables["cenario"]
    update_scenario_status = (
        update(scenario).
        where(scenario.c.id_cenario == id_scenario).
        values(status=status,
            tempo_execucao=tempo_execucao)
    )
    engine.execute(update_scenario_status)
    return True


#%%
@app.task
def update_scenario_food(id_scenario:int, total_comida:int)->bool:
    scenario = meta.tables["cenario"]
    update_scenario_quantidade_comida = (
        update(scenario).
        where(scenario.c.id_cenario == id_scenario).
        values(quantidade_total_comida=total_comida)
    )
    engine.execute(
        update_scenario_quantidade_comida
    )
    return True

#%%
@app.task
def update_antihill(id_antihill:int,quantidade_comida:int, quantidade_formiga_carregando:int, quantidade_formiga_procurando:int, maximo_carregado_formiga:int)->bool:
    anthill = meta.tables["formigueiro"]
    update_antihill = (
        update(anthill).
        where(anthill.c.id_formigueiro == id_antihill).
        values(
            quantidade_comida=quantidade_comida,
            quantidade_formiga_carregando=quantidade_formiga_carregando,
            quantidade_formiga_procurando=quantidade_formiga_procurando,
            maximo_carregado_formiga = maximo_carregado_formiga,
            id_cenario=1
        )
    )
    engine.execute(update_antihill)
#%%



# Info requisitadas para inserção
# num_cenarios = 10
# num_total_formigueiros = 10

# num_total_formigas = 100
# percentual_procurando_comida = 0.5
# percentual_carregando_comida = 0.5


# num_total_comida=10
# percentual_na_fonte_de_comida = 0.5
# percentual_na_fonte = 0.25
# percentual_no_formigueiro = 0.25



