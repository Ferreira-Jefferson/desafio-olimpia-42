import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Pesquisa de Empresas - Investment Banking",
    page_icon="📊",
    layout="wide"
)

# Título
st.title("📊 Pesquisa Automatizada de Empresas")
st.markdown("### Sistema de Análise Preliminar para Investment Banking")

# Sidebar para API Key
with st.sidebar:
    st.header("⚙️ Configurações")
    api_key = st.text_input("Google Gemini API Key", type="password", help="Insira sua chave de API do Google Gemini")
    st.markdown("---")
    st.markdown("**Como obter a API Key:**")
    st.markdown("1. Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)")
    st.markdown("2. Faça login com sua conta Google")
    st.markdown("3. Clique em 'Get API Key'")
    st.markdown("4. Copie e cole aqui")

# Lista de empresas sugeridas
empresas_sugeridas = [
    "Petrobras (PETR4)",
    "Vale (VALE3)",
    "Itaú Unibanco (ITUB4)",
    "Bradesco (BBDC4)",
    "Ambev (ABEV3)",
    "Minerva Foods (BEEF3)",
    "Magazine Luiza (MGLU3)",
    "B3 (B3SA3)",
    "Weg (WEGE3)",
    "Localiza (RENT3)"
]

# Input da empresa
col1, col2 = st.columns([3, 1])
with col1:
    empresa_input = st.text_input(
        "Nome da Empresa",
        placeholder="Ex: Petrobras, Vale, Itaú...",
        help="Digite o nome de uma empresa brasileira de capital aberto"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    buscar_btn = st.button("🔍 Pesquisar", use_container_width=True, type="primary")

# Sugestões
with st.expander("💡 Empresas Sugeridas"):
    cols = st.columns(5)
    for idx, empresa in enumerate(empresas_sugeridas):
        with cols[idx % 5]:
            if st.button(empresa, key=f"btn_{idx}", use_container_width=True):
                empresa_input = empresa.split("(")[0].strip()
                buscar_btn = True

def criar_chain_pesquisa(api_key):
    """Cria a chain do LangChain para pesquisa"""
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        google_api_key=api_key,
        temperature=0.3
    )
    
    prompt = PromptTemplate(
        input_variables=["empresa"],
        template="""Você é um analista financeiro especializado em Investment Banking. 
Pesquise e forneça informações ATUALIZADAS sobre a empresa: {empresa}

Você DEVE usar a ferramenta de pesquisa web para obter informações em tempo real.

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
            "data": "Data aproximada",
            "fonte": "Fonte da notícia",
            "link": "URL completo da notícia"
        }},
        {{
            "titulo": "Título da notícia 2",
            "data": "Data aproximada",
            "fonte": "Fonte da notícia",
            "link": "URL completo da notícia"
        }},
        {{
            "titulo": "Título da notícia 3",
            "data": "Data aproximada",
            "fonte": "Fonte da notícia",
            "link": "URL completo da notícia"
        }}
    ],
    "acao": {{
        "preco_atual": "R$ XX,XX",
        "variacao": "+X,XX% ou -X,XX%",
        "data_referencia": "Data da cotação",
        "volume": "Volume negociado"
    }},
    "analise_rapida": "Breve análise da situação atual da empresa (2-3 linhas)"
}}

IMPORTANTE: 
- Use APENAS informações atualizadas de 2024-2025
- Pesquise notícias RECENTES (últimos 30 dias)
- Obtenha o preço ATUAL da ação
- Retorne APENAS o JSON, sem texto adicional
"""
    )
    
    return LLMChain(llm=llm, prompt=prompt)

def exibir_resultados(dados):
    """Exibe os resultados de forma organizada"""
    
    # Cabeçalho da empresa
    st.markdown("---")
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"## {dados['nome_oficial']}")
        st.markdown(f"**Ticker:** `{dados['ticker']}`")
    
    with col2:
        st.metric("Preço da Ação", dados['acao']['preco_atual'])
    
    with col3:
        variacao = dados['acao']['variacao']
        delta_color = "normal" if "+" in variacao else "inverse"
        st.metric("Variação", variacao)
    
    # Informações da ação
    st.markdown("---")
    st.markdown("### 💰 Informações da Ação")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Data de Referência:** {dados['acao']['data_referencia']}")
    with col2:
        st.info(f"**Volume:** {dados['acao']['volume']}")
    
    # Resumo da empresa
    st.markdown("---")
    st.markdown("### 🏢 Sobre a Empresa")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"**Setor:** {dados['resumo']['setor']}")
        st.markdown(f"**Descrição:** {dados['resumo']['descricao']}")
    
    with col2:
        st.markdown("**Principais Produtos/Serviços:**")
        for produto in dados['resumo']['principais_produtos']:
            st.markdown(f"- {produto}")
    
    # Notícias
    st.markdown("---")
    st.markdown("### 📰 Notícias Recentes")
    
    for idx, noticia in enumerate(dados['noticias'], 1):
        with st.container():
            st.markdown(f"#### {idx}. {noticia['titulo']}")
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"**Fonte:** {noticia['fonte']} | **Data:** {noticia['data']}")
            with col2:
                if noticia['link'] and noticia['link'] != "N/A":
                    st.markdown(f"[🔗 Ler notícia completa]({noticia['link']})")
            st.markdown("---")
    
    # Análise rápida
    st.markdown("### 📊 Análise Rápida")
    st.success(dados['analise_rapida'])
    
    # Timestamp
    st.markdown("---")
    st.caption(f"Pesquisa realizada em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

# Processamento da pesquisa
if buscar_btn and empresa_input:
    if not api_key:
        st.error("⚠️ Por favor, insira sua API Key do Google Gemini na barra lateral.")
    else:
        with st.spinner(f"🔍 Pesquisando informações sobre {empresa_input}..."):
            try:
                # Criar chain
                chain = criar_chain_pesquisa(api_key)
                
                # Executar pesquisa
                resultado = chain.run(empresa=empresa_input)
                
                # Limpar resultado (remover markdown se houver)
                resultado_limpo = resultado.strip()
                if resultado_limpo.startswith("```json"):
                    resultado_limpo = resultado_limpo[7:]
                if resultado_limpo.startswith("```"):
                    resultado_limpo = resultado_limpo[3:]
                if resultado_limpo.endswith("```"):
                    resultado_limpo = resultado_limpo[:-3]
                resultado_limpo = resultado_limpo.strip()
                
                # Parse JSON
                dados = json.loads(resultado_limpo)
                
                # Exibir resultados
                exibir_resultados(dados)
                
                # Opção de download
                st.markdown("---")
                col1, col2, col3 = st.columns([1, 1, 2])
                with col1:
                    st.download_button(
                        label="📥 Baixar JSON",
                        data=json.dumps(dados, indent=2, ensure_ascii=False),
                        file_name=f"{dados['ticker']}_analise.json",
                        mime="application/json"
                    )
                
            except json.JSONDecodeError as e:
                st.error(f"❌ Erro ao processar resposta: {e}")
                st.code(resultado)
            except Exception as e:
                st.error(f"❌ Erro durante a pesquisa: {str(e)}")
                st.exception(e)

elif buscar_btn and not empresa_input:
    st.warning("⚠️ Por favor, digite o nome de uma empresa.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Sistema desenvolvido para análises preliminares em Investment Banking</p>
    <p>Powered by LangChain + Google Gemini + Streamlit</p>
</div>
""", unsafe_allow_html=True)