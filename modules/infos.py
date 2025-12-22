import requests
from bs4 import BeautifulSoup
import yfinance as yf
from modules.groq_client import obter_ticker_b3

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
	Encontra o ticker da empresa usando IA (Groq).
	"""
	ticker = obter_ticker_b3(nome_empresa)

	if ticker:
		return ticker

	# Fallback simples se a IA falhar
	return nome_empresa.split()[0].upper()
