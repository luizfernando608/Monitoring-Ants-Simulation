#select * from Global
#select * from Cenario where Cenario.id = ID

from sqlalchemy import MetaData, create_engine, select

## utilizei o banco antigo para fazer alguns testes mas os nomes das tabelas já está o nome do analitico...

database_type = "postgresql"
user_database = "ympevcvwzchqwr"
password  = "34d49e45118ea441d83d827b2c4cb63831f8ec847444a950c53b5b2232c87996"
hostname = "ec2-34-198-186-145.compute-1.amazonaws.com"
port = "5432"
database_name = "d6rl9e5tvp50sh"
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
    s = 'select * from Global;'
    return engine.execute(s).fetchall()[-1]

[NCenario, NFormigueiro, NFormigas, NFProcurando,NFCarregando , NComida, NCFonte, 
 NCFormigueiro, NCTransito, MediaTempo, IDMinTempo, MinTempo, IDMaxTempo, 
 MaxTempo,MediaCarregado, MaxCarregado] = retorn_global()


MaxTempo = round(MaxTempo,3)
MinTempo = round(MinTempo,3)
MediaTempo = round(MediaTempo,3)

MediaCarregado = round(MediaCarregado,3)
#%%
def retorna_lista_cenario():
    '''
    Vai no banco e retorna a lista de cenarios

    Returns
    -------
    list
        lista de cenarios

    '''
    s = 'select id from Cenario'
    return [i[0] for i in engine.execute(s).fetchall()]
    
    
print(retorna_lista_cenario())

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
    scenario = meta.tables["Cenario"]
    s = select(scenario).where(scenario.c.id==ID)
    return engine.execute(s).fetchall()[-1]


print(retorna_cenario(retorna_lista_cenario()[0]))
