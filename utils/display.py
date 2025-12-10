from colorama import init, Fore, Back, Style

# Inicializa colorama
init(autoreset=True)

def print_cabecalho(texto):
    """Imprime um cabeçalho colorido"""
    print(f"\n{Fore.CYAN}{'═' * 60}")
    print(f"{Fore.YELLOW}{'📊 ' if 'PESQUISA' in texto else '📋 '}{texto}")
    print(f"{Fore.CYAN}{'═' * 60}")

def print_secao(texto):
    """Imprime uma seção"""
    numero = texto.split('.')[0] if '.' in texto else ""
    titulo = texto.split('. ')[1] if '. ' in texto else texto
    print(f"\n{Fore.GREEN}{numero}. {Fore.WHITE}{'▶ ' if not numero else ''}{Style.BRIGHT}{titulo}")
    print(f"{Fore.LIGHTBLACK_EX}{'─' * 40}")

def print_sucesso(texto):
    """Imprime mensagem de sucesso"""
    print(f"{Fore.GREEN}✓ {texto}")

def print_erro(texto):
    """Imprime mensagem de erro"""
    print(f"{Fore.RED}✗ {texto}")

def print_info(texto):
    """Imprime informação"""
    print(f"{Fore.BLUE}ℹ {texto}")

def print_cotacao(dados):
    """Imprime dados da cotação formatados"""
    if dados['status'] == 'sucesso':
        variacao = dados['variacao_percentual']
        cor = Fore.GREEN if variacao >= 0 else Fore.RED
        sinal = "+" if variacao >= 0 else ""
        
        print(f"{Fore.WHITE}Ticker: {Fore.YELLOW}{dados['ticker']}")
        print(f"{Fore.WHITE}Preço Atual: {Fore.WHITE}R$ {dados['preco_atual']:.2f}")
        print(f"{Fore.WHITE}Variação: {cor}{sinal}{variacao:.2f}%")
        print(f"{Fore.WHITE}Mín/Máx: R$ {dados['minima']:.2f} / R$ {dados['maxima']:.2f}")
        print(f"{Fore.WHITE}Volume: {dados['volume']:,}")
        print(f"{Fore.LIGHTBLACK_EX}Última atualização: {dados['data_consulta']}")
    else:
        print_erro(dados['mensagem'])

def print_noticias(noticias):
    """Imprime notícias formatadas"""
    if not noticias:
        print_erro("Nenhuma notícia encontrada")
        return
    
    for i, noticia in enumerate(noticias, 1):
        print(f"\n{Fore.CYAN}{i}. {noticia['titulo'][:80]}...")
        print(f"{Fore.LIGHTBLACK_EX}   Fonte: {noticia['fonte']}")
        print(f"{Fore.LIGHTBLACK_EX}   Data: {noticia.get('data', 'Não informada')}")