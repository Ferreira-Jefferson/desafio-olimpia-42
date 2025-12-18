import feedparser
from datetime import datetime

def buscar_noticias_rss(nome_empresa):
    """
    Busca notícias reais via RSS (InfoMoney, Investing, etc.)
    """
    noticias = []
    feeds = {
        "InfoMoney": "https://www.infomoney.com.br/feed/",
        "Investing": "https://br.investing.com/rss/news_301.rss"
    }

    for fonte, url in feeds.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:  # pega até 5 notícias
                titulo = entry.title
                link = entry.link
                data = getattr(entry, "published", None)

                # filtra por nome da empresa no título
                if nome_empresa.lower() in titulo.lower():
                    noticias.append({
                        "titulo": titulo,
                        "link": link,
                        "fonte": fonte,
                        "data": data or datetime.now().strftime("%d/%m/%Y")
                    })
                if len(noticias) >= 5:
                    break
        except Exception as e:
            print(f"[ERRO] Não foi possível acessar {fonte}: {e}")
            continue

    return noticias
