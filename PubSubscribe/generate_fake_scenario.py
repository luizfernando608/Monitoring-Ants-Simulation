#%%
import consumer
import numpy as np

#%%

for i in range(1,100):
    status = np.random.choice(["running","finished"],p=[0.6,0.4], size=1)[0]
    quantidade_total_comida = 10000
    if status == "running":
        tempo_execucao = 0
    if status == "finished":
        tempo_execucao = np.random.uniform(10,1000)
    consumer.insert_scenario.delay(status, tempo_execucao, quantidade_total_comida)


#%%

for i in range(1,100):
    quantidade_comida = np.random.randint(0,10000)
    quantidade_formiga_carregando = np.random.randint(0,10000-quantidade_comida)
    quantidade_formiga_procurando = np.random.randint(0,10000-quantidade_comida-quantidade_formiga_carregando)
    maximo_carregado_formiga = np.random.randint(0,quantidade_comida)
    id_cenario = i
    consumer.insert_antihill.delay(quantidade_comida,
                            quantidade_formiga_carregando,
                            quantidade_formiga_procurando,
                            maximo_carregado_formiga,
                            id_cenario)