import os
import re
import json
import requests
from config import Config

GROQ_API_KEY = Config.GROQ_API_KEY
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"

def obter_ticker_b3(nome_empresa):
	"""
	Usa IA da Groq para retornar o ticker correto da B3.
	Retorna string (ex: PETR4) ou None.
	"""
	if not GROQ_API_KEY:
		return None
	prompt = f"""
Retorne APENAS o ticker da B3 (ex: PETR4, VALE3, ITUB4).
Empresa informada: "{nome_empresa}"

Regras:
- Se o nome não for de uma empresa válida, verifique se o usuário não digitou errado e corrija
- Corrija erros de digitação
- Use o ticker mais negociado
- Não explique nada
- Se não souber, retorne "DESCONHECIDO"
"""
	
	try:
		response = requests.post(
			GROQ_URL,
			headers={
				"Authorization": f"Bearer {GROQ_API_KEY}",
				"Content-Type": "application/json"
			},
			json={
				"model": MODEL,
				"messages": [{"role": "user", "content": prompt}],
				"temperature": 0,
				"max_tokens": 10
			},
			timeout=15
		)

		if response.status_code != 200:
			print("Groq error:", response.text)
			return None

		data = response.json()
		choices = data.get("choices")
		if not choices:
			return None

		ticker = choices[0]["message"]["content"].strip().upper()

		if ticker == "DESCONHECIDO":
			return None

		# valida formato B3
		if not re.match(r"^[A-Z]{4,5}\d{1,2}$", ticker):
			return None

		return ticker

	except Exception as e:
		print(f"Groq exception: {e}")
		return None
	
def obter_nome_empresa(ticker):
	"""
	Usa IA da Groq para retornar o ticker correto da B3.
	Retorna string (ex: PETR4) ou None.
	"""
	if not GROQ_API_KEY:
		return None
	prompt = f"""
Retorne APENAS o nome popular da empresa com base no seu ticker
Ticker informada: "{ticker}"

Regras:
- Sempre retorne o nome popular da empresa. Ex: Petróleo Brasileiro S.A. - Petrobras = Petrobras
- O nome deve ser apenas uma palavra
- Se não souber, retorne "DESCONHECIDO"
"""
	
	try:
		response = requests.post(
			GROQ_URL,
			headers={
				"Authorization": f"Bearer {GROQ_API_KEY}",
				"Content-Type": "application/json"
			},
			json={
				"model": MODEL,
				"messages": [{"role": "user", "content": prompt}],
				"temperature": 0,
				"max_tokens": 10
			},
			timeout=15
		)

		if response.status_code != 200:
			print("Groq error:", response.text)
			return None

		data = response.json()
		choices = data.get("choices")
		if not choices:
			return None

		nome_empresa = choices[0]["message"]["content"].strip()

		if nome_empresa == "DESCONHECIDO":
			return None

		return nome_empresa

	except Exception as e:
		print(f"Groq exception: {e}")
		return None


def filtrar_noticias_empresa(nome_empresa, noticias):
	prompt = f"""
Você receberá uma lista de notícias.
Retorne APENAS as notícias que tenham relação direta ou impacto potencial na empresa "{nome_empresa}".

Responda SOMENTE com um JSON válido no formato:
[
  {{
	"titulo": "...",
	"link": "...",
	"fonte": "...",
	"data": "..."
  }}
]

Lista de notícias:
{json.dumps(noticias, ensure_ascii=False)}
"""

	try:
		response = requests.post(
			GROQ_URL,
			headers={
				"Authorization": f"Bearer {GROQ_API_KEY}",
				"Content-Type": "application/json"
			},
			json={
				"model": MODEL,
				"messages": [
					{"role": "user", "content": prompt}
				],
				"temperature": 0
			},
			timeout=15
		)

		response.raise_for_status()

		content = response.json()["choices"][0]["message"]["content"]
		return json.loads(content)

	except Exception as e:
		print(f"[ERRO GROQ] {e}")
		return []
