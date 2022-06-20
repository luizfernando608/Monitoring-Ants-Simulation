#select * from Global
#select * from Scenario where Scenario.id = ID

from sqlalchemy import MetaData, create_engine, select

from datawarehouse_credentials import *

engine = create_engine(f"{database_type}://{user_database}:{password}@{hostname}:{port}/{database_name}")
meta = MetaData(bind=engine)
MetaData.reflect(meta)

def retorn_global():
    '''
    Vai no banco analitico e retorna os dados de uma só vez

    Returns
        lista aonde estão:
              num_scenarios INT NOT NULL,
              num_anthills INT NOT NULL,
              num_ants INT NOT NULL,
              ants_searching FLOAT NOT NULL,
              ants_carring FLOAT NOT NULL,
              total_food INT NOT NULL,
              map_food FLOAT NOT NULL,
              anthill_food FLOAT NOT NULL,
              trafic_food FLOAT NOT NULL,
              mean_executing_time FLOAT NOT NULL,
              min_time_scenario VARCHAR(36) NOT NULL,
              min_time_time FLOAT NOT NULL,
              max_time_scenairio VARCHAR(36) NOT NULL,
              max_time_time FLOAT NOT NULL,
              mean_food_stored_per_ant INT NOT NULL,
              max_food_stored INT NOT NULL
    '''
    s = 'select * from Global order by timestamp;'
    r = engine.execute(s).fetchall()
    if len(r)==0:
        return 16*[0]
    else:
        return r[-1]

#%%
def retorna_lista_cenario():
    '''
    Vai no banco e retorna a lista de cenarios

    Returns
    -------
    list
        lista de cenarios

    '''
    s = 'select id from Scenario'
    return [i[0] for i in engine.execute(s).fetchall()]
    
    

#%%
def retorna_cenario(ID):
    '''
    Vai ao banco de dados e retorna os dados do cenário selecionado

    Parameters
    ----------
    ID : "str"
        Id do cenário

    Returns
    -------
    Lista
        ID VARCHAR(36) NOT NULL unique,
        Anthill INT NOT NULL,
        Ants INT NOT NULL,
        ants_searching FLOAT NOT NULL,
        ants_carring FLOAT NOT NULL,
        total_food INT NOT NULL,
        anthill_food FLOAT NOT NULL,
        trafic_food FLOAT NOT NULL,
        elapsed FLOAT NOT NULL,
        prob_win FLOAT NOT NULL,

    '''
    scenario = meta.tables["scenario"]
    s = select(scenario).where(scenario.c.id==ID)
    r = engine.execute(s).fetchall()
    if len(r)==0:
        return ['']+9*[0]
    else:
        return r[-1]

