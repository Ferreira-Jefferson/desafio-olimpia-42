import json
from datetime import datetime

import streamlit as st

from modules.historia import obter_resumo_empresa
from modules.cotacao import obter_cotacao_atual
from modules.noticia import buscar_noticias_rss
from modules.gemini import GeminiProcessor

# --------------------------
# Configuração da página
# --------------------------
st.set_page_config(page_title="Relatório de Empresas", layout="wide")

# --------------------------
# Utilitários
# --------------------------
def format_number(n):
    """Formata números com separador de milhar; se não for número, retorna string original."""
    try:
        nf = float(n)
        if nf.is_integer():
            return f"{int(nf):,}".replace(",", ".")
        return f"{nf:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
    except Exception:
        return str(n)

def safe_metric(label, value, delta=None):
    """Exibe metric sem estourar erro de formatação."""
    if isinstance(value, (int, float)):
        value_fmt = format_number(value)
    else:
        try:
            value_fmt = format_number(float(value))
        except Exception:
            value_fmt = str(value)
    if delta is not None:
        try:
            st.metric(label, value_fmt, delta)
        except Exception:
            st.metric(label, value_fmt)
    else:
        st.metric(label, value_fmt)

def build_report_layout(dados_json, dados_brutos):
    """Desenha o relatório executivo formatado."""
    st.title(f"📋 Relatório Executivo — {dados_json.get('nome_oficial', dados_brutos['empresa'])}")
    st.caption(f"Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    # Cabeçalho principal
    with st.container():
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        col1.markdown(f"**Ticker:** `{dados_json.get('ticker', dados_brutos.get('cotacao', {}).get('ticker', '—'))}`")
        col2.markdown(f"**Setor:** {dados_json.get('resumo', {}).get('setor', '—')}")
        acao = dados_json.get("acao", {})
        preco = acao.get("preco_atual", dados_brutos.get("cotacao", {}).get("preco_atual"))
        variacao = acao.get("variacao", dados_brutos.get("cotacao", {}).get("variacao_percentual"))
        volume = acao.get("volume", dados_brutos.get("cotacao", {}).get("volume"))

        col3.metric("Preço", f"R$ {format_number(preco) if preco is not None else '—'}")
        if isinstance(variacao, (int, float)):
            col4.metric("Variação", f"{variacao:+.2f}%")
        else:
            try:
                v = float(variacao)
                col4.metric("Variação", f"{v:+.2f}%")
            except Exception:
                col4.metric("Variação", str(variacao) if variacao else "—")

    st.markdown("---")

    # Sobre a empresa
    st.subheader("🏢 Sobre a empresa")
    desc = dados_json.get("resumo", {}).get("descricao") or dados_brutos.get("info", {}).get("descricao")
    st.markdown(f"**Descrição:**\n\n{desc or '—'}")

    produtos = dados_json.get("resumo", {}).get("principais_produtos") or []
    if produtos:
        st.markdown("**Principais produtos/serviços:**")
        for p in produtos:
            st.markdown(f"- {p}")

    st.markdown("---")

    # Cotação
    st.subheader("💰 Cotação")
    safe_metric("Preço atual", f"R$ {format_number(preco) if preco is not None else '—'}")
    delta_text = None
    if isinstance(variacao, (int, float)):
        delta_text = f"{variacao:+.2f}%"
    else:
        try:
            delta_text = f"{float(variacao):+.2f}%"
        except Exception:
            delta_text = None
    safe_metric("Variação", delta_text or (str(variacao) if variacao else "—"))
    if volume is not None:
        try:
            volume_fmt = format_number(int(volume))
        except Exception:
            volume_fmt = format_number(volume)
    else:
        volume_fmt = "—"
    safe_metric("Volume", volume_fmt)

    st.markdown("---")

    # Notícias
    st.subheader("📰 Notícias recentes")
    noticias = dados_json.get("noticias", []) or dados_brutos.get("noticias", [])
    if noticias:
        for n in noticias:
            titulo = n.get("titulo", "Sem título")
            fonte = n.get("fonte", "Fonte não informada")
            link = n.get("link")
            resumo = n.get("resumo")
            st.markdown(f"**{titulo}** — *{fonte}*")
            if link:
                st.markdown(f"[🔗 Acessar notícia]({link})")
            if resumo:
                st.markdown(f"> {resumo}")
            st.divider()
    else:
        st.info("Nenhuma notícia recente encontrada.")

    # Análise rápida
    analise = dados_json.get("analise_rapida")
    if analise:
        st.subheader("📈 Análise rápida")
        st.markdown(analise)

    st.markdown("---")

    # JSON com persistência
    st.subheader("🧾 Visualizar e baixar JSON")
    with st.expander("Ver JSON do relatório"):
        json_str = json.dumps(dados_json, ensure_ascii=False, indent=2)
        st.code(json_str, language="json")
        st.download_button(
            label="⬇️ Baixar JSON",
            data=json_str.encode("utf-8"),
            file_name=f"relatorio_{dados_json.get('ticker','empresa')}.json",
            mime="application/json",
            key="download_json"  # chave fixa evita reset
        )
        st.caption("Dica: você também pode copiar o conteúdo acima (Ctrl/Cmd + C).")

# --------------------------
# Interface principal
# --------------------------
st.title("📊 Pesquisa Automatizada de Empresas")
st.write("Sistema de análise preliminar para Investment Banking")

empresa = st.text_input("Digite o nome da empresa brasileira:", "Vale")
gerar = st.button("Gerar relatório")

if gerar and empresa.strip():
    with st.status("Iniciando...", expanded=True) as status:
        st.write("🔎 Buscando dados da empresa...")
        info = obter_resumo_empresa(empresa)

        dados_coletados = {
            "empresa": empresa,
            "info": {},
            "cotacao": {},
            "noticias": []
        }
        if info.get("status") == "sucesso":
            dados_coletados["info"] = info["dados"]
        else:
            st.warning(info.get("mensagem", "Não foi possível obter informações da empresa."))

        st.write("💹 Buscando cotação atual...")
        cotacao = obter_cotacao_atual(empresa)
        if cotacao.get("status") == "sucesso":
            dados_coletados["cotacao"] = cotacao
        else:
            st.warning(cotacao.get("mensagem", "Não foi possível obter cotação."))

        st.write("📰 Buscando notícias recentes...")
        noticias = buscar_noticias_rss(empresa)
        dados_coletados["noticias"] = noticias or []

        st.write("🧠 Gerando relatório com IA (Gemini)...")
        try:
            processor = GeminiProcessor()
            dados_finais = processor.resumir_dados_com_json(empresa, dados_coletados)
            status.update(label="Relatório gerado com sucesso!", state="complete")
        except Exception as e:
            status.update(label="Falha ao gerar relatório com IA", state="error")
            st.error(f"Erro no processamento: {str(e)}")
            dados_finais = None

    # Persistência em session_state
    st.session_state["dados_finais"] = dados_finais
    st.session_state["dados_coletados"] = dados_coletados

# Exibição final (mesmo após rerun)
if "dados_finais" in st.session_state and st.session_state["dados_finais"]:
    build_report_layout(st.session_state["dados_finais"], st.session_state["dados_coletados"])
elif "dados_coletados" in st.session_state:
    st.subheader("📄 Dados coletados (sem IA)")
    st.json(st.session_state["dados_coletados"])

elif gerar and not empresa.strip():
    st.warning("Informe o nome da empresa para continuar.")

st.caption("© Relatório gerado com o uso de IA. Uso para fins informativos.")
