import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

dic = {
    'titulo_pagina':'# 🔩 Estudo sobre Aletas',
    'subtitulo': '##### Transferência de calor', 
    'condicoes_titulo':'Condição na extremidade:', 
    'condicoes_extremidade': ['Transferência por Convecção', 
                              'Adiabática', 
                              'Temperatura prescrita', 
                              'Aleta infinita'], 
    'condicao_escolhida': None,
    'forma_titulo': 'Forma da aleta:',
    'forma': ['Retangular', 'Pino'], 
    'forma_escolhida': None,
    'temperatura_base': None,
    'tamanho': None,
    'k':None,
    'h': None, 
    'perimetro': None,
    'area_c':None,
}

st.markdown(dic['titulo_pagina'])
st.markdown(dic['subtitulo'])


_cols = st.columns(2)
with _cols[0]:
    dic['forma_escolhida'] = st.selectbox(dic['forma_titulo'], dic['forma'])
with _cols[1]:
    dic['condicao_escolhida'] = st.selectbox(dic['condicoes_titulo'], dic['condicoes_extremidade'])

with st.sidebar:

    dic['temperatura_base'] = st.number_input('Temperatura na base [K]', 100.0, step=10.0)
    dic['tamanho'] = st.number_input('Tamanho da aleta [m]', 1.0, step=.1)
    dic['k'] = st.number_input('Coef. condução [W/m²K]', 100.0, step=.1)
    dic['h'] = st.number_input('Coef. convecção [W/m²K]',value=177.0, step=.1)
    dic['perimetro'] =  st.number_input('Perímetro [m]', .50, step=.1)
    dic['area_c'] = st.number_input('Área circunferência [m²]', .50, step=.1)




st.markdown('___')

if dic['condicao_escolhida'] == dic['condicoes_extremidade'][0]:

    st.markdown('Na extremidade:')
    st.latex(r'''
        h\theta(L)=\left.\ -kd\theta/dx\right|_{x=L}
        ''' )

    st.markdown('Sendo:')
    _cols = st.columns(4)
    with _cols[0]:
        st.latex(r'''
        m^2\equiv\frac{hP}{kA_c}
        ''')
    with _cols[1]:
        st.latex(r'''
        M\equiv\sqrt{hPkA_c\theta_b}
        ''')
    with _cols[2]:
        st.latex(r'''
        \theta\equiv T-T_\infty
        ''')
    with _cols[3]:
        st.latex(r'''
        \theta_b=\theta(0)=T_b-T_\infty
        ''')

    st.markdown('Distribuição da temperatura:')
    st.latex(r'''
            \frac{\theta}{\theta_b}=\frac{cosh\ m(L-x)\ +\ (\frac{h}{mk})\ sinh\ m(L-x)\ }{cosh\ mL\ +\ (\frac{h}{mk})\ sinh\ mL\ }
            ''')

    st.markdown('Taxa de transferência de calor na aleta:')
    st.latex(r'''
            q_a=\ M\frac{sinh\ mL+\left(\frac{h}{mk}\right)\ cosh\ mL}{cosh\ mL+\left(\frac{h}{mk}\right)\ sinh\ mL} 
            ''')

_cols = st.columns(3)
with _cols[0]:
    t = dic['temperatura_base']
    st.latex(r'''\theta_b='''+ rf'''{t} K''')
with _cols[1]:
    tam = dic['tamanho']
    st.latex(r'''L='''+ rf'''{tam} m''')

# ''' CÁLCULO SEGUINDO AS FÓRMULAS ACIMA:'''

m = dic['m'] = np.sqrt(dic['h'] * dic['perimetro'] / dic['k'] * dic['area_c'])
L = dic['tamanho']
h = dic['h']
k = dic['k']

x = np.linspace(0, L, num=100)

theta = (np.cosh(m * (L-x)) + ((h/(m*k)) * np.sinh(m*(L-x))))/(np.cosh(m * L) + ((h/(m*k)) * np.sinh(m*L)))

st.plotly_chart(px.line(theta))