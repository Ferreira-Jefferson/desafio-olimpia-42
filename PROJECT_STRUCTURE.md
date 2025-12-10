# 📁 Estrutura do Projeto

## 🗂️ Organização Recomendada

```
desafio-olimpia-42/
│
├── 📄 app.py                          # Aplicação Streamlit principal
├── 📄 pesquisa_terminal.py           # Versão terminal alternativa
├── 📄 test_sistema.py                # Script de testes automatizados
│
├── 📋 requirements.txt                # Dependências Python
├── 📋 .env.example                    # Exemplo de configuração
├── 📋 .gitignore                      # Arquivos ignorados pelo Git
│
├── 📁 .streamlit/
│   └── 📄 config.toml                # Configurações do Streamlit
│
├── 📚 docs/
│   ├── 📄 README.md                  # Documentação principal
│   ├── 📄 QUICKSTART.md              # Guia rápido de instalação
│   ├── 📄 TROUBLESHOOTING.md         # Solução de problemas
│   ├── 📄 EXAMPLES.md                # Exemplos de uso
│   ├── 📄 GEMINI_SEARCH.md           # Documentação da busca web
│   ├── 📄 EXECUTIVE_SUMMARY.md       # Resumo executivo
│   └── 📄 PROJECT_STRUCTURE.md       # Este arquivo
│
├── 📁 data/                          # (Opcional) Dados exportados
│   └── 📄 .gitkeep
│
├── 📁 tests/                         # (Opcional) Testes unitários
│   └── 📄 .gitkeep
│
└── 📁 .git/                          # Controle de versão Git
```

## 📝 Descrição dos Arquivos

### 🎯 Arquivos Principais

#### `app.py` (1.200 linhas)
**Propósito**: Interface gráfica Streamlit
- Configuração da página
- Gerenciamento de API Key
- Interface de usuário
- Exibição de resultados
- Export de dados

**Responsabilidades**:
- Layout e design
- Interação com usuário
- Integração com LangChain
- Formatação de saída

---

#### `pesquisa_terminal.py` (800 linhas)
**Propósito**: Versão linha de comando
- Interface CLI colorida
- Menu interativo
- Same funcionalidades que app.py
- Ideal para automação

**Quando usar**:
- Scripts automatizados
- Servidores sem interface gráfica
- Integração com outros sistemas
- Preferência por terminal

---

#### `test_sistema.py` (600 linhas)
**Propósito**: Validação do ambiente
- Testa instalação de pacotes
- Verifica versão Python
- Valida API Key
- Checa arquivos necessários

**Executar antes**:
- Primeira instalação
- Após mudanças no ambiente
- Troubleshooting
- Deploy em novo servidor

---

### 📋 Arquivos de Configuração

#### `requirements.txt`
```txt
streamlit>=1.28.0
langchain>=0.1.0
langchain-google-genai>=1.0.0
google-generativeai>=0.3.0
python-dotenv>=1.0.0
```

**Uso**:
```bash
pip install -r requirements.txt
```

---

#### `.env.example`
```bash
GOOGLE_API_KEY=sua_chave_api_aqui
```

**Setup**:
```bash
cp .env.example .env
# Edite .env com sua API key real
```

---

#### `.gitignore`
```bash
__pycache__/
*.pyc
.env
venv/
.streamlit/secrets.toml
*.log
data/*.json
```

**Proteção**:
- Não commita API keys
- Ignora arquivos temporários
- Mantém repo limpo

---

#### `.streamlit/config.toml`
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"

[server]
headless = true
port = 8501
```

**Customização**:
- Cores do tema
- Configurações de servidor
- Comportamento padrão

---

### 📚 Documentação

#### `README.md` (Principal)
**Conteúdo**:
- Visão geral do projeto
- Guia de instalação completo
- Instruções de uso
- Opções de hospedagem
- FAQ e troubleshooting

**Público**: Todos os usuários

---

#### `QUICKSTART.md` (Rápido)
**Conteúdo**:
- Setup em 5 minutos
- Comandos essenciais
- Deploy rápido
- Checklist

**Público**: Usuários com pressa

---

#### `TROUBLESHOOTING.md` (Problemas)
**Conteúdo**:
- Erros comuns
- Soluções detalhadas
- Comandos de diagnóstico
- Debug avançado

**Público**: Usuários com problemas

---

#### `EXAMPLES.md` (Exemplos)
**Conteúdo**:
- Exemplos de input/output
- Casos de uso
- Formato dos dados
- Dicas práticas

**Público**: Novos usuários

---

#### `GEMINI_SEARCH.md` (Técnico)
**Conteúdo**:
- Como funciona busca web
- Configuração detalhada
- Otimizações
- Best practices

**Público**: Desenvolvedores

---

#### `EXECUTIVE_SUMMARY.md` (Executivo)
**Conteúdo**:
- Visão de negócio
- ROI e métricas
- Roadmap
- Casos de uso

**Público**: Stakeholders, gestores

---

## 📁 Estrutura por Fase

### Fase 1: MVP (Mínimo Viável)
```
desafio-olimpia-42/
├── app.py
├── requirements.txt
├── .env.example
└── README.md
```
**Status**: ✅ Completo - Funcional

---

### Fase 2: Produção (Atual)
```
desafio-olimpia-42/
├── app.py
├── pesquisa_terminal.py
├── test_sistema.py
├── requirements.txt
├── .env.example
├── .gitignore
├── .streamlit/config.toml
└── docs/
    ├── README.md
    ├── QUICKSTART.md
    ├── TROUBLESHOOTING.md
    ├── EXAMPLES.md
    ├── GEMINI_SEARCH.md
    └── EXECUTIVE_SUMMARY.md
```
**Status**: ✅ Completo - Pronto para produção

---

### Fase 3: Escalável (Futuro)
```
desafio-olimpia-42/
├── src/
│   ├── __init__.py
│   ├── chains.py           # LangChain chains
│   ├── prompts.py          # Prompt templates
│   ├── parsers.py          # Output parsers
│   └── utils.py            # Funções auxiliares
│
├── tests/
│   ├── __init__.py
│   ├── test_chains.py
│   ├── test_api.py
│   └── test_integration.py
│
├── config/
│   ├── settings.py
│   └── logging.conf
│
├── app.py
├── cli.py
└── api.py                  # REST API (FastAPI)
```
**Status**: 🔮 Planejado

---

## 🎯 Arquivos por Responsabilidade

### Interface de Usuário
- `app.py` - Streamlit web
- `pesquisa_terminal.py` - CLI
- `.streamlit/config.toml` - UI config

### Lógica de Negócio
- `app.py` (create_chain_pesquisa)
- Prompts templates inline
- Parsing de respostas

### Configuração
- `requirements.txt` - Dependências
- `.env` - Variáveis de ambiente
- `.streamlit/config.toml` - Streamlit config

### Testes e Validação
- `test_sistema.py` - Testes automatizados
- Scripts de diagnóstico inline

### Documentação
- `docs/*.md` - Toda documentação
- Comentários inline no código

---

## 📊 Tamanho Estimado dos Arquivos

```
app.py                      ~35 KB
pesquisa_terminal.py        ~22 KB
test_sistema.py            ~15 KB

requirements.txt            ~200 bytes
.env.example               ~50 bytes
.gitignore                 ~300 bytes
.streamlit/config.toml     ~250 bytes

README.md                  ~25 KB
QUICKSTART.md              ~12 KB
TROUBLESHOOTING.md         ~30 KB
EXAMPLES.md                ~20 KB
GEMINI_SEARCH.md           ~18 KB
EXECUTIVE_SUMMARY.md       ~15 KB
PROJECT_STRUCTURE.md       ~10 KB

TOTAL                      ~202 KB
```

---

## 🔄 Fluxo de Dados

```
┌─────────────┐
│   Usuário   │
└──────┬──────┘
       │
       v
┌─────────────────┐
│   app.py        │
│  (Interface)    │
└────────┬────────┘
         │
         v
┌──────────────────┐
│   LangChain      │
│   (Framework)    │
└────────┬─────────┘
         │
         v
┌──────────────────┐
│  Gemini API      │
│  + Web Search    │
└────────┬─────────┘
         │
         v
┌──────────────────┐
│   Resultados     │
│   (JSON)         │
└────────┬─────────┘
         │
         v
┌──────────────────┐
│   Usuário        │
│   (Visualização) │
└──────────────────┘
```

---

## 🛠️ Comandos Úteis

### Navegação
```bash
# Listar estrutura
tree                    # Linux/Mac
dir /s /b              # Windows

# Contar linhas
find . -name "*.py" | xargs wc -l    # Linux/Mac
```

### Manutenção
```bash
# Limpar caches
find . -type d -name __pycache__ -exec rm -rf {} +
find . -name "*.pyc" -delete

# Verificar tamanho
du -sh *                # Linux/Mac
dir                     # Windows
```

### Desenvolvimento
```bash
# Rodar app principal
streamlit run app.py

# Rodar versão terminal
python pesquisa_terminal.py

# Executar testes
python test_sistema.py
```

---

## ✅ Checklist de Arquivos

Antes de fazer commit:

- [ ] ✅ Todos os arquivos .py têm docstrings
- [ ] ✅ .env não está no repositório
- [ ] ✅ .gitignore está configurado
- [ ] ✅ requirements.txt está atualizado
- [ ] ✅ Documentação está completa
- [ ] ✅ Exemplos funcionam
- [ ] ✅ Testes passam

---

## 📦 Para Distribuição

### Arquivos Essenciais (Mínimo)
```
app.py
requirements.txt
.env.example
README.md
```

### Arquivos Recomendados (Produção)
```
+ pesquisa_terminal.py
+ test_sistema.py
+ .gitignore
+ .streamlit/config.toml
+ QUICKSTART.md
```

### Arquivos Completos (Full Package)
```
+ Toda a documentação
+ Exemplos
+ Scripts de teste
+ CI/CD configs (futuro)
```

---

**Mantido por**: Equipe de Desenvolvimento
**Última atualização**: Dezembro 2024
**Versão da estrutura**: 1.0