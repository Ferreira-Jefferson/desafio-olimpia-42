"""
Versão Terminal do Sistema de Pesquisa de Empresas
Para usar: python pesquisa_terminal.py
"""

import os
import json
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Cores para terminal (compatível com Windows/Linux/Mac)
class Cores:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def limpar_tela():
    """Limpa o terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Imprime o cabeçalho do sistema"""
    limpar_tela()
    print(Cores.HEADER + Cores.BOLD)
    print("=" * 80)
    print("  📊 SISTEMA DE PESQUISA AUTOMATIZADA DE EMPRESAS")
    print("  Investment Banking - Análise Preliminar")
    print("=" * 80)
    print(Cores.ENDC)

def print_separador():
    """Imprime uma linha separadora"""
    print(Cores.OKCYAN + "-" * 80 + Cores.ENDC)

def obter_api_key():
    """Obtém a API key do ambiente ou solicita ao usuário"""
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print(Cores.WARNING + "\n⚠️  API Key não encontrada no arquivo .env" + Cores.ENDC)
        print("\nPara obter sua API Key:")
        print("1. Acesse: https://makersuite.google.com/app/apikey")
        print("2. Faça login com sua conta Google")
        print("3. Clique em 'Get API Key'")
        print("4. Copie e cole aqui\n")
        
        api_key = input(Cores.BOLD + "Digite sua API Key do Google Gemini: " + Cores.ENDC).strip()
        
        if not api_key:
            print(Cores.FAIL + "\n❌ API Key não fornecida. Encerrando..." + Cores.ENDC)
            exit(1)
    
    return api_key

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
    """Exibe os resultados de forma formatada no terminal"""
    
    print("\n" + Cores.OKGREEN + Cores.BOLD)
    print("=" * 80)
    print(f"  {dados['nome_oficial']}")
    print("=" * 80)
    print(Cores.ENDC)
    
    # Informações básicas
    print(Cores.OKCYAN + f"\n📌 Ticker: " + Cores.ENDC + Cores.BOLD + dados['ticker'] + Cores.ENDC)
    print(Cores.OKCYAN + f"📂 Setor: " + Cores.ENDC + dados['resumo']['setor'])
    
    # Cotação
    print_separador()
    print(Cores.OKBLUE + Cores.BOLD + "\n💰 COTAÇÃO DA AÇÃO" + Cores.ENDC)
    print(f"   Preço Atual: {Cores.BOLD}{dados['acao']['preco_atual']}{Cores.ENDC}")
    
    variacao = dados['acao']['variacao']
    cor_variacao = Cores.OKGREEN if '+' in variacao else Cores.FAIL
    print(f"   Variação: {cor_variacao}{variacao}{Cores.ENDC}")
    print(f"   Volume: {dados['acao']['volume']}")
    print(f"   Data: {dados['acao']['data_referencia']}")
    
    # Resumo da empresa
    print_separador()
    print(Cores.OKBLUE + Cores.BOLD + "\n🏢 SOBRE A EMPRESA" + Cores.ENDC)
    print(f"\n{dados['resumo']['descricao']}")
    
    print(f"\n{Cores.BOLD}Principais Produtos/Serviços:{Cores.ENDC}")
    for i, produto in enumerate(dados['resumo']['principais_produtos'], 1):
        print(f"   {i}. {produto}")
    
    # Notícias
    print_separador()
    print(Cores.OKBLUE + Cores.BOLD + "\n📰 NOTÍCIAS RECENTES" + Cores.ENDC)
    
    for i, noticia in enumerate(dados['noticias'], 1):
        print(f"\n{Cores.BOLD}{i}. {noticia['titulo']}{Cores.ENDC}")
        print(f"   📅 {noticia['data']} | 📰 {noticia['fonte']}")
        if noticia['link'] and noticia['link'] != "N/A":
            print(f"   🔗 {noticia['link']}")
    
    # Análise rápida
    print_separador()
    print(Cores.OKBLUE + Cores.BOLD + "\n📊 ANÁLISE RÁPIDA" + Cores.ENDC)
    print(f"\n{dados['analise_rapida']}")
    
    # Timestamp
    print_separador()
    print(Cores.WARNING + f"\n⏰ Pesquisa realizada em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}" + Cores.ENDC)
    print()

def salvar_json(dados, ticker):
    """Salva os dados em arquivo JSON"""
    nome_arquivo = f"{ticker}_analise_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)
    
    print(Cores.OKGREEN + f"\n✅ Dados salvos em: {nome_arquivo}" + Cores.ENDC)

def menu_principal():
    """Menu principal do sistema"""
    empresas_sugeridas = [
        "Petrobras", "Vale", "Itaú Unibanco", "Bradesco", "Ambev",
        "Minerva Foods", "Magazine Luiza", "B3", "Weg", "Localiza"
    ]
    
    print("\n" + Cores.BOLD + "Empresas sugeridas:" + Cores.ENDC)
    for i, empresa in enumerate(empresas_sugeridas, 1):
        print(f"  {i:2d}. {empresa}")
    
    print(f"\n  {Cores.BOLD}0. Sair{Cores.ENDC}")
    print_separador()
    
    return empresas_sugeridas

def main():
    """Função principal"""
    print_header()
    
    # Obter API Key
    api_key = obter_api_key()
    
    # Criar chain
    try:
        chain = criar_chain_pesquisa(api_key)
        print(Cores.OKGREEN + "\n✅ Sistema inicializado com sucesso!" + Cores.ENDC)
    except Exception as e:
        print(Cores.FAIL + f"\n❌ Erro ao inicializar: {str(e)}" + Cores.ENDC)
        return
    
    while True:
        empresas_sugeridas = menu_principal()
        
        escolha = input(Cores.BOLD + "\nEscolha uma opção (número) ou digite o nome da empresa: " + Cores.ENDC).strip()
        
        if escolha == "0":
            print(Cores.OKGREEN + "\n👋 Até logo!" + Cores.ENDC)
            break
        
        # Determinar empresa
        if escolha.isdigit() and 1 <= int(escolha) <= len(empresas_sugeridas):
            empresa = empresas_sugeridas[int(escolha) - 1]
        else:
            empresa = escolha
        
        if not empresa:
            print(Cores.WARNING + "\n⚠️  Por favor, digite o nome de uma empresa." + Cores.ENDC)
            continue
        
        # Executar pesquisa
        print(Cores.OKCYAN + f"\n🔍 Pesquisando informações sobre {empresa}..." + Cores.ENDC)
        print(Cores.WARNING + "   (Isso pode levar alguns segundos)" + Cores.ENDC)
        
        try:
            resultado = chain.run(empresa=empresa)
            
            # Limpar resultado
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
            
            # Opção de salvar
            salvar = input(Cores.BOLD + "\n💾 Deseja salvar os dados em JSON? (s/n): " + Cores.ENDC).strip().lower()
            if salvar == 's':
                salvar_json(dados, dados['ticker'])
            
            # Continuar ou sair
            continuar = input(Cores.BOLD + "\n🔄 Pesquisar outra empresa? (s/n): " + Cores.ENDC).strip().lower()
            if continuar != 's':
                print(Cores.OKGREEN + "\n👋 Até logo!" + Cores.ENDC)
                break
            
            print_header()
            
        except json.JSONDecodeError as e:
            print(Cores.FAIL + f"\n❌ Erro ao processar resposta: {e}" + Cores.ENDC)
            print(Cores.WARNING + "\nResposta recebida:" + Cores.ENDC)
            print(resultado)
            
        except Exception as e:
            print(Cores.FAIL + f"\n❌ Erro durante a pesquisa: {str(e)}" + Cores.ENDC)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Cores.WARNING + "\n\n⚠️  Operação cancelada pelo usuário." + Cores.ENDC)
        print(Cores.OKGREEN + "👋 Até logo!" + Cores.ENDC)