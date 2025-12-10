import yfinance as yf
from datetime import datetime

def obter_cotacao_atual(nome_empresa):
    """
    Obtém a cotação atual da empresa
    """
    try:
        from modules.historia import encontrar_ticker
        ticker = encontrar_ticker(nome_empresa)
        
        if not ticker:
            return {
                "status": "erro",
                "mensagem": "Ticker não encontrado"
            }
        
        # Adiciona .SA para empresas brasileiras
        ticker_br = ticker + ".SA"
        empresa = yf.Ticker(ticker_br)
        
        # Obtém dados históricos recentes
        hist = empresa.history(period="1d")
        
        if hist.empty:
            return {
                "status": "erro",
                "mensagem": f"Dados não disponíveis para {ticker_br}"
            }
        
        # Informações da cotação
        ultima_cotacao = hist['Close'].iloc[-1]
        abertura = hist['Open'].iloc[-1]
        maxima = hist['High'].iloc[-1]
        minima = hist['Low'].iloc[-1]
        volume = hist['Volume'].iloc[-1]
        
        # Calcula variação
        variacao = ultima_cotacao - abertura
        variacao_percentual = (variacao / abertura) * 100 if abertura != 0 else 0
        
        return {
            "status": "sucesso",
            "ticker": ticker_br,
            "preco_atual": round(ultima_cotacao, 2),
            "abertura": round(abertura, 2),
            "maxima": round(maxima, 2),
            "minima": round(minima, 2),
            "volume": int(volume),
            "variacao": round(variacao, 2),
            "variacao_percentual": round(variacao_percentual, 2),
            "moeda": "BRL",
            "data_consulta": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        
    except Exception as e:
        return {
            "status": "erro",
            "mensagem": f"Erro ao buscar cotação: {str(e)}"
        }