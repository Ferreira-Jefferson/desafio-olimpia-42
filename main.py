import sys
import json
from datetime import datetime
from modules.historia import obter_resumo_empresa
from modules.noticia import buscar_noticias_rss
from modules.cotacao import obter_cotacao_atual
from modules.gemini import GeminiProcessor
from utils.display import *

def main():
    # Cabeçalho do sistema
    print_cabecalho("📊 PESQUISA AUTOMATIZADA DE EMPRESAS")
    print(f"{Fore.LIGHTBLACK_EX}Sistema de Análise Preliminar para Investment Banking\n")
    
    # Lista de empresas sugeridas
    empresas_sugeridas = [
        "Petrobras", "Vale", "Itaú Unibanco", "Bradesco", "Ambev",
        "Minerva Foods", "Magazine Luiza", "B3", "Weg", "Localiza"
    ]
    
    print(f"{Fore.CYAN}💡 Empresas sugeridas: {', '.join(empresas_sugeridas[:5])}...")
    
    # Solicita nome da empresa
    print(f"\n{Fore.WHITE}Digite o nome da empresa brasileira:")
    empresa = input(f"{Fore.YELLOW}>>> {Fore.WHITE}").strip()
    
    if not empresa:
        print_erro("Nome da empresa não fornecido")
        sys.exit(1)
    
    print_info(f"Iniciando pesquisa para: {empresa}")
    
    # 1. Coleta dados brutos
    dados_coletados = {
        "empresa": empresa,
        "info": {},
        "cotacao": {},
        "noticias": []
    }
    
    # Busca informações da empresa
    print_secao("1. BUSCANDO INFORMAÇÕES DA EMPRESA")
    info = obter_resumo_empresa(empresa)
    if info['status'] == 'sucesso':
        dados_coletados['info'] = info['dados']
        print_sucesso(f"✓ Informações obtidas: {info['dados']['nome']}")
    else:
        print_erro(f"✗ {info['mensagem']}")
    
    # Busca cotação
    print_secao("2. BUSCANDO COTAÇÃO ATUAL")
    cotacao = obter_cotacao_atual(empresa)
    if cotacao['status'] == 'sucesso':
        dados_coletados['cotacao'] = cotacao
        print_cotacao(cotacao)
    else:
        print_erro(f"✗ {cotacao['mensagem']}")
    
    # Busca notícias
    print_secao("3. BUSCANDO NOTÍCIAS RECENTES")
    noticias = buscar_noticias_rss(empresa)
    dados_coletados['noticias'] = noticias
    
    if noticias:
        print_sucesso(f"✓ Encontradas {len(noticias)} notícias")
        for i, noticia in enumerate(noticias[:3], 1):
            print(f"{Fore.WHITE}  {i}. {noticia['titulo'][:80]}...")
    else:
        print_erro("✗ Nenhuma notícia encontrada")
    
    # 2. Processa com Gemini
    print_secao("4. GERANDO RELATÓRIO COM LANGCHAIN + GEMINI")
    
    try:
        processor = GeminiProcessor()
        print_info("🔍 Processando dados coletados...")
        
        dados_finais = processor.resumir_dados_com_json(empresa, dados_coletados)
        
        if dados_finais:
            exibir_relatorio(dados_finais, dados_coletados)
        else:
            print_erro("Não foi possível gerar o relatório com IA")
            exibir_dados_brutos(dados_coletados)
            
    except ValueError as e:
        print_erro(f"Erro de configuração: {str(e)}")
        print_info("Configure sua GOOGLE_API_KEY no arquivo .env")
        exibir_dados_brutos(dados_coletados)
    except Exception as e:
        print_erro(f"Erro no processamento: {str(e)}")
        exibir_dados_brutos(dados_coletados)
    
    # Finalização
    print_cabecalho("✅ PESQUISA CONCLUÍDA")
    print(f"\n{Fore.GREEN}Relatório gerado com sucesso!")
    print(f"{Fore.LIGHTBLACK_EX}Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"\n{Fore.WHITE}Pressione Enter para sair...")
    input()

def exibir_relatorio(dados_json, dados_brutos):
    """Exibe o relatório formatado no terminal"""
    print_cabecalho(f"📋 RELATÓRIO - {dados_json['nome_oficial']}")
    
    # Cabeçalho com ticker
    print(f"\n{Fore.YELLOW}🏢 {dados_json['nome_oficial']}")
    print(f"{Fore.CYAN}Ticker: {dados_json['ticker']}")
    
    # Informações da ação
    print(f"\n{Fore.GREEN}💰 COTAÇÃO ATUAL")
    print(f"{Fore.WHITE}Preço: {dados_json['acao']['preco_atual']}")
    print(f"{Fore.WHITE}Variação: {dados_json['acao']['variacao']}")
    print(f"{Fore.WHITE}Volume: {dados_json['acao']['volume']}")
    
    # Resumo da empresa
    print(f"\n{Fore.GREEN}📊 SOBRE A EMPRESA")
    print(f"{Fore.WHITE}Setor: {dados_json['resumo']['setor']}")
    print(f"\n{Fore.CYAN}Descrição:")
    print(f"{Fore.WHITE}{dados_json['resumo']['descricao']}")
    
    print(f"\n{Fore.CYAN}Principais produtos/serviços:")
    for produto in dados_json['resumo']['principais_produtos']:
        print(f"{Fore.WHITE}• {produto}")
    
    # Notícias
    print(f"\n{Fore.GREEN}📰 NOTÍCIAS RECENTES")
    for i, noticia in enumerate(dados_json['noticias'], 1):
        print(f"\n{Fore.YELLOW}{i}. {noticia['titulo']}")
        print(f"{Fore.LIGHTBLACK_EX}Fonte: {noticia['fonte']}")
        if 'resumo' in noticia:
            print(f"{Fore.WHITE}{noticia['resumo']}")
    
    # Análise rápida
    print(f"\n{Fore.GREEN}📈 ANÁLISE RÁPIDA")
    print(f"{Fore.CYAN}{dados_json['analise_rapida']}")
    
    # Dados brutos de referência
    print(f"\n{Fore.LIGHTBLACK_EX}{'═' * 60}")
    print(f"{Fore.LIGHTBLACK_EX}DADOS BRUTOS COLETADOS:")
    if dados_brutos['cotacao'].get('preco_atual'):
        print(f"{Fore.LIGHTBLACK_EX}Preço bruto: R$ {dados_brutos['cotacao']['preco_atual']:.2f}")
    print(f"{Fore.LIGHTBLACK_EX}{'═' * 60}")

def exibir_dados_brutos(dados_coletados):
    """Exibe dados brutos quando o Gemini falha"""
    print_cabecalho("📄 DADOS COLETADOS (SEM IA)")
    
    print(f"\n{Fore.YELLOW}Empresa: {dados_coletados['empresa']}")
    
    if dados_coletados['info']:
        print(f"\n{Fore.GREEN}Informações:")
        for key, value in dados_coletados['info'].items():
            if key in ['nome', 'setor', 'industria'] and value:
                print(f"{Fore.WHITE}{key}: {Fore.CYAN}{value}")
    
    if dados_coletados['cotacao'].get('preco_atual'):
        print(f"\n{Fore.GREEN}Cotação:")
        print(f"{Fore.WHITE}Preço: R$ {dados_coletados['cotacao']['preco_atual']:.2f}")
        print(f"{Fore.WHITE}Variação: {dados_coletados['cotacao']['variacao_percentual']:.2f}%")
    
    if dados_coletados['noticias']:
        print(f"\n{Fore.GREEN}Notícias encontradas:")
        for i, noticia in enumerate(dados_coletados['noticias'][:3], 1):
            print(f"{Fore.WHITE}{i}. {noticia['titulo'][:100]}...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⏹️ Operação cancelada pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print_erro(f"❌ Erro inesperado: {str(e)}")
        sys.exit(1)