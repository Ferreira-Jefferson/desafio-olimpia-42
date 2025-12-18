import requests
from bs4 import BeautifulSoup
import yfinance as yf

def obter_resumo_empresa(nome_empresa):
    """
    Obtém informações básicas da empresa usando yfinance
    """
    try:
        # Tenta encontrar o ticker correto
        ticker = encontrar_ticker(nome_empresa)
        
        if not ticker:
            return {
                "status": "erro",
                "mensagem": f"Ticker não encontrado para {nome_empresa}"
            }
        
        # Busca informações usando yfinance
        empresa = yf.Ticker(ticker + ".SA")
        info = empresa.info
        
        resumo = {
            "nome": info.get('longName', nome_empresa),
            "setor": info.get('sector', 'Não informado'),
            "industria": info.get('industry', 'Não informado'),
            "site": info.get('website', 'Não informado'),
            "descricao": info.get('longBusinessSummary', 'Não disponível'),
            "pais": info.get('country', 'Brasil'),
            "funcionarios": info.get('fullTimeEmployees', 'Não informado'),
            "ticker": ticker + ".SA"
        }
        
        return {
            "status": "sucesso",
            "dados": resumo
        }
        
    except Exception as e:
        return {
            "status": "erro",
            "mensagem": f"Erro ao buscar informações: {str(e)}"
        }

def encontrar_ticker(nome_empresa):
    """
    Mapeia nomes de empresas para tickers da B3
    """
    tickers = {
        "petrobras": "PETR4",
        "vale": "VALE3",
        "itau": "ITUB4",
        "itau unibanco": "ITUB4",
        "ambev": "ABEV3",
        "minerva": "BEEF3",
        "bradesco": "BBDC4",
        "banco do brasil": "BBAS3",
        "magazine luiza": "MGLU3",
        "via": "VIIA3",
        "jbs": "JBSS3",
        "walmart": "WALM34",
        "natura": "NTCO3",
        "renner": "LREN3",
        "suzano": "SUZB3",
        "taesa": "TAEE11"
    }
    
    nome_lower = nome_empresa.lower()
    
    for key, value in tickers.items():
        if key in nome_lower:
            return value
    
    # Se não encontrar, retorna o próprio nome (será tratado pelo yfinance)
    return nome_empresa.split()[0] if nome_empresa.split() else nome_empresa