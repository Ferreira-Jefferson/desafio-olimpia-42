import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_community.chains import LLMChain
from config import Config

class GeminiProcessor:
    def __init__(self):
        if not Config.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY não encontrada. Configure no arquivo .env")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=Config.GOOGLE_API_KEY,
            temperature=0.3
        )
    
    def resumir_dados_com_json(self, empresa, dados_coletados):
        """
        Usa o Gemini para pesquisar e retornar dados em formato JSON
        baseado no modelo do seu código que funciona
        """
        try:
            # Template baseado no seu código que funciona
            prompt = PromptTemplate(
                input_variables=["empresa"],
                template="""Você é um analista financeiro especializado em Investment Banking. 
Forneça informações ATUALIZADAS sobre a empresa: {empresa}

Use estas informações coletadas como referência:
{dados_coletados}

Forneça as seguintes informações no formato JSON exato abaixo:

{{
    "nome_oficial": "Nome oficial completo da empresa",
    "ticker": "Código da ação na B3 (ex: PETR4, VALE3)",
    "resumo": {{
        "setor": "Setor de atuação principal",
        "descricao": "Descrição breve da empresa (2-3 linhas)",
        "principais_produtos": ["produto1", "produto2", "produto3"]
    }},
    "noticias": [
        {{
            "titulo": "Título da notícia 1",
            "fonte": "Fonte da notícia",
            "resumo": "Resumo breve da notícia"
        }},
        {{
            "titulo": "Título da notícia 2", 
            "fonte": "Fonte da notícia",
            "resumo": "Resumo breve da notícia"
        }}
    ],
    "acao": {{
        "preco_atual": "Preço formatado",
        "variacao": "Variação percentual",
        "volume": "Volume negociado"
    }},
    "analise_rapida": "Breve análise da situação atual da empresa (2-3 linhas)"
}}

IMPORTANTE: 
- Baseie-se nas informações coletadas
- Complemente com seu conhecimento atual
- Retorne APENAS o JSON válido, sem texto adicional
- Formate corretamente para parse JSON
"""
            )
            
            # Prepara dados coletados para o prompt
            dados_str = f"""
DADOS COLETADOS AUTOMATICAMENTE:

1. INFORMAÇÕES BÁSICAS:
- Nome: {dados_coletados.get('info', {}).get('nome', 'N/A')}
- Setor: {dados_coletados.get('info', {}).get('setor', 'N/A')}
- Indústria: {dados_coletados.get('info', {}).get('industria', 'N/A')}

2. COTAÇÃO:
- Ticker: {dados_coletados.get('cotacao', {}).get('ticker', 'N/A')}
- Preço: R$ {dados_coletados.get('cotacao', {}).get('preco_atual', 0):.2f}
- Variação: {dados_coletados.get('cotacao', {}).get('variacao_percentual', 0):.2f}%

3. NOTÍCIAS ENCONTRADAS:
"""
            
            for i, noticia in enumerate(dados_coletados.get('noticias', []), 1):
                dados_str += f"- {noticia['titulo']} ({noticia.get('fonte', 'Fonte')})\n"
            
            # Cria a chain
            chain = LLMChain(llm=self.llm, prompt=prompt)
            
            # Executa
            resultado = chain.run({
                "empresa": empresa,
                "dados_coletados": dados_str
            })
            
            # Limpa o resultado
            resultado_limpo = resultado.strip()
            
            # Remove markdown code blocks se existirem
            if resultado_limpo.startswith("```json"):
                resultado_limpo = resultado_limpo[7:]
            elif resultado_limpo.startswith("```"):
                resultado_limpo = resultado_limpo[3:]
            
            if resultado_limpo.endswith("```"):
                resultado_limpo = resultado_limpo[:-3]
            
            resultado_limpo = resultado_limpo.strip()
            
            # Parse JSON
            dados_json = json.loads(resultado_limpo)
            return dados_json
            
        except json.JSONDecodeError as e:
            print(f"Erro ao parsear JSON: {e}")
            print(f"Resposta recebida: {resultado}")
            return None
        except Exception as e:
            print(f"Erro no Gemini: {str(e)}")
            return None