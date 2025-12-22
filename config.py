import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # URLs para consultas
    RSS_FEEDS = {
        "infomoney": "https://www.infomoney.com.br/feed/",
        "investing": "https://br.investing.com/rss/news_301.rss"
    }
    
    # Configurações Yahoo Finance
    YAHOO_BASE_URL = "https://query1.finance.yahoo.com/v8/finance/chart/"