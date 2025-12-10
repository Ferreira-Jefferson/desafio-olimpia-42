import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from config import Config

class GeminiProcessor:
    def __init__(self):
        if not Config.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY não encontrada. Configure no arquivo .env")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            api_key=Config.GOOGLE_API_KEY,
            temperature=0.3
        )
    
    def resumir_dados_com_json(self, empresa, dados_coletados):
        try:
            prompt = PromptTemplate(
                input_variables=["empresa", "dados_coletados"],
                template="""
Você é um analista financeiro especializado em Investment Banking. 
Forneça informações ATUALIZADAS sobre a empresa: {empresa}

Use estas informações coletadas como referência:
{dados_coletados}

Retorne APENAS o seguinte JSON válido:

{{
    "nome_oficial": "",
    "ticker": "",
    "resumo": {{
        "setor": "",
        "descricao": "",
        "principais_produtos": []
    }},
    "noticias": [
        {{
            "titulo": "",
            "fonte": "",
            "resumo": ""
        }}
    ],
    "acao": {{
        "preco_atual": "",
        "variacao": "",
        "volume": ""
    }},
    "analise_rapida": ""
}}
"""
            )

            # Renderiza o prompt
            prompt_text = prompt.format(
                empresa=empresa,
                dados_coletados=self._formatar_dados(dados_coletados)
            )

            # Chama o modelo (API NOVA)
            response = self.llm.invoke(prompt_text)

            resultado = response.content.strip()

            # Remove blocos markdown
            resultado = resultado.replace("```json", "").replace("```", "").strip()

            # Converte para JSON
            return json.loads(resultado)

        except Exception as e:
            print(f"Erro no Gemini: {str(e)}")
            return None
    
    def _formatar_dados(self, dados):
        out = f"""
1. INFORMAÇÕES BÁSICAS:
- Nome: {dados.get('info', {}).get('nome', 'N/A')}
- Setor: {dados.get('info', {}).get('setor', 'N/A')}
- Indústria: {dados.get('info', {}).get('industria', 'N/A')}

2. COTAÇÃO:
- Ticker: {dados.get('cotacao', {}).get('ticker', 'N/A')}
- Preço: R$ {dados.get('cotacao', {}).get('preco_atual', 0):.2f}
- Variação: {dados.get('cotacao', {}).get('variacao_percentual', 0):.2f}%

3. NOTÍCIAS:
"""
        for n in dados.get("noticias", []):
            out += f"- {n.get('titulo', '')} ({n.get('fonte', '')})\n"

        return out
