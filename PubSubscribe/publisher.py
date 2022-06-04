import sqlalchemy
# from task import hello, add
import time
from consumer import *

# Command examples
insert_scenario(
    status="running",
    tempo_execucao=0,
    quantidade_total_comida=1000,
).delay()


insert_antihill(
    quantidade_comida=0,
    quantidade_formiga_carregando=10,
    quantidade_formiga_procurando=10,
    maximo_carregado_formiga=1,
    id_cenario=1
).delay()


update_antihill(
    id_formigueiro=1,
    quantidade_comida=500,
    quantidade_formiga_carregando=5,
    quantidade_formiga_procurando=15,
    maximo_carregado_formiga=20,
    id_cenario=1
)

update_scenario_status(
    id_scenario=1,
    status="finished",
)