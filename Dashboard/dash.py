#%%
from sqlalchemy import MetaData, create_engine, select
import streamlit as st
import time
import altair as alt
import pandas as pd

#%%
# Ligar Banco de Dados
database_type = "postgresql"
user_database = "ympevcvwzchqwr"
password  = "34d49e45118ea441d83d827b2c4cb63831f8ec847444a950c53b5b2232c87996"
hostname = "ec2-34-198-186-145.compute-1.amazonaws.com"
port = "5432"
database_name = "d6rl9e5tvp50sh"
engine = create_engine(f"{database_type}://{user_database}:{password}@{hostname}:{port}/{database_name}")
meta = MetaData(bind=engine)
MetaData.reflect(meta)

#%%

# NUM_Formigueiros // Num_For_Car // Num_For_Pro // Num_Comida_Formigueiro
t1=time.time()
s='''SELECT count(formigueiro.id_cenario), sum(formigueiro.quantidade_formiga_carregando),
            sum(formigueiro.quantidade_formiga_procurando), sum(formigueiro.quantidade_comida)
     FROM formigueiro'''
a=engine.execute(s).fetchall()

# NUM_Cenarios // NUM_T_Comida
s='''SELECT count(cenario.id_cenario), sum(cenario.quantidade_total_comida)
     FROM cenario'''
b=engine.execute(s).fetchall()


#%%
st.set_page_config(page_title='Formiguinhas',
                   page_icon='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/google/313/ant_1f41c.png',
                   layout="wide")

st.title('FORMIGUINHAS')
a1,a2,a3,a4 = st.columns(4)
a1.metric('Numero Cenarios',b[0][0])
a2.metric('Número Formigueiros',a[0][0])
a3.metric('Número Formigas',a[0][1]+a[0][2])
a4.metric('Número Total de Comida',b[0][1])
#%%
source = pd.DataFrame({'formigas':['carregando','procurando'],
                       'quantidade':[a[0][1],a[0][2]]})

ants = alt.Chart(source).mark_bar().encode(
    x=alt.X("sum(quantidade)",title='%',stack='normalize'),
    color=alt.Color("formigas:N"),
)
#%%
source = pd.DataFrame({'comida':['formigueiro','transporte','fonte'],
                       'quantidade':[a[0][3],a[0][1],b[0][1]-a[0][3]-a[0][1]]})

food = alt.Chart(source).mark_bar().encode(
    x=alt.X("sum(quantidade)",title='%',stack='normalize'),
    color=alt.Color("comida:N"),
)

m= (ants&food).resolve_scale(
    color='independent'
).configure_view(
    stroke=None
)

b1,b2,b3,b4=st.columns([1,1,1,3])
b1.write('\n')
b2.write('\n')
b3.write('\n')
b1.image('https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/facebook/158/ant_1f41c.png')
b2.image('https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/21/ant_1f41c.png')
b3.image('https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/samsung/320/ant_1f41c.png')
b4.markdown("### Porcentagens")
b4.altair_chart(m)
