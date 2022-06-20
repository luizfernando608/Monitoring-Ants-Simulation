#%%
from pyspark.sql import SparkSession, SQLContext
from sqlalchemy import MetaData, and_, create_engine, update, insert, select
from time import sleep
spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.jars", "../postgresql-42.2.6.jar") \
    .config('spark.newSession().sql.shuffle.partitions', '10') \
    .getOrCreate()

database_type = "postgresql"
user_database = "postgres"
password  = "formigueiro123"
hostname_operational = "antsdatabase.cvb1csfwepbn.us-east-1.rds.amazonaws.com"
hostname_analytical = "allc-datawarehous.cvb1csfwepbn.us-east-1.rds.amazonaws.com"
port = "5432"
database_operational = "postgres"
database_analytical = "postgres"

df_ants = spark.read \
    .format("jdbc") \
    .option("url", f"jdbc:postgresql://{hostname_operational}:5432/{database_operational}") \
    .option("dbtable", "ant") \
    .option("user", user_database) \
    .option("password", password) \
    .option("driver", "org.postgresql.Driver") \
    .load()

df_antihills = spark.read \
    .format("jdbc") \
    .option("url", f"jdbc:postgresql://{hostname_operational}:5432/{database_operational}") \
    .option("dbtable", "anthill") \
    .option("user", user_database) \
    .option("password", password) \
    .option("driver", "org.postgresql.Driver") \
    .load()

df_scenarios = spark.read \
    .format("jdbc") \
    .option("url", f"jdbc:postgresql://{hostname_operational}:5432/{database_operational}") \
    .option("dbtable", "scenario") \
    .option("user", user_database) \
    .option("password", password) \
    .option("driver", "org.postgresql.Driver") \
    .load()
    
df_analytical_scenario = spark.read \
    .format("jdbc") \
    .option("url", f"jdbc:postgresql://{hostname_analytical}:5432/{database_analytical}") \
    .option("dbtable", "scenario") \
    .option("user", user_database) \
    .option("password", password) \
    .option("driver", "org.postgresql.Driver") \
    .load()
    
df_analytical_global = spark.read \
    .format("jdbc") \
    .option("url", f"jdbc:postgresql://{hostname_analytical}:5432/{database_analytical}") \
    .option("dbtable", "scenario") \
    .option("user", user_database) \
    .option("password", password) \
    .option("driver", "org.postgresql.Driver") \
    .load()

df_ants.createGlobalTempView("ant")
df_antihills.createGlobalTempView("anthill")
df_scenarios.createGlobalTempView("scenario")

df_analytical_scenario.createGlobalTempView("analytical_scenario")
df_analytical_global.createGlobalTempView("analytical_global")


def num_scenarios():
    result = spark.newSession().sql("""select count(*) from global_temp.scenario""").first()[0]
    return result


def num_antihills():
    """Numero de formigueiros"""
    result = spark.newSession().sql("""select count(*) from global_temp.anthill""").first()[0]
    return result


def num_ants():
    """Numero de formigas"""
    result = spark.newSession().sql("""select count(*) from global_temp.ant""").first()[0]
    return result


def num_ants_carrying():
    """Numero carregando comida"""
    return spark.newSession().sql("select count(*) from global_temp.ant where ant.status='2'").first()[0]


def num_ants_looking_for_food():
    """Numero procurando comida"""
    return spark.newSession().sql("select count(*) from global_temp.ant where ant.status!='2'").first()[0]

def rate_carrying():
    """Percentual de formigas procurando comida."""
    return num_ants_carrying()/num_ants()

def rate_looking_for_food():
    """Percentual de formigas carregando comida."""
    return num_ants_looking_for_food()/num_ants()

def total_food():
    """Total de comida em todos os cenários"""
    return spark.newSession().sql("select sum(total_food) from global_temp.scenario").first()[0]

def total_source_food():
    """Total de comida na fonte"""
    return spark.newSession().sql("select sum(s.map_food) from global_temp.scenario s").first()[0]

def total_food_carrying():
    """Total comida sendo carregada"""
    return spark.newSession().sql("select count(*) from global_temp.ant where ant.status='2'").first()[0]

def total_food_anthill():
    return spark.newSession().sql("select sum(a.food_quantity) from global_temp.anthill a").first()[0]

def rate_source_food():
    """Percentual de comida na fonte"""
    return total_source_food()/total_food()

def rate_food_carrying():
    """Percentual de comida sendo carregada"""
    return total_food_carrying()/total_food()

def rate_food_anthill():
    """Percentual de comida na fonte"""
    return total_food_anthill()/total_food()


def avg_elapsed_time():
    """tempo medio de execução de um cenário"""
    return spark.newSession().sql("select avg(elapsed) from global_temp.scenario").first()[0]

def scenario_min_elapsed():
    """identificador e o tempo de execução do cenário que teve menor tempo de duração"""
    id,elapsed = spark.newSession().sql(
        """
        select id, min(elapsed) as elapsed
        from global_temp.scenario 
        group by id
        order by elapsed asc
        limit 1
        """).first()[:]
    return id, elapsed

def scenario_max_elapsed():
    """identificador e o tempo de execução do cenário que teve maior tempo deduração"""
    id,elapsed = spark.newSession().sql(
        """
        select id, max(elapsed) as elapsed
        from global_temp.scenario 
        group by id
        order by elapsed desc
        limit 1
        """).first()[:]
    return id, elapsed

def ant_max_food():
    """máximo de unidades de comida que uma formiga foi capaz de levarpara o formigueiro"""
    result = spark.newSession().sql("select max(total_food) from global_temp.ant").first()[0]
    return result

def ant_avg_food():
    """unidades de comida uma formiga leva para o formigueiro em média durante a execução de um cenário"""
    result = spark.newSession().sql("select avg(total_food) from global_temp.ant").first()[0]
    return result



#### QUERIES POR CENÀRIO ####
def num_anthills_scenario(id):
    """Número de formigueiros no cenário"""
    return spark.newSession().sql(f"select count(*) from global_temp.anthill where scenario_id = '{id}'").first()[0]

def num_ants_scenario(id):
    """Número de formigas no cenário"""
    return spark.newSession().sql(f"select count(*) from global_temp.ant where scenario_id = '{id}'").first()[0]

def total_food_scenario(id):
    """Total de comida no cenário"""
    return spark.newSession().sql(f"select sum(total_food) from global_temp.ant where scenario_id = '{id}'").first()[0]

def elapsed_scenario(id):
    """Tempo de execução do cenário"""
    return spark.newSession().sql(f"select elapsed from global_temp.scenario where id = '{id}'").first()[0]



def num_ants_by_anthill(id_scenario):
    """Número de formigas por formigueiro"""
    results = spark.newSession().sql(
    f"""select anthill_id, count(*)
        from global_temp.ant a
        where scenario_id = '{id_scenario}'
        group by anthill_id""").collect()
    return [tuple(i.asDict().values()) for i in results]
        

def num_ants_carrying_by_anthill(id_scenario):
    "Número de formigas carregando comida por formigueiro"
    results = spark.newSession().sql(
    f"""select anthill_id, count(*)
        from global_temp.ant a
        where scenario_id = '{id_scenario}'
        and a.status = '2'
        group by anthill_id ;""").collect()
    return [tuple(i.asDict().values()) for i in results]

def num_ants_looking_for_food_by_anthill(id_scenario):
    "Número de formigas procurando comida por formigueiro"
    result= spark.newSession().sql(
    f"""select anthill_id, count(*)
        from global_temp.ant a
        where scenario_id = '{id_scenario}'
        and a.status != '2'
        group by anthill_id ;""").collect()
    return [tuple(i.asDict().values()) for i in result]


def total_food_by_anthill(id_scenario):
    "Total de comida no formigueiro"
    results= spark.newSession().sql(
    f"""select id, sum(food_quantity)
        from global_temp.anthill a
        where scenario_id = '{id_scenario}'
        group by id ;""").collect()
    return [tuple(i.asDict().values()) for i in results]

def total_food_carrying_by_anthill(id_scenario):
    "Total de comida sendo carregada para o formigueiro"
    results= spark.newSession().sql(
    f"""select anthill_id, count(*)
        from global_temp.ant a
        where scenario_id = '{id_scenario}'
        and a.status = '2'
        group by anthill_id ;""").collect()
    return [tuple(i.asDict().values()) for i in results]

def list_scenarios():
    results = spark.newSession().sql(f"""select id from global_temp.scenario""").collect()
    return [i[0] for i in results]

def does_scenario_exists(id_scenario:str)->bool:
    scenario_instance = meta.tables['scenario']
    scenario_instance_query = (select([scenario_instance.c.id]).where(scenario_instance.c.id == id_scenario))
    ids_scenario_instance = engine.execute(scenario_instance_query).fetchall()
    if len(ids_scenario_instance) == 0:
        return False
    else:
        return True

from datawarehouse_credentials import *
engine = create_engine(f"{database_type}://{user_database}:{password}@{hostname}:{port}/{database_name}")
meta = MetaData(bind=engine)
MetaData.reflect(meta)



while True:
    ### Criar Tabela Global:
    G1 = num_scenarios()
    G2 = num_antihills()
    G3 = num_ants()
    G4 = num_ants_looking_for_food()
    G5 = num_ants_carrying()
    G6 = total_food()
    G7 = total_source_food()
    G8 = total_food_anthill()
    G9 = num_ants_carrying()
    G10 = avg_elapsed_time()
    G11, G12 = scenario_min_elapsed()
    G13 ,G14 = scenario_max_elapsed()
    G15 = ant_avg_food()
    G16 = ant_max_food()


    global_table = meta.tables["global"]
    query = (insert(global_table).values(
        num_scenarios=G1,
        num_anthills=G2,
        num_ants=G3,
        ants_searching=G4,
        ants_carring=G5,
        total_food=G6,
        map_food=G7,
        anthill_food=G8,
        trafic_food=G9,
        mean_executing_time=G10,
        min_time_scenario=G11,
        min_time_time=G12,
        max_time_scenairio=G13,
        max_time_time=G14,
        mean_food_stored_per_ant=G15,
        max_food_stored=G16
    ))

    engine.execute(query)    

    #%%
    # MEIO Com sono...


    lista=list_scenarios()
    cenario_table = meta.tables["scenario"]

    for cenario in lista:    
        C1 = cenario
        C2 = num_anthills_scenario(cenario)
        C3 = num_ants_scenario(cenario)
        C4 = num_ants_looking_for_food_by_anthill(cenario)
        if len(C4) == 0:
            C4 = 0
        else:
            C4 = C4[0][1]
        
        C5 = num_ants_carrying_by_anthill(cenario)
        if len(C5) == 0:
            C5 = 0
        else:
            C5 = C5[0][1]
            
        C6 = total_food_scenario(cenario)
        C7 = total_food_by_anthill(cenario)
        if len(C7) == 0:
            C7 = 0
        else:
            C7 = C7[0][1]
            
        C8 = total_food_carrying_by_anthill(cenario)
        if len(C8) == 0:
            C8 = 0
        else:
            C8 = C8[0][1]

        C9 = elapsed_scenario(cenario)
        C10= (C7+C8)/(C6+C7+C8)*100

        if not does_scenario_exists(cenario):
            query_scenario =insert(cenario_table).values(
                id=C1,
                anthill_id=C2,
                ants_id=C3,
                ants_searching=C4,
                ants_carring=C5,
                total_food=C6,
                anthill_food=C7,
                trafic_food=C8,
                elapsed=C9,
                prob_win=C10)
        else:
            query_scenario =(update(cenario_table)
            .where(cenario_table.c.id == cenario).values(
                anthill_id=C2,
                ants_id=C3,
                ants_searching=C4,
                ants_carring=C5,
                total_food=C6,
                anthill_food=C7,
                trafic_food=C8,
                elapsed=C9,
                prob_win=C10))

        engine.execute(query_scenario)
    

    sleep(30)
