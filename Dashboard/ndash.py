#NewDash
import streamlit as st
import pandas as pd
from spark_queries import *

NFormigas = 10
NFCarregando = 5
NFProcurando = 5

NFormigueiro = 2
NCenario = 2

NComida = 10
NCFonte = 3
NCFormigueiro = 2
NCTransito = 5

MaxTempo = 10
MinTempo = 5
MediaTempo = 7.5
MaxCarregado = 2
MediaCarregado = 0.2

mapa = {'cenario1':{'NFormigueiro':1,'NFormigas':5,'NFC':3,'NFP':2,'NComida':5,'NCFon':2,'NCFor':0,
                    'Tempo':10,'form_describe':[{'NFormigas':5,'NFC':3,'NFP':2,'NCFor':0}]}}


st.set_page_config(page_title='Formiguinhas',
                   page_icon='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/google/313/ant_1f41c.png',
                   layout="wide")

a = st.expander('Dados Primários')

a1,a2,a3,a4 = a.columns(4)
a1.metric('Numero Cenarios',NCenario)
a2.metric('Número Formigueiros',NFormigueiro)
a3.metric('Número Formigas',NFormigas)
a3.write(f'- % Carregando: {NFCarregando/NFormigas*100} %')
a3.write(f'- % Procurando: {NFProcurando/NFormigas*100} %')
a4.metric('Número Total de Comida',NComida)
a4.write(f'- % na Fonte: {NCFonte/NComida*100} %')
a4.write(f'- % Formigueiro: {NCFormigueiro/NComida*100} %')
a4.write(f'- % em Transito: {NCTransito/NComida*100} %')
a4.empty()

b = st.expander('Medições')

b_1,b_4=b.columns([3,2])
b1,b2,b3,b4,b5 = b.columns(5)

b_1.title('Tempo de Execução dos Cenários')
b_4.title('Comida por Formiga')

b1.metric('Maior tempo de Execução',MaxTempo)
b2.metric('Menor tempo de Execução',MinTempo)
b3.metric('Tempo médio de Execução',MediaTempo)
b4.metric('Máximo de comida carregada',MaxCarregado)
b5.metric('Média de comida carregada',MediaCarregado)


c = st.expander('Qual cenário quer observar?')

c1,l = c.columns([2,3])
seletor = c1.selectbox('',mapa.keys())
if seletor !='':
    c.title(seletor.title())
    c1,c2,c3,c4=c.columns(4)
    c1.metric('Numero Formigueiros',mapa[seletor]['NFormigueiro'])
    c2.metric('Numero Formigas',mapa[seletor]['NFormigas'])
    c3.metric('Numero Comida',mapa[seletor]['NComida'])
    c4.metric('Tempo de Execução',mapa[seletor]['Tempo'])
    for i in range(0,len(mapa[seletor]['form_describe'])):
        item = mapa[seletor]['form_describe'][i]
        l,c_0,l=c.columns([1,9,1])
        c_0.title('Formigueiro '+str(i+1))
        l,c1,c2,c3,l = c.columns([1,3,3,3,1])
        c1.metric('Numero Formigas',item['NFormigas'])
        c1.write(f"- % Carregando: {item['NFC']/item['NFormigas']*100} %")
        c1.write(f"- % Procurando: {item['NFP']/item['NFormigas']*100} %")
        c1.empty()
        c2.metric('Numero Comida', item['NCFor']+item['NFC'])
        c2.write(f"- % Formigueiro: {item['NCFor']/(item['NCFor']+item['NFC'])*100} %")
        c2.write(f"- % Transito: {item['NFC']/(item['NCFor']+item['NFC'])*100} %")
        c3.metric('Probabilidade',str((item['NCFor']+item['NFC'])/mapa[seletor]['NComida']*100) +' %')