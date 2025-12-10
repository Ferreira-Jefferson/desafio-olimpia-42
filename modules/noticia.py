import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from config import Config
import time

def buscar_noticias_rss(nome_empresa):
    """
    Busca notícias em sites financeiros brasileiros e retorna com links reais
    """
    noticias = []
    
    sites = [
        {
            "nome": "Investing.com Brasil",
            "url": f"https://br.investing.com/search/?q={nome_empresa}",
            "seletor": ".articleItem",
            "link_seletor": "a.title",  # Seletor específico para o link
            "base_url": "https://br.investing.com"  # Para links relativos
        },
        {
            "nome": "Valor Econômico",
            "url": f"https://www.valor.com.br/busca?search={nome_empresa}",
            "seletor": ".search-result",
            "link_seletor": "a",  # Seletor para o link dentro do resultado
            "base_url": "https://www.valor.com.br"
        },
        {
            "nome": "InfoMoney",
            "url": f"https://www.infomoney.com.br/?s={nome_empresa}",
            "seletor": ".noticia-post",
            "link_seletor": "a",  # Seletor para o link
            "base_url": "https://www.infomoney.com.br"
        }
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    for site in sites:
        try:
            response = requests.get(site["url"], headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            artigos = soup.select(site["seletor"])[:3]  # Limita a 3 artigos por site
            
            for artigo in artigos:
                # Tenta encontrar o título
                titulo_elem = artigo.find(['h2', 'h3', 'h4', 'a', 'span'])
                titulo = titulo_elem.get_text(strip=True) if titulo_elem else "Título não disponível"
                
                # Tenta encontrar o link REAL
                link_elem = artigo.select_one(site.get("link_seletor", "a"))
                if link_elem and link_elem.has_attr('href'):
                    link_raw = link_elem['href']
                    
                    # Converte link relativo para absoluto
                    if link_raw.startswith('/'):
                        link = site["base_url"] + link_raw
                    elif link_raw.startswith('http'):
                        link = link_raw
                    else:
                        link = site["base_url"] + '/' + link_raw
                else:
                    link = site["url"]  # Fallback para URL de busca
                
                # Verifica se é uma notícia relevante (contém nome da empresa)
                if titulo and len(titulo) > 20 and any(termo in titulo.lower() for termo in nome_empresa.lower().split()):
                    noticias.append({
                        "titulo": titulo[:150] + "..." if len(titulo) > 150 else titulo,
                        "link": link,
                        "fonte": site["nome"],
                        "data": datetime.now().strftime("%d/%m/%Y")
                    })
                    
                    if len(noticias) >= 5:  # Limita total de notícias
                        break
            time.sleep(0.5)
        except requests.exceptions.RequestException as e:
            print(f"[ERRO] Não foi possível acessar {site['nome']}: {e}")
            continue
        except Exception as e:
            print(f"[ERRO] Processando {site['nome']}: {e}")
            continue
    
    return noticias[:5]