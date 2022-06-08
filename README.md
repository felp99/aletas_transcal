# Estudo sobre Aletas | Transferência de Calor
Análise do comportamento de diferentes aletas em um aplicativo Python.

###### Dê uma ⭐ se você gostar do repositório!
###### Faça um fork e contribua para um aplicativo mais robusto! 💪🏻

## Rodando localmente (<i>cmd</i> ou outro):

### Assumindo que você tem [Python](https://www.python.org/downloads/) e [Git](https://git-scm.com/) instalado.

Clone o repositório:
> git clone https://github.com/felp99/aletas_transcal.git

Crie um .env (ambiente de execução local do Python):
> python3 -m venv --upgrade-deps venv

Ative o .env :
> .\venv\Scripts\activate

Instale as dependências necessárias:
> pip install -r requirements.txt

Rode o app:
> streamlit run app.py

## Como utilizar o 🔩 AletasApp:

### Introdução

![image](https://user-images.githubusercontent.com/76445505/172018627-c04cd103-7263-4e0a-9ae6-c2999b2929a4.png)

### Parâmetros iniciais:

Todo o estudo desse aplicativo foi realizado com embasamento teórico no

- 📚 INCROPERA, F.; DEWITT, D.P. Fundamentos de Transferência de Calor e de Massa, 7ed., Rio de Janeiro: LTC, 2014. 

Selecione a condição na extremidade e a forma da aleta na barra lateral a esquerda.

![image](https://user-images.githubusercontent.com/76445505/172018674-f579e4f2-2be7-4d06-a7a9-b47934d3dab1.png)

#### Base teórica

Cada **Condição na Extremidade** da aleta tem um cálculo de Perfil, Taxa, Eficiência e Efetividade diferentes. O que é explicitado em:

![image](https://user-images.githubusercontent.com/76445505/172018731-35fadd81-9e58-40ff-8523-6c4dd8a753ca.png)

### Outros parâmetros:

Selecione os demais parâmetros como coef. de condução e convecção na barra lateral a esquerda.

![image](https://user-images.githubusercontent.com/76445505/172019057-28d0566f-160e-4825-bcdf-c84a2edfccfc.png)

Eles serão explicitados logo abaixo à base teórica:

![image](https://user-images.githubusercontent.com/76445505/172018922-4a3b42e4-a584-4f0c-9860-b407c6b0c8ee.png)

### Resultados:

Em **Resultados**, pode-se analisar uma comparação das diferentes condições na extremidade e suas relativas taxas, eficiências e efetividades. Também se vê os diferentes perfis de temperatura para cada caso. 

*Altere os parâmetros e verifique diferentes cenários.*

![image](https://user-images.githubusercontent.com/76445505/172018935-28a48c3e-f0dd-456f-94d9-5efb64bc6b62.png)

