#NewDash
import streamlit as st
from time import sleep

st.set_page_config(page_title='Formiguinhas',
                   page_icon='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/google/313/ant_1f41c.png',
                   layout="wide")

import pandas as pd
from spark_queries import *

NFormigas = num_ants()
NFCarregando = num_ants_carrying()
NFProcurando = num_ants_looking_for_food()

NFormigueiro = num_antihills()
NCenario = num_scenarios()

NComida = total_food()
NCFonte = total_source_food()
NCFormigueiro = total_food_anthill()
NCTransito = total_food_carrying()

IDMaxTempo, MaxTempo = scenario_max_elapsed()
MaxTempo = round(MaxTempo,3)
IDMinTempo, MinTempo = scenario_min_elapsed()
MinTempo = round(MinTempo,3)
MediaTempo = round(avg_elapsed_time(),3)
MaxCarregado = round(ant_max_food(),3)
MediaCarregado = round(ant_avg_food(),3)

mapa = {'cenario1':{'NFormigueiro':1,'NFormigas':5,'NFC':3,'NFP':2,'NComida':5,'NCFon':2,'NCFor':0,
                    'Tempo':10,'form_describe':[{'NFormigas':5,'NFC':3,'NFP':2,'NCFor':0}]}}

a = st.expander('Dados Primários')

a1,a2,a3,a4 = a.columns(4)
a1.metric('Numero Cenarios',NCenario)
a2.metric('Número Formigueiros',NFormigueiro)
a3.metric('Número Formigas',NFormigas)
a3.write(f'- % Carregando: {round(NFCarregando/NFormigas*100,2)} %')
a3.write(f'- % Procurando: {round(NFProcurando/NFormigas*100,2)} %')
a4.metric('Número Total de Comida',NComida)
a4.write(f'- % na Fonte: {round(NCFonte/NComida*100,2)} %')
a4.write(f'- % Formigueiro: {round(NCFormigueiro/NComida*100,2)} %')
a4.write(f'- % em Transito: {round(NCTransito/NComida*100,2)} %')
a4.empty()

b = st.expander('Medições')

b_1,b_4=b.columns([3,2])
b1,b2,b3,b4,b5 = b.columns(5)

b_1.title('Tempo de Execução dos Cenários')
b_4.title('Comida por Formiga')

b1.metric('Maior tempo de Execução',MaxTempo)
b1.write(IDMaxTempo)
b2.metric('Menor tempo de Execução',MinTempo)
b2.write(IDMinTempo)
b2.empty()
b3.metric('Tempo médio de Execução',MediaTempo)
b4.metric('Máximo de comida carregada',MaxCarregado)
b5.metric('Média de comida carregada',MediaCarregado)


c = st.expander('Qual cenário quer observar?')

# scenarios_data = {}
# for seletor in list_scenarios():
#     scenario_data = {}
#     scenario_data['Numero Formigueiros']= num_anthills_scenario(seletor)
#     scenario_data['Numero Formigas']= num_ants_scenario(seletor)    
#     scenario_data['Numero Comida']= total_food_scenario(seletor)
#     scenario_data['Tempo de Execução']= elapsed_scenario(seletor)
#     scenarios_data["Numero Formigas"] = []
#     scenarios_data["Numero Procurando"] = []
#     scenarios_data["Numero Carregando"] = []
#     for i in range(0,len(num_ants_looking_for_food_by_anthill(seletor))):
#         scenarios_data["Numero Formigas"].append(num_ants_by_anthill(seletor)[i][1])
#         carrying = num_ants_carrying_by_anthill(seletor)[i][1]
#         if len(carrying) == 0:
#             scenarios_data["Numero Carregando"].append(0)
#         else:
#             scenarios_data["Numero Carregando"].append(carrying[i][1])
#         scenarios_data['Numero Procurando'].append(num_ants_looking_for_food_by_anthill(seletor)[i][1]/num_ants_by_anthill(seletor)[i][1]*100)




c1,l = c.columns([2,3])
seletor = c1.selectbox('',list_scenarios())
if seletor !='':
    c.title(seletor.title())
    c1,c2,c3,c4=c.columns(4)
    c1.metric('Numero Formigueiros',num_anthills_scenario(seletor))
    c2.metric('Numero Formigas',num_ants_scenario(seletor))
    c3.metric('Numero Comida',total_food_scenario(seletor))
    c4.metric('Tempo de Execução',elapsed_scenario(seletor))
    for i in range(0,len(num_ants_looking_for_food_by_anthill(seletor))):
        #item = mapa[seletor]['form_describe'][i]
        l,c_0,l=c.columns([1,9,1])
        c_0.title('Formigueiro '+str(i+1))
        l,c1,c2,c3,l = c.columns([1,3,3,3,1])
        c1.metric('Numero Formigas',num_ants_by_anthill(seletor)[i][1])
        if len(num_ants_carrying_by_anthill(seletor)) ==0:
            carrying = 0
        else:
            carrying = num_ants_carrying_by_anthill(seletor)[i][1]
        c1.write(f"- % Carregando: {carrying/num_ants_by_anthill(seletor)[i][1]*100} %")
        c1.write(f"- % Procurando: {num_ants_looking_for_food_by_anthill(seletor)[i][1]/num_ants_by_anthill(seletor)[i][1]*100} %")
        c1.empty()
        total_food_A = carrying + total_food_by_anthill(seletor)[i][1]
        c2.metric('Numero Comida', total_food_A) 
        c2.write(f"- % Formigueiro: {total_food_by_anthill(seletor)[i][1]/(total_food_A)*100} %")
        c2.write(f"- % Transito: {carrying/(total_food_A)*100} %")
        c3.metric('Probabilidade',str((total_food_A)/total_food_scenario(seletor)*100) +' %')


# automatically rerun after 30s
sleep(30)
st.experimental_rerun()