# 📊 Sistema de Análise de Empresas para Investment Banking

Este projeto automatiza a coleta e análise de informações sobre empresas brasileiras de capital aberto, gerando relatórios completos com dados financeiros, notícias e análises estruturadas.

## ✨ Funcionalidades

- **🔍 Pesquisa Automatizada**: Busca informações de empresas usando múltiplas fontes
- **💰 Cotação em Tempo Real**: Consulta preços de ações via Yahoo Finance
- **📰 Notícias Atualizadas**: Coleta as últimas notícias via RSS feeds
- **🧠 Processamento com IA**: Gera relatórios estruturados usando Google Gemini
- **🖥️ Duas Interfaces Disponíveis**:
  - Interface web moderna com Streamlit
  - Versão CLI (linha de comando) para terminal

## 🚀 Como Executar o Projeto

### Pré-requisitos

- Python 3.8 ou superior
- Conta no Google AI Studio para obter API Key
- Git instalado (opcional)

### Passo 1: Configurar Ambiente

```bash
# Clone o repositório (se aplicável)
git clone <seu-repositorio>
cd desafio-olimpia-42

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### Passo 2: Configurar API Key do Gemini

1. Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crie uma nova API Key
3. No diretório do projeto, crie um arquivo `.env`:
```bash
# .env
GOOGLE_API_KEY=sua_chave_aqui
```

### Passo 3: Executar a Versão CLI (Terminal)

```bash
python main.py
```

O sistema solicitará o nome da empresa e mostrará o relatório completo no terminal.

### Passo 4: Executar a Versão Web (Streamlit)

```bash
streamlit run app.py
```

Acesse `http://localhost:8501` no seu navegador.

## 🌐 Versão Online

O projeto está disponível online em:

🔗 **https://desafio-olimpia-42-sn59tsm4u4w67ng8jyn5x9.streamlit.app/**

## 🏗️ Estrutura do Projeto

```
desafio-olimpia-42/
├── app.py                 # Interface web com Streamlit
├── main.py               # Interface CLI (terminal)
├── config.py             # Configurações do projeto
├── requirements.txt      # Dependências do Python
├── .env                  # Variáveis de ambiente (API Key)
├── modules/
│   ├── cotacao.py       # Módulo de cotação de ações
│   ├── gemini.py        # Processamento com IA Gemini
│   ├── historia.py      # Informações da empresa
│   └── noticia.py       # Coleta de notícias
└── utils/
    └── display.py       # Utilitários de exibição
```

## 📋 Empresas Suportadas

O sistema reconhece automaticamente as principais empresas brasileiras:
- Petrobras, Vale, Itaú Unibanco
- Bradesco, Ambev, Minerva Foods
- Magazine Luiza, B3, Weg, Localiza
- E muitas outras...

## 🛠️ Tecnologias Utilizadas

- **LangChain**: Framework para aplicações com LLMs
- **Google Gemini**: Modelo de IA para processamento de dados
- **Streamlit**: Framework para aplicações web em Python
- **yFinance**: Biblioteca para dados financeiros do Yahoo
- **Feedparser**: Leitor de feeds RSS para notícias
- **BeautifulSoup**: Web scraping para informações adicionais

## 📊 Exemplo de Saída

O sistema gera relatórios com:
- ✅ Nome oficial e ticker da empresa
- ✅ Setor de atuação e descrição
- ✅ Produtos/serviços principais
- ✅ Cotação atual com variação
- ✅ Notícias recentes com links
- ✅ Análise rápida gerada por IA
- ✅ Opção de download em JSON

## 🔧 Solução de Problemas

### Erro "GOOGLE_API_KEY não encontrada"
1. Verifique se o arquivo `.env` existe na raiz do projeto
2. Confirme se a API Key está correta
3. Reinicie o ambiente virtual após criar o arquivo `.env`

### Erro de dependências
```bash
# Atualize o pip e reinstale
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Empresa não encontrada
- Use o nome completo da empresa (ex: "Itaú Unibanco" ao invés de apenas "Itaú")
- Verifique se a empresa é de capital aberto na B3

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais e de demonstração técnica.

## ✍️ Autor

Sistema desenvolvido para o desafio técnico de Investment Banking, automatizando processos de due diligence e análise preliminar de empresas.

---

💡 **Dica**: Para melhores resultados, utilize os nomes completos das empresas conforme listados na B3.