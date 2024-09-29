import sys
print(sys.executable)
print(sys.path)
import pandas as pd  # Biblioteca usada para manipulação de dados (DataFrames)
import requests  # Biblioteca usada para fazer requisições HTTP
import json  # Biblioteca para trabalhar com dados no formato JSON
from datetime import datetime, timedelta  # Utilizadas para manipulação de datas e tempos

# Função para coletar dados da API OpenSky
def coletar_dados_opensky(inicio, fim):
    url = "https://opensky-network.org/api/flights/all"  # URL da API para todos os voos
    params = {
        'begin': inicio,  # Timestamp do início (em segundos desde 1970, o formato que a API aceita)
        'end': fim        # Timestamp do fim (em segundos desde 1970)
    }

    # Faz a requisição GET à API com os parâmetros de tempo definidos
    response = requests.get(url, params=params)
    
    # Verifica se a requisição foi bem-sucedida (código 200 significa sucesso)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)  # Transformando os dados em um DataFrame para facilitar a análise
        return df
    else:
        print(f"Erro ao coletar dados: {response.status_code} - {response.text}")
        return None  # Retorna 'None' se houver algum erro

# Definindo o período de coleta (última 1 hora)
hoje = datetime.now()  # Momento atual
inicio = int((hoje - timedelta(hours=1)).timestamp())  # Timestamp de uma hora atrás
fim = int(hoje.timestamp())  # Timestamp do momento atual

# Coletar dados
dados_voos = coletar_dados_opensky(inicio, fim)

# Verifica se os dados foram coletados com sucesso
if dados_voos is not None:
    print(dados_voos.head())
    print(dados_voos.describe())
else:
    print("Nenhum dado foi coletado.")

# Verificando se há valores ausentes em cada coluna
print("Valores ausentes antes da limpeza:")
print(dados_voos.isnull().sum())  # Exibe a contagem de valores ausentes por coluna

# Removendo linhas com valores ausentes
dados_voos_limpos = dados_voos.dropna()  # Remove qualquer linha que tenha pelo menos um valor ausente

# Verificando se ainda existem valores ausentes após a limpeza
print("Valores ausentes após a limpeza:")
print(dados_voos_limpos.isnull().sum())  # Exibe a contagem de valores ausentes novamente

# Removendo duplicatas, se houver
dados_voos_limpos = dados_voos_limpos.drop_duplicates()  # Remove linhas duplicadas do DataFrame

# Exibindo estatísticas descritivas
print("Estatísticas descritivas:")
print(dados_voos_limpos.describe())  # Mostra estatísticas como média, desvio padrão, etc., para colunas numéricas

# Extraindo a hora da coluna 'firstSeen'
dados_voos_limpos['hora'] = pd.to_datetime(dados_voos_limpos['firstSeen'], unit='s')

# Importando bibliotecas de visualização
import matplotlib.pyplot as plt  # Biblioteca para plotagem de gráficos
import seaborn as sns  # Biblioteca para visualização de dados baseada em matplotlib

# Configurando estilo do seaborn
sns.set(style='whitegrid')  # Define o estilo dos gráficos

# Histogramas para visualizar a distribuição do número de voos por hora
plt.figure(figsize=(12, 6))  # Define o tamanho da figura
sns.histplot(dados_voos_limpos['hora'].dt.hour, bins=24, kde=False)  # Cria um histograma com horas dos voos
plt.title('Distribuição de Voos por Hora do Dia')  # Título do gráfico
plt.xlabel('Hora do Dia')  # Rótulo do eixo X
plt.ylabel('Número de Voos')  # Rótulo do eixo Y
plt.xticks(range(0, 24))  # Define os ticks do eixo X para representar cada hora do dia
plt.show()  # Exibe o gráfico
