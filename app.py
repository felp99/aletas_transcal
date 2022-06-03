from random import random
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

#Salvando o pipreqs: >pipreqs --encoding=utf8 .

st.set_page_config(
     page_title="AletasApp",
     page_icon="🔩",
     layout="wide",
     initial_sidebar_state="expanded",
 )

RANDOM = False
class AletasApp:
    def __init__(self) -> None:
        self.utils()
        
        with st.sidebar:
            self.barra_lateral()

        self.geral()
        self.conteudo()

    def utils(self):
        self.componentes = {}
        self.titulo_pagina = '# 🔩 Estudo sobre Aletas'
        self.subtitulo = '##### Transferência de calor'
        self.condicoes_extremidade = ['Transferência por Convecção',
                                      'Adiabática', 
                                      'Temperatura prescrita', 
                                      'Aleta infinita']
        self.template_contexto = {
            'theta':None,
            'qa':None,
        }

        self.formulas_origem = [r'''m^2\equiv\frac{hP}{kA_c},''', 
                                r'''M\equiv\sqrt{hPkA_c\theta_b},''',
                                r'''\theta\equiv T-T_\infty,''',
                                r'''\theta_b=\theta(0)=T_b-T_\infty''']

    def barra_lateral(self):

        self.condicao_escolhida = st.selectbox(label='Condição na extremidade:',
                                        options=self.condicoes_extremidade)

        st.markdown('___')

        self.temperatura_base = st.number_input('Temperatura na base [K]', 
                                                value=self.retornar_aleatorio(100.0,100),
                                                step=10.0)
        self.temperatura_prescrita_escolhida = st.number_input(label='Temperatura prescrita [K]', 
                                                                value=self.retornar_aleatorio(100.0,100),
                                                                step=.01)
        self.L = st.number_input(label='Tamanho da aleta [m]', 
                                       value=self.retornar_aleatorio(1.0,1),
                                       step=.01)
        self.k = st.number_input(label='Coef. condução [W/mK]', 
                                 value = self.retornar_aleatorio(100.0,1000),
                                 step=10.)
        self.h = st.number_input(label='Coef. convecção [W/m²K]', 
                                 value = self.retornar_aleatorio(100.0,1000),
                                 step=10.)
        self.P =  st.number_input(label='Perímetro [m]', 
                                  value = self.retornar_aleatorio(0.5,1),
                                  step=.1)
        self.area_b = st.number_input(label='Área da base [m²]', 
                                      value= self.retornar_aleatorio(0.5,1),
                                      step=.1)

    def conteudo(self):
        st.markdown(self.titulo_pagina)
        st.markdown(self.subtitulo)

        st.markdown('''Análise do comportamento de diferentes aletas em um aplicativo Python.
                       Na barra lateral, escolha diferentes **condições na extremidade da aleta** para analisar sua **base teórica**.
                       Escolha também **diferentes parâmetros** que serão utilizados para o cálculo dos **perfis de temperatura
                       e taxa de transferência de calor**.''')

        

        self.trans_conv()
        self.adiabatica()
        self.temperatura_prescrita()
        self.aleta_infinita()

        if self.condicao_escolhida == self.condicoes_extremidade[0]:
            self.mostrar_info(self.trans_conv_info)
        elif self.condicao_escolhida == self.condicoes_extremidade[1]:
            self.mostrar_info(self.adiabatica_info)
        elif self.condicao_escolhida == self.condicoes_extremidade[2]:
            self.mostrar_info(self.temperatura_prescrita_info)
        elif self.condicao_escolhida == self.condicoes_extremidade[3]:
            self.mostrar_info(self.aleta_infinita_info)

        self.mostrar_parametros_escolhidos()

        self.plotar_resultados()

        _ = st.columns(2)

        with _[0]:
            st.caption('📚 INCROPERA, F.; DEWITT, D.P. Fundamentos de Transferência de Calor e de Massa, 7ed., Rio de Janeiro: LTC, 2014.')
        with _[1]:
            st.caption(f'👨🏻‍💻 Código fonte: https://github.com/felp99/aletas_transcal')

    def geral(self):
        self.m = np.sqrt(self.h * self.P / self.k * self.area_b)
        self.x = np.linspace(start = 0, stop = self.L, num=100)
        self.M = np.sqrt(self.h * self.P * self.k * self.area_b) * self.temperatura_base

    def eficiencia_calc(self, qa):
        return qa/(self.h * self.P * self.L * self.temperatura_base)

    def efetividade_calc(self, qa):
        return qa/(self.h*self.temperatura_base*self.area_b)

    def trans_conv(self):

        self.trans_conv_info = {
                'Na extremidade:': r'''h\theta\left(L\right)=-\left(\frac{kd\theta}{dx}\right)_{x=L}''',
                'Distribuição da temperatura:': r'''\frac{\theta}{\theta_b}=\frac{cosh\ m(L-x)\ +\ (\frac{h}{mk})\ sinh\ m(L-x)\ }{cosh\ mL\ +\ (\frac{h}{mk})\ sinh\ mL\ }''',
                'Taxa de transferência de calor na aleta:': r'''q_a=\ M\frac{sinh\ mL+\left(\frac{h}{mk}\right)\ cosh\ mL}{cosh\ mL+\left(\frac{h}{mk}\right)\ sinh\ mL}''',
            }


        theta = (np.cosh(self.m * (self.L-self.x)) + ((self.h/(self.m*self.k)) * np.sinh(self.m*(self.L-self.x))))/(np.cosh(self.m * self.L) + ((self.h/(self.m*self.k)) * np.sinh(self.m*self.L)))
        qa =  self.M * ((np.sinh(self.m*self.L)+((self.h/(self.m*self.k))* np.cosh(self.m * self.L)))/(np.cosh(self.m*self.L)+((self.h/(self.m*self.k))* np.sinh(self.m * self.L))))
        
        context = {}
        context['theta'] = theta
        context['qa']  = qa
        context['titulo'] = self.condicoes_extremidade[0]
        context['eficiencia'] = self.eficiencia_calc(qa)
        context['efetividade'] = self.efetividade_calc(qa)
        self.trans_conv_resultado =  context

    def adiabatica(self):

        self.adiabatica_info = {
                'Na extremidade:': r'''-\left(\frac{kd\theta}{dx}\right)_{x=L}=0''',
                'Distribuição da temperatura:': r'''\frac{\theta}{\theta_b}=\frac{cosh\ m\left(L-x\right)\ \ }{L}''',
                'Taxa de transferência de calor na aleta:': r'''q_a=M\ tanh\ (mL)''',
            }

        theta = np.cosh(self.m * (self.L-self.x))/np.cosh(self.m*self.L)
        qa =  self.M * np.tanh(self.m*self.L)

        context = {}
        context['theta'] = theta
        context['qa']  = qa
        context['titulo'] = self.condicoes_extremidade[1]
        context['eficiencia'] = self.eficiencia_calc(qa)
        context['efetividade'] = self.efetividade_calc(qa)
        self.adiabatica_resultado = context

    def temperatura_prescrita(self):

        self.temperatura_prescrita_info = {
                'Na extremidade:': r'''\theta_L=\theta\left(L\right)''' + rf'''= {round(self.temperatura_prescrita_escolhida, 2)} K''',
                'Distribuição da temperatura:': r'''\frac{\theta}{\theta_b}=\frac{\left(\frac{\theta_L}{\theta_b}\right)sinh\ (mx)\ +\ sinh\ m(L-x)}{sinh\ (mL)}''',
                'Taxa de transferência de calor na aleta:': r'''q_a=M\frac{\left(cosh\ mL\ -\ \frac{\theta_L}{\theta_b}\right)}{sinh\ mL}''',
            }

        theta = ((self.temperatura_prescrita_escolhida/self.temperatura_base)*np.sinh(self.m*self.x)) + np.sinh(self.m*(self.L-self.x))/np.sinh(self.m*self.L)
        qa =  self.M * (np.cosh(self.m*self.L)-(self.temperatura_prescrita_escolhida/self.temperatura_base))/np.sinh(self.m*self.L)

        context = {}
        context['theta'] = theta
        context['qa']  = qa
        context['titulo'] = self.condicoes_extremidade[2]
        context['eficiencia'] = self.eficiencia_calc(qa)
        context['efetividade'] = self.efetividade_calc(qa)
        self.temperatura_prescrita_resultado = context


    def aleta_infinita(self):
        
        self.aleta_infinita_info = {
                'Na extremidade:': r'''\left(L\rightarrow \infty\right):\ \theta(L)=0''',
                'Distribuição da temperatura:': r'''\frac{\theta}{\theta_b}=e^{-mx}''',
                'Taxa de transferência de calor na aleta:': r'''q_a=M''',
            }
        theta = np.exp(-self.m * self.x)
        qa =  self.M

        context = {}
        context['theta'] = theta
        context['qa']  = qa
        context['titulo'] = self.condicoes_extremidade[3]
        context['eficiencia'] = self.eficiencia_calc(qa)
        context['efetividade'] = self.efetividade_calc(qa)
        self.aleta_infinita_resultado = context

    def plotar_resultados(self):

        dicionario_resultados = {
            'trans_conv':self.trans_conv_resultado,
            'adiabatica':self.adiabatica_resultado,
            'temperatura_prescrita':self.temperatura_prescrita_resultado,
            'aleta_infinita':self.aleta_infinita_resultado,
        }

        df = pd.DataFrame()
        
        st.markdown('### Resultados:')
        st.markdown('##### Comparação dos resultados:')
        _colunas_metricas = st.columns(4)
        for ncondicao, condicao in enumerate(dicionario_resultados):
            theta = dicionario_resultados[condicao]['theta']
            qa = dicionario_resultados[condicao]['qa']
            eficiencia = dicionario_resultados[condicao]['eficiencia']

            df.loc[dicionario_resultados[condicao]['titulo'], 'Taxa'] = f'{round(qa,2)} W'
            df.loc[dicionario_resultados[condicao]['titulo'], 'Eficiência'] = eficiencia
        st.table(df)

        fig = go.Figure()
        st.markdown('##### Perfil da temperatura:')
        for ncondicao, condicao in enumerate(dicionario_resultados):
            theta = dicionario_resultados[condicao]['theta']
            fig.add_trace(go.Line(
                x = self.x,
                y = theta * self.temperatura_base,
                name=dicionario_resultados[condicao]['titulo'],
            ))
            
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            autosize=True,
            yaxis_title="θ [K]",
            xaxis_title="L [m]",
            legend_title="Condição na extremidade:", 
            hovermode=f"x")    

        st.plotly_chart(fig)        

    def mostrar_parametros_escolhidos(self):
        _cols = st.columns(4)
        with _cols[0]:
            st.latex(r'''\theta_b='''+ rf'''{round(self.temperatura_base, 2)} K''')
        with _cols[1]:
            st.latex(r'''L='''+ rf'''{round(self.L, 2)} m''')
        with _cols[2]:
            st.latex(r'''k='''+ rf'''{round(self.k, 2)} '''+ r'''\frac{h}{mk}''')
        with _cols[3]:
            st.latex(r'''h='''+ rf'''{round(self.h, 2)} '''+ r'''\frac{h}{m^2k}''')

        _cols = st.columns(2)
        with _cols[0]:
            st.latex(r'''P='''+ rf'''{round(self.P,2)} m''')
        with _cols[1]:
            st.latex(r'''A_b='''+ rf'''{round(self.area_b,2)} m^2''')

    def mostrar_info(self, infos):

        with st.expander(f'📝 Base teórica: {self.condicao_escolhida}', expanded=False):

            st.markdown('Sendo:')
            _c = st.columns(len(self.formulas_origem))
            for nc, c in enumerate(_c):
                with c:
                    st.latex(self.formulas_origem[nc])

            for info in infos:
                st.markdown(info)
                st.latex(infos[info])

    def retornar_aleatorio(self, default, multiplicador_random):
        return default if not RANDOM else random() * multiplicador_random

AletasApp()