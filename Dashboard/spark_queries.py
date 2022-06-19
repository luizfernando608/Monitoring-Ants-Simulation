#%%
from unittest import result
from pyspark.context import SparkContext
from pyspark.sql import SparkSession, SQLContext

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.jars", "../postgresql-42.2.6.jar") \
    .config('spark.newSession().sql.shuffle.partitions', '10') \
    .getOrCreate()

database_type = "postgresql"
user_database = "root"#"ympevcvwzchqwr"
password  = "root"#"34d49e45118ea441d83d827b2c4cb63831f8ec847444a950c53b5b2232c87996"
hostname = "127.0.0.1"#"ec2-34-198-186-145.compute-1.amazonaws.com"
port = "5432"
database_name = "test_ants"#"d6rl9e5tvp50sh"


df_ants = spark.read \
    .format("jdbc") \
    .option("url", f"jdbc:postgresql://{hostname}:5432/{database_name}") \
    .option("dbtable", "ant") \
    .option("user", user_database) \
    .option("password", password) \
    .option("driver", "org.postgresql.Driver") \
    .load()

df_antihills = spark.read \
    .format("jdbc") \
    .option("url", f"jdbc:postgresql://{hostname}:5432/{database_name}") \
    .option("dbtable", "anthill") \
    .option("user", user_database) \
    .option("password", password) \
    .option("driver", "org.postgresql.Driver") \
    .load()

df_scenarios = spark.read \
    .format("jdbc") \
    .option("url", f"jdbc:postgresql://{hostname}:5432/{database_name}") \
    .option("dbtable", "scenario") \
    .option("user", user_database) \
    .option("password", password) \
    .option("driver", "org.postgresql.Driver") \
    .load()
    

#%%
df_ants.createGlobalTempView("ant")
df_antihills.createGlobalTempView("anthill")
df_scenarios.createGlobalTempView("scenario")

spark.sql


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
    id,elapsed = spark.sql("select id,elapsed from global_temp.scenario where elapsed = (select min(elapsed) from global_temp.scenario)").first()[:]
    return id, elapsed

def scenario_max_elapsed():
    """identificador e o tempo de execução do cenário que teve maior tempo deduração"""
    id,elapsed = spark.newSession().sql("select id,elapsed from global_temp.scenario where elapsed = (select max(elapsed) from global_temp.scenario)").first()[:]
    return id, elapsed

def ant_max_food():
    """máximo de unidades de comida que uma formiga foi capaz de levarpara o formigueiro"""
    result = spark.newSession().sql("select max(total_food) from global_temp.ant").first()[0]
    return result

def ant_avg_food():
    """unidades de comida uma formiga leva para o formigueiro em média durante a execução de um cenário"""
    result = spark.newSession().sql("select avg(total_food) from global_temp.ant").first()[0]
    return result

#%%

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

#%%

def num_ants_by_anthill(id_scenario):
    """Número de formigas por formigueiro"""
    results = spark.newSession().sql(
    f"""select anthill_id, count(*)
        from global_temp.ant a
        where scenario_id = '{id_scenario}'
        group by anthill_id""").collect()
    return [tuple(i.asDict().values()) for i in results]
        


#%%
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
    



