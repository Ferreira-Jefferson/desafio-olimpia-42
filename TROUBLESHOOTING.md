# 🔧 Guia de Troubleshooting

## 🧪 Teste o Sistema Primeiro

Antes de começar, execute o script de teste:

```bash
python test_sistema.py
```

Este script verifica:
- ✅ Versão do Python
- ✅ Pacotes instalados
- ✅ API Key configurada
- ✅ Arquivos necessários
- ✅ Funcionalidade do LangChain
- ✅ Disponibilidade do Streamlit

---

## ❌ Problemas Comuns e Soluções

### 1. Erro: "No module named 'streamlit'"

**Causa**: Pacotes não instalados ou ambiente virtual não ativado

**Solução**:
```bash
# Ative o ambiente virtual primeiro
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instale os pacotes
pip install -r requirements.txt

# Verifique a instalação
pip list | grep streamlit
```

---

### 2. Erro: "API key not valid"

**Causa**: API Key incorreta ou não configurada

**Soluções**:

**Opção A - Via Interface Streamlit**:
1. Execute o app: `streamlit run app.py`
2. Insira a API Key na barra lateral
3. Não precisa configurar .env

**Opção B - Via .env**:
```bash
# Crie arquivo .env na raiz do projeto
echo "GOOGLE_API_KEY=sua_chave_aqui" > .env

# Ou manualmente:
# 1. Crie arquivo .env
# 2. Adicione: GOOGLE_API_KEY=sua_chave_aqui
```

**Obter nova API Key**:
1. Acesse: https://makersuite.google.com/app/apikey
2. Login com Google
3. "Get API Key" ou "Create API Key"
4. Copie a chave completa

---

### 3. Erro: "Cannot install package versions have conflicting dependencies"

**Causa**: Conflitos entre versões de pacotes

**Solução**:
```bash
# Limpe o ambiente
pip uninstall -y langchain langchain-google-genai google-generativeai

# Instale em ordem específica
pip install google-generativeai==0.3.0
pip install langchain-google-genai==1.0.0
pip install langchain>=0.1.0
pip install streamlit>=1.28.0

# Ou force reinstalação
pip install -r requirements.txt --force-reinstall --no-cache-dir
```

---

### 4. Erro: "Address already in use" ou porta ocupada

**Causa**: Porta 8501 já está em uso

**Solução**:
```bash
# Use outra porta
streamlit run app.py --server.port 8502

# Ou mate o processo na porta 8501
# Windows:
netstat -ano | findstr :8501
taskkill /PID [PID_NUMBER] /F

# Linux/Mac:
lsof -ti:8501 | xargs kill -9
```

---

### 5. Aplicação não abre no navegador

**Causa**: Configurações do navegador ou firewall

**Solução**:
```bash
# Abra manualmente
streamlit run app.py

# Depois acesse no navegador:
http://localhost:8501

# Ou tente modo headless
streamlit run app.py --server.headless true

# Com IP específico
streamlit run app.py --server.address 0.0.0.0
```

---

### 6. Erro: "JSONDecodeError"

**Causa**: Resposta da API não está em JSON válido

**Soluções**:

**Temporária** - Tente novamente:
- API pode ter retornado erro temporário
- Clique em "Pesquisar" novamente

**Se persistir**:
```python
# Verifique se a API está respondendo
# No terminal Python:
import google.generativeai as genai
genai.configure(api_key="sua_chave")
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("teste")
print(response.text)
```

---

### 7. Pesquisa muito lenta ou timeout

**Causas possíveis**:
- Conexão lenta
- API sobrecarregada
- Muitas requisições simultâneas

**Soluções**:
```bash
# Aumente o timeout (edite app.py)
# Adicione na configuração do LLM:
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    google_api_key=api_key,
    temperature=0.3,
    request_timeout=120  # 2 minutos
)

# Ou teste com modelo mais rápido
# Troque para: gemini-pro
```

---

### 8. Dados desatualizados ou incorretos

**Causa**: API não encontrou informações recentes

**Soluções**:
1. Tente empresa mais conhecida/líquida
2. Use ticker exato (ex: PETR4 ao invés de Petrobras)
3. Verifique se mercado está aberto
4. Pesquise novamente em alguns minutos

---

### 9. Erro ao fazer deploy no Streamlit Cloud

**Problema A**: "Requirements.txt not found"
```bash
# Certifique-se de que requirements.txt está na raiz
git add requirements.txt
git commit -m "Add requirements.txt"
git push
```

**Problema B**: "Module not found" no deploy
```bash
# Verifique requirements.txt
cat requirements.txt

# Deve conter no mínimo:
streamlit>=1.28.0
langchain>=0.1.0
langchain-google-genai>=1.0.0
google-generativeai>=0.3.0
python-dotenv>=1.0.0
```

**Problema C**: "Secrets not configured"
1. No Streamlit Cloud, vá em Settings
2. Clique em Secrets
3. Adicione:
```toml
GOOGLE_API_KEY = "sua_chave_aqui"
```

---

### 10. Python version incompatível

**Erro**: "Python version X.X is not supported"

**Solução**:
```bash
# Verifique versão atual
python --version

# Precisa ser 3.8+
# Baixe versão correta:
# Windows: https://www.python.org/downloads/
# Linux: sudo apt install python3.9
# Mac: brew install python@3.9

# Crie venv com versão específica
python3.9 -m venv venv
```

---

## 🚨 Erros Críticos

### Erro: "ImportError: cannot import name 'ChatGoogleGenerativeAI'"

**Causa**: Versão incompatível do langchain-google-genai

**Solução**:
```bash
pip uninstall langchain-google-genai
pip install langchain-google-genai==1.0.0

# Se não funcionar:
pip install --upgrade langchain-google-genai
```

---

### Erro: "SSL Certificate verification failed"

**Causa**: Problema com certificados SSL

**Solução**:
```bash
# Atualize pip e certificados
python -m pip install --upgrade pip
pip install --upgrade certifi

# Se persistir (USE COM CUIDADO):
export PYTHONHTTPSVERIFY=0  # Linux/Mac
set PYTHONHTTPSVERIFY=0     # Windows
```

---

## 🔍 Debug Avançado

### Ativar modo verbose do LangChain

Edite `app.py`:
```python
import langchain
langchain.verbose = True
langchain.debug = True
```

### Ver logs detalhados do Streamlit

```bash
streamlit run app.py --logger.level=debug
```

### Testar API Key isoladamente

```python
# test_api.py
import os
from langchain_google_genai import ChatGoogleGenerativeAI

api_key = input("Cole sua API Key: ").strip()

try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        google_api_key=api_key
    )
    response = llm.invoke("Olá, você está funcionando?")
    print("✅ API Key válida!")
    print(f"Resposta: {response.content}")
except Exception as e:
    print(f"❌ Erro: {e}")
```

---

## 📊 Comandos Úteis para Diagnóstico

```bash
# Verificar ambiente Python
which python
python --version
pip --version

# Listar pacotes instalados
pip list
pip show streamlit
pip show langchain-google-genai

# Verificar processos Streamlit
ps aux | grep streamlit  # Linux/Mac
tasklist | findstr streamlit  # Windows

# Limpar cache do pip
pip cache purge

# Reinstalar tudo do zero
pip uninstall -y -r requirements.txt
pip install -r requirements.txt

# Ver espaço em disco
df -h  # Linux/Mac
dir   # Windows

# Testar conexão com internet
ping google.com
curl https://generativelanguage.googleapis.com
```

---

## 🆘 Ainda com Problemas?

### Checklist Final:

- [ ] Python 3.8+ instalado?
- [ ] Ambiente virtual ativado?
- [ ] `requirements.txt` instalado?
- [ ] API Key válida?
- [ ] Arquivos na pasta correta?
- [ ] Porta 8501 livre?
- [ ] Conexão com internet OK?
- [ ] Firewall não está bloqueando?

### Coletar Informações para Suporte:

```bash
# Execute e salve output
python test_sistema.py > diagnostico.txt 2>&1

# Informações do sistema
python --version >> diagnostico.txt
pip list >> diagnostico.txt

# Envie diagnostico.txt para análise
```

---

## 💡 Dicas de Prevenção

1. **Sempre use ambiente virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # ou venv\Scripts\activate
   ```

2. **Mantenha pacotes atualizados**
   ```bash
   pip install --upgrade pip
   pip list --outdated
   ```

3. **Faça backup do .env**
   - Nunca commite .env no Git
   - Mantenha cópia segura da API Key

4. **Use .gitignore correto**
   ```bash
   # Verifique se está ignorando:
   .env
   __pycache__/
   venv/
   ```

5. **Teste localmente antes do deploy**
   ```bash
   streamlit run app.py
   # Teste todas as funcionalidades
   # Só então faça deploy
   ```

---

## 📚 Recursos Adicionais

- [Documentação Streamlit](https://docs.streamlit.io)
- [Documentação LangChain](https://python.langchain.com)
- [Google Gemini API Docs](https://ai.google.dev/docs)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

---

## 🎯 Última Tentativa - Reset Total

Se nada funcionar, faça reset completo:

```bash
# 1. Desative e delete venv
deactivate
rm -rf venv  # Linux/Mac
rmdir /s venv  # Windows

# 2. Limpe cache Python
find . -type d -name __pycache__ -exec rm -rf {} +  # Linux/Mac
del /s /q __pycache__  # Windows

# 3. Recrie tudo
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

# 4. Teste
python test_sistema.py

# 5. Execute
streamlit run app.py
```

---

**Última atualização**: Dezembro 2024