# 🚀 Guia Rápido de Instalação

## ⚡ Setup em 5 Minutos

### 1️⃣ Instalar Python
```bash
# Verifique se tem Python 3.8+
python --version

# Se não tiver, baixe em: https://www.python.org/downloads/
```

### 2️⃣ Clonar/Baixar o Projeto
```bash
# Opção 1: Com Git
git clone <url-do-repositorio>
cd desafio-olimpia-42

# Opção 2: Download manual
# Baixe o ZIP e extraia
```

### 3️⃣ Instalar Dependências
```bash
# Criar ambiente virtual (recomendado)
python3 -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 4️⃣ Obter API Key
1. Acesse: https://makersuite.google.com/app/apikey
2. Login com Google
3. Clique em "Get API Key"
4. Copie a chave

### 5️⃣ Executar

**Interface Gráfica (Streamlit):**
```bash
streamlit run app.py
```

**Terminal:**
```bash
python pesquisa_terminal.py
```

---

## 🌐 Deploy na Web (3 Minutos)

### Streamlit Cloud (Mais Fácil)

1. **Envie para GitHub:**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/SEU-USUARIO/SEU-REPO.git
git push -u origin main
```

2. **Deploy:**
   - Acesse: https://share.streamlit.io
   - Login com GitHub
   - New app → Selecione seu repositório
   - Deploy!

3. **Configure API Key:**
   - Settings → Secrets
   - Adicione:
   ```toml
   GOOGLE_API_KEY = "sua_chave_aqui"
   ```

**Pronto!** Sua app estará em: `https://seu-app.streamlit.app`

---

## 🐛 Problemas Comuns

### Erro: "No module named 'streamlit'"
```bash
pip install -r requirements.txt
```

### Erro: "API Key inválida"
- Verifique se copiou corretamente
- Confirme que API está ativa no Google AI Studio

### App não abre no navegador
```bash
# Tente outra porta
streamlit run app.py --server.port 8502
```

### Erro ao instalar dependências
```bash
# Atualize pip primeiro
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📞 Comandos Úteis

```bash
# Ver versão do Python
python --version

# Ver pacotes instalados
pip list

# Atualizar pacote específico
pip install --upgrade nome-do-pacote

# Desativar ambiente virtual
deactivate

# Limpar cache do pip
pip cache purge
```

---

## 📊 Testar o Sistema

**Empresas para teste:**
- Petrobras
- Vale
- Itaú
- Ambev
- Magazine Luiza

---

## ✅ Checklist de Instalação

- [ ] Python 3.8+ instalado
- [ ] Dependências instaladas
- [ ] API Key obtida
- [ ] App rodando localmente
- [ ] (Opcional) Deploy na web realizado

---

## 💡 Dicas

1. **Ambiente Virtual**: Sempre use para evitar conflitos
2. **API Key**: Nunca compartilhe publicamente
3. **Git**: Adicione `.env` ao `.gitignore`
4. **Erros**: Leia a mensagem completa de erro
5. **Documentação**: Consulte README.md para detalhes

---

## 🎯 Próximos Passos

1. ✅ Instale e teste localmente
2. ✅ Faça deploy na web
3. ✅ Teste com diferentes empresas
4. ✅ Personalize conforme necessário

**Tempo total: ~10 minutos** ⏱️