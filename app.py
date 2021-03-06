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
        self.formatos_aleta = ['Plana Retangular', 'Pino Retangular']
        self.template_contexto = {
            'theta':None,
            'qa':None,
        }

        self.formulas_origem = [r'''m^2\equiv\frac{hP}{kA_c},''', 
                                r'''M\equiv\sqrt{hPkA_c}\theta_b,''',
                                r'''\theta\equiv T-T_\infty,''',
                                r'''\theta_b=\theta(0)=T_b-T_\infty''']

    def barra_lateral(self):

        self.condicao_escolhida = st.selectbox(label='Condição na extremidade:',
                                        options=self.condicoes_extremidade)

        self.formato_aleta = st.selectbox(label='Forma da aleta:',
                                          options=self.formatos_aleta)

        if (self.formato_aleta == self.formatos_aleta[0]):
            st.image("src/aleta_ret.jpg")
        else:
            st.image("src/aleta_pino.png")

        st.markdown('___')

        self.temperatura_infinito = st.number_input('Temperatura no infinito [K]', 
                                                value=self.retornar_aleatorio(303.,100),
                                                step=10.0)

        self.temperatura_base = st.number_input('Temperatura na base [K]', 
                                                value=self.retornar_aleatorio(373.,100),
                                                step=10.0)


        self.temperatura_extremidade = st.slider(label='Temperatura na extremidade [K]', 
                                                 min_value=self.temperatura_base-10, 
                                                 max_value=self.temperatura_base+12)                  

        self.L = st.number_input(label='Comprimento da aleta (L) [mm]', 
                                       value=self.retornar_aleatorio(24.,100),
                                       step=10.)/1000

        if self.formato_aleta == self.formatos_aleta[0]:

            self.w = st.number_input(label='Largura (w) [mm]', 
                                        value=self.retornar_aleatorio(60.,100),
                                        step=10.)/1000

            self.t = st.number_input(label='Altura (t) [mm]', 
                                        value=self.retornar_aleatorio(4.,100),
                                        step=10.)/1000
        else:

            self.raio = st.number_input(label='Raio [mm]', 
                                        value=self.retornar_aleatorio(100.,100),
                                        step=10.)/1000

        self.k = st.number_input(label='Coef. condução [W/mK]', 
                                 value = self.retornar_aleatorio(50.0,1000),
                                 step=10.)

        self.h = st.number_input(label='Coef. convecção [W/m²K]', 
                                 value = self.retornar_aleatorio(50.0,1000),
                                 step=10.)


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
        if self.formato_aleta == self.formatos_aleta[0]:
            self.area_b = self.w * self.t
            self.P = (self.w * 2) + (self.t * 2)
            self.area_s = self.L * self.P
        elif self.formato_aleta == self.formatos_aleta[1]:
            self.area_b = np.pi * self.raio **2
            self.P = (self.raio * 2) * np.pi
            self.area_s = np.pi * ((self.raio*2) ** 2) /4
        self.theta_b = self.temperatura_base - self.temperatura_infinito
        self.theta_L = self.temperatura_extremidade - self.temperatura_infinito
        self.m = np.sqrt((self.h * self.P) / (self.k * self.area_b))
        self.x = np.linspace(start = 0, stop = self.L, num=100)
        self.M = np.sqrt(self.h * self.P * self.k * self.area_b) * self.theta_b

    def eficiencia_calc(self, qa):
        return qa/(self.h * self.area_s * self.theta_b)

    def efetividade_calc(self, qa):
        return qa/(self.h * self.area_b * self.theta_b)

    def trans_conv(self):

        self.trans_conv_info = {
                'Na extremidade:': r'''h\theta\left(L\right)=-\left(\frac{kd\theta}{dx}\right)_{x=L}''',
                'Distribuição da temperatura:': r'''\frac{\theta}{\theta_b}=\frac{cosh\ m(L-x)\ +\ (\frac{h}{mk})\ sinh\ m(L-x)\ }{cosh\ mL\ +\ (\frac{h}{mk})\ sinh\ mL\ }''',
                'Taxa de transferência de calor na aleta:': r'''q_a=\ M\frac{sinh\ mL+\left(\frac{h}{mk}\right)\ cosh\ mL}{cosh\ mL+\left(\frac{h}{mk}\right)\ sinh\ mL}''',
            }

        theta = (np.cosh(self.m * (self.L-self.x)) + ((self.h/(self.m*self.k)) * np.sinh(self.m*(self.L-self.x))))/(np.cosh(self.m * self.L) + ((self.h/(self.m*self.k)) * np.sinh(self.m*self.L)))
        
        qa_conv =  self.M * ((np.sinh(self.m * self.L)+((self.h/(self.m*self.k))* np.cosh(self.m * self.L)))/(np.cosh(self.m*self.L)+((self.h/(self.m*self.k))* np.sinh(self.m * self.L))))

        context = {}
        context['theta'] = theta
        context['qa']  = qa_conv
        context['titulo'] = self.condicoes_extremidade[0]
        context['eficiencia'] = self.eficiencia_calc(qa_conv)
        context['efetividade'] = self.efetividade_calc(qa_conv)
        self.trans_conv_resultado =  context

    def adiabatica(self):

        self.adiabatica_info = {
                'Na extremidade:': r'''-\left(\frac{kd\theta}{dx}\right)_{x=L}=0''',
                'Distribuição da temperatura:': r'''\frac{\theta}{\theta_b}=\frac{cosh\ m\left(L-x\right)\ \ }{L}''',
                'Taxa de transferência de calor na aleta:': r'''q_a=M\ tanh\ (mL)''',
            }

        theta = np.cosh(self.m * (self.L-self.x))/np.cosh(self.m*self.L)
        qa_adiabatica =  self.M * np.tanh(self.m*self.L)

        context = {}
        context['theta'] = theta
        context['qa']  = qa_adiabatica
        context['titulo'] = self.condicoes_extremidade[1]
        context['eficiencia'] = self.eficiencia_calc(qa_adiabatica)
        context['efetividade'] = self.efetividade_calc(qa_adiabatica)
        self.adiabatica_resultado = context

    def temperatura_prescrita(self):

        self.temperatura_prescrita_info = {
                'Na extremidade:': r'''\theta_L=\theta\left(L\right)''' + rf'''= {round(self.theta_L, 2)} K''',
                'Distribuição da temperatura:': r'''\frac{\theta}{\theta_b}=\frac{\left(\frac{\theta_L}{\theta_b}\right)sinh\ (mx)\ +\ sinh\ m(L-x)}{sinh\ (mL)}''',
                'Taxa de transferência de calor na aleta:': r'''q_a=M\frac{\left(cosh\ mL\ -\ \frac{\theta_L}{\theta_b}\right)}{sinh\ mL}''',
            }

        theta = ((self.theta_L/self.theta_b)*np.sinh(self.m*self.x)) + np.sinh(self.m*(self.L-self.x))/np.sinh(self.m*self.L)
        qa_temp_prescrita =  self.M * (np.cosh(self.m*self.L)-(self.theta_L/self.theta_b))/np.sinh(self.m*self.L)

        context = {}
        context['theta'] = theta
        context['qa']  = qa_temp_prescrita
        context['titulo'] = self.condicoes_extremidade[2]
        context['eficiencia'] = self.eficiencia_calc(qa_temp_prescrita)
        context['efetividade'] = self.efetividade_calc(qa_temp_prescrita)
        self.temperatura_prescrita_resultado = context


    def aleta_infinita(self):
        
        self.aleta_infinita_info = {
                'Na extremidade:': r'''\left(L\rightarrow \infty\right):\ \theta(L)=0''',
                'Distribuição da temperatura:': r'''\frac{\theta}{\theta_b}=e^{-mx}''',
                'Taxa de transferência de calor na aleta:': r'''q_a=M''',
            }
        theta = np.exp(-self.m * self.x)
        qa_infinita =  self.M

        context = {}
        context['theta'] = theta
        context['qa']  = qa_infinita
        context['titulo'] = self.condicoes_extremidade[3]
        context['eficiencia'] = 1/(self.m*self.L)
        context['efetividade'] = self.efetividade_calc(qa_infinita)
        self.aleta_infinita_resultado = context

    def plotar_resultados(self):

        dicionario_resultados = {}
        df = pd.DataFrame()
        
        st.markdown('___')
        st.markdown('### Resultados:')
        st.markdown('##### Comparação dos resultados:')

        dicionario_resultados = {
            'trans_conv':self.trans_conv_resultado,
            'adiabatica':self.adiabatica_resultado,
            'temperatura_prescrita':self.temperatura_prescrita_resultado,
            'aleta_infinita':self.aleta_infinita_resultado,
        }

        for ncondicao, condicao in enumerate(dicionario_resultados):
            theta = dicionario_resultados[condicao]['theta']
            qa = dicionario_resultados[condicao]['qa']
            eficiencia = dicionario_resultados[condicao]['eficiencia']
            efetividade = dicionario_resultados[condicao]['efetividade']

            df.loc[dicionario_resultados[condicao]['titulo'], 'Taxa'] = f'{round(qa,2)} W'
            df.loc[dicionario_resultados[condicao]['titulo'], 'Eficiência'] = eficiencia
            df.loc[dicionario_resultados[condicao]['titulo'], 'Efetividade'] = efetividade

        st.table(df)

        fig = go.Figure()
        st.markdown('##### Perfil da temperatura:')
        for ncondicao, condicao in enumerate(dicionario_resultados):
            theta = dicionario_resultados[condicao]['theta']
            fig.add_trace(go.Line(
                x = self.x,
                y = theta * self.theta_b,
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
        st.markdown('___')

    def mostrar_parametros_escolhidos(self):
        _cols = st.columns(4)
        with _cols[0]:
            st.latex(r'''\theta_b='''+ rf'''{round(self.theta_b, 2)} K''')
        with _cols[1]:
            st.latex(r'''L='''+ rf'''{round(self.L, 2)} m''')
        with _cols[2]:
            st.latex(r'''k='''+ rf'''{round(self.k, 2)} '''+ r'''\frac{h}{mk}''')
        with _cols[3]:
            st.latex(r'''h='''+ rf'''{round(self.h, 2)} '''+ r'''\frac{h}{m^2k}''')

        _cols = st.columns(3)
        with _cols[0]:
            st.latex(r'''P\simeq'''+ rf'''{round(self.P,2)} m''')
        with _cols[1]:
            st.latex(r'''A_b\simeq'''+ rf'''{round(self.area_b,4)} m^2''')
        with _cols[2]:
            st.latex(r'''A_s\simeq'''+ rf'''{round(self.area_s,4)} m^2''')

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