import feedparser
from datetime import datetime
from modules.groq_client import obter_nome_empresa, filtrar_noticias_empresa

def buscar_noticias_rss(ticker):
	noticias = []
	feeds = {
		"InfoMoney": "https://www.infomoney.com.br/feed/",
		"Investing": "https://br.investing.com/rss/news_301.rss"
	}

	nome_empresa = obter_nome_empresa(ticker)
	noticias_nao_tratadas = []

	for fonte, url in feeds.items():
		try:
			feed = feedparser.parse(url)
			for entry in feed.entries[:10]:
				noticias_nao_tratadas.append({
					"titulo": entry.title,
					"link": entry.link,
					"fonte": fonte,
					"data": getattr(entry, "published", datetime.now().strftime("%d/%m/%Y"))
				})

				if len(noticias_nao_tratadas) >= 10:
					break
		except Exception as e:
			print(f"[ERRO] Não foi possível acessar {fonte}: {e}")

	# 🔥 FILTRAGEM COM GROQ
	noticias = filtrar_noticias_empresa(nome_empresa, noticias_nao_tratadas)

	return noticias
