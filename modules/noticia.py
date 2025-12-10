import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from config import Config

def buscar_noticias_rss(nome_empresa):
    """
    Busca notícias relacionadas à empresa em feeds RSS
    """
    noticias_encontradas = []
    
    try:
        # Busca no InfoMoney RSS
        feed = feedparser.parse(Config.RSS_FEEDS["infomoney"])
        
        for entry in feed.entries[:10]:  # Limita às 10 últimas
            if any(termo in entry.title.lower() for termo in nome_empresa.lower().split()):
                noticias_encontradas.append({
                    "titulo": entry.title,
                    "link": entry.link,
                    "fonte": "InfoMoney",
                    "data": entry.get('published', 'Data não disponível')
                })
                
            if len(noticias_encontradas) >= 3:
                break
                
    except Exception as e:
        print(f"Erro ao buscar RSS: {e}")
    
    # Se não encontrou no RSS, busca em sites de notícias
    if len(noticias_encontradas) < 3:
        noticias_encontradas.extend(buscar_noticias_sites(nome_empresa))
    
    return noticias_encontradas[:3]

def buscar_noticias_sites(nome_empresa):
    """
    Busca notícias em sites financeiros
    """
    noticias = []
    
    sites = [
        {
            "nome": "Investing.com",
            "url": f"https://br.investing.com/search/?q={nome_empresa}",
            "seletor": ".articleItem"
        },
        {
            "nome": "Valor Econômico",
            "url": f"https://www.valor.com.br/busca?search={nome_empresa}",
            "seletor": ".search-result"
        }
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for site in sites:
        try:
            response = requests.get(site["url"], headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Busca por notícias (simplificado - pode precisar de ajuste)
            artigos = soup.select(site["seletor"])[:2]
            
            for artigo in artigos:
                titulo = artigo.get_text(strip=True)[:100]
                if titulo and len(titulo) > 20:
                    noticias.append({
                        "titulo": titulo + "...",
                        "link": site["url"],
                        "fonte": site["nome"],
                        "data": "Hoje"
                    })
                    
        except Exception as e:
            continue
    
    return noticias