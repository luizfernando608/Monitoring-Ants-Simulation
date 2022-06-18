#%%
from heapq import merge
from sqlalchemy import MetaData, and_, create_engine, update, insert, select
import pyspark.pandas as ps
from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.jars", "../postgresql-42.2.6.jar") \
    .getOrCreate()

spark
#%%

database_type = "postgresql"
user_database = "ympevcvwzchqwr"
password  = "34d49e45118ea441d83d827b2c4cb63831f8ec847444a950c53b5b2232c87996"
hostname = "ec2-34-198-186-145.compute-1.amazonaws.com"
port = "5432"
database_name = "d6rl9e5tvp50sh"

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


df_ants = ps.DataFrame(df_ants)
df_antihills = ps.DataFrame(df_antihills)
df_scenarios = ps.DataFrame(df_scenarios)
#%%
df_ants
#%%
df_scenarios_antihill = df_scenarios.merge(df_antihills,left_on='id',right_on='scenario_id')
df_scenarios_antihill =  df_scenarios_antihill.drop("id_x",axis=1)
df_scenarios_antihill.rename(columns={"id_y":"anthill_id"},inplace=True)
df_total = df_scenarios_antihill.merge(df_ants,left_on=['scenario_id',"anthill_id"],right_on=['scenario_id',"anthill_id"])


df_total.rename(
    columns={"total_food_x":"total_food_map","total_food_y":"total_food_ants",
            "status_y":"status_ants","status_x":"status_scenario"}, inplace=True)

