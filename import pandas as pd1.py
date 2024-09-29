import pandas as pd
import requests
from datetime import datetime, timedelta

# Função para coletar dados da API OpenSky
def coletar_dados_opensky(inicio, fim):
    url = "https://opensky-network.org/api/flights/all"
    params = {
        'begin': inicio,
        'end': fim
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        return df
    else:
        print(f"Erro ao coletar dados: {response.status_code}")
        return None

# Definindo o período de coleta (últimos 7 dias)
hoje = datetime.now()
inicio = int((hoje - timedelta(days=7)).timestamp())
fim = int(hoje.timestamp())

print(f"Início: {inicio}, Fim: {fim}")  # Verifique os valores

# Coletar dados
dados_voos = coletar_dados_opensky(inicio, fim)

if dados_voos is not None:
    print(dados_voos.isnull().sum())  # Verificar dados faltantes
    dados_voos.dropna(inplace=True)   # Remover dados faltantes

    if 'date' in dados_voos.columns:
        dados_voos['date'] = pd.to_datetime(dados_voos['date'], unit='s')

    print(dados_voos.head())
    print(dados_voos.describe())
