import streamlit as st
from time import sleep

def retorna_linha(valores):
    tamanho=0
    for a in valores:
        tamanho += len(str(a))
    return '|'+str(valores[0])+(73-tamanho)*' '+str(valores[1])+'|'


b='|'


#Limpar Código
import os
os.system('cls')
 
st.set_page_config(page_title='Formiguinhas',
                   page_icon='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/google/313/ant_1f41c.png',
                   layout="wide")

from functions import *

[NCenario, NFormigueiro, NFormigas, NFProcurando, NFCarregando , NComida, NCFonte, 
 NCFormigueiro, NCTransito, MediaTempo, IDMinTempo, MinTempo, IDMaxTempo, 
 MaxTempo,MediaCarregado, MaxCarregado,t] = retorn_global()

MaxTempo = round(MaxTempo,3)
MinTempo = round(MinTempo,3)
MediaTempo = round(MediaTempo,3)
NComida =  NCFonte +NCFormigueiro + NCTransito
MediaCarregado = round(MediaCarregado,3)

if NCenario==0:
    st.title('Ainda não tem dados')
else:
    a = st.container()
    a.subheader('Dados Primários')
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

    st.markdown('__________')
    b = st.container()
    
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

    st.markdown('__________')
    
    c = st.container()

    c1,l = c.columns([2,3])
    seletor = c1.selectbox('Qual cenário quer observar?',['']+retorna_lista_cenario())
    if seletor !='':
        [CID,CNFormigueiros,CNFormigas,CNFProcurando,CNFCarregando,CNCFonte,
        CNCFormigueiro,CNCTransito,CTempo,CProb]=retorna_cenario(seletor)
        CProb=round(CProb,3)
        CTempo=round(CTempo,3)
        CNComida = CNCFonte+CNCFormigueiro+CNCTransito
        c.title(seletor.title())
        c1,c2,c3,c4=c.columns(4)
        c1.metric('Numero Formigueiros',CNFormigueiros)
        c2.metric('Numero Formigas',CNFormigas)
        c3.metric('Numero Comida',CNComida)
        c4.metric('Tempo de Execução',CTempo)
        # Formigueiro
        l,c_0,l=c.columns([1,9,1])
        c_0.title('Formigueiro '+str(1))
        l,c1,c2,c3,l = c.columns([1,3,3,3,1])
        c1.metric('Numero Formigas',CNFormigas)
        c1.write(f"- % Carregando: {round(CNFCarregando/CNFormigas*100,2)} %")
        c1.write(f"- % Procurando: {round(CNFProcurando/CNFormigas*100,2)} %")
        c1.empty()
        total_food_A = CNCTransito + CNCFormigueiro
        c2.metric('Numero Comida', total_food_A) 
        c2.write(f"- % Formigueiro: {round(CNCFormigueiro/(total_food_A)*100,2)} %")
        c2.write(f"- % Transito: {round(CNCTransito/(total_food_A)*100,2)} %")
        c3.metric('Probabilidade',str(CProb) +' %')
        print(
            retorna_linha(['Valores:','']),
            retorna_linha([' Total Cenários', NCenario]),
            retorna_linha([' Total Formigueiro',NFormigueiro]),
            retorna_linha([' Total Formiga',NFormigas]),
            retorna_linha(['  % Carregando',str(round(NFCarregando/NFormigas*100,2))+'%']),
            retorna_linha(['  % Procurando',str(round(NFProcurando/NFormigas*100,2))+'%']),
            retorna_linha([' Total Comida',NComida]),
            retorna_linha(['  % Fonte',str(round(NCFonte/NComida*100,2))+'%']),
            retorna_linha(['  % Formigueiro',str(round(NCFormigueiro/NComida*100,2))+'%']),
            retorna_linha(['  % Transito',str(round(NCTransito/NComida*100,2))+'%']),
            retorna_linha(['','']),
            retorna_linha(['Tempo Cenários:','']),
            retorna_linha([' Máximo',MaxTempo]),
            retorna_linha(['  Quem',IDMaxTempo]),
            retorna_linha([' Mínimo',MinTempo]),
            retorna_linha(['  Quem',IDMinTempo]),
            retorna_linha([' Média',MediaTempo]),
            retorna_linha(['Comida Carregada por Formiga:','']),
            retorna_linha([' Máximo',MaxCarregado]),
            retorna_linha([' Média', MediaCarregado]),
            retorna_linha(['','']),
            retorna_linha(['CENARIO',seletor]),
            retorna_linha(['Numero Formigueiros',CNFormigueiros]),
            retorna_linha(['Numero Formigas',CNFormigas]),
            retorna_linha(['Numero Comida',CNComida]),
            retorna_linha(['Tempo de Execução',CTempo]),
            retorna_linha(['FORMIGUEIRO','']),
            retorna_linha([' Numero Formigas',CNFormigas]),
            retorna_linha(["- % Carregando" ,f"{round(CNFCarregando/CNFormigas*100,2)} %"]),
            retorna_linha(["- % Procurando",f"{round(CNFProcurando/CNFormigas*100,2)} %"]),
            retorna_linha([' Numero Comida', total_food_A]),
            retorna_linha(["- % Formigueiro",f" {round(CNCFormigueiro/(total_food_A)*100,2)} %"]),
            retorna_linha(["- % Transito",f"{round(CNCTransito/(total_food_A)*100,2)} %"]),
            retorna_linha([' Probabilidade',str(CProb) +' %']),sep='\n')
    else:
        print(
        retorna_linha(['Valores:','']),
        retorna_linha([' Total Cenários', NCenario]),
        retorna_linha([' Total Formigueiro',NFormigueiro]),
        retorna_linha([' Total Formiga',NFormigas]),
        retorna_linha(['  % Carregando',str(round(NFCarregando/NFormigas*100,2))+'%']),
        retorna_linha(['  % Procurando',str(round(NFProcurando/NFormigas*100,2))+'%']),
        retorna_linha([' Total Comida',NComida]),
        retorna_linha(['  % Fonte',str(round(NCFonte/NComida*100,2))+'%']),
        retorna_linha(['  % Formigueiro',str(round(NCFormigueiro/NComida*100,2))+'%']),
        retorna_linha(['  % Transito',str(round(NCTransito/NComida*100,2))+'%']),
        retorna_linha(['','']),
        retorna_linha(['Tempo Cenários:','']),
        retorna_linha([' Máximo',MaxTempo]),
        retorna_linha(['  Quem',IDMaxTempo]),
        retorna_linha([' Mínimo',MinTempo]),
        retorna_linha(['  Quem',IDMinTempo]),
        retorna_linha([' Média',MediaTempo]),
        retorna_linha(['Comida Carregada por Formiga:','']),
        retorna_linha([' Máximo',MaxCarregado]),
        retorna_linha([' Média', MediaCarregado]),sep='\n')


# automatically rerun after 30s
sleep(5)
st.experimental_rerun()