# 🌐 Gemini API - Pesquisa Web em Tempo Real

## Como Funciona

O Google Gemini possui capacidade integrada de pesquisar informações atualizadas na web. Quando você faz uma pergunta que requer dados recentes, o modelo automaticamente:

1. 🔍 **Identifica** que precisa de informações atuais
2. 🌐 **Pesquisa** na web em tempo real
3. 📊 **Processa** os resultados encontrados
4. 💬 **Retorna** resposta consolidada com fontes

## ✅ O Que o Sistema Faz Automaticamente

### 1. Detecção Inteligente de Necessidade

O Gemini detecta quando sua pergunta requer dados atuais:

```python
# Perguntas que acionam busca automática:
"Qual o preço atual da ação da Petrobras?"  # ✅ Busca cotação
"Notícias recentes sobre Vale"              # ✅ Busca notícias
"Quem é o CEO atual da Magazine Luiza?"    # ✅ Busca informação atual
```

### 2. Busca Contextualizada

O modelo pesquisa especificamente pelo que precisa:

- **Cotações**: Busca em tempo real na B3
- **Notícias**: Procura últimas 30 dias
- **Informações corporativas**: Sites oficiais, relatórios
- **Dados setoriais**: Fontes especializadas

### 3. Validação de Fontes

O Gemini prioriza:
- ✅ Sites oficiais de empresas
- ✅ Bolsa de valores (B3)
- ✅ Veículos de notícias confiáveis
- ✅ Relatórios financeiros publicados

## 🔧 Configuração no Código

### No nosso sistema (já configurado):

```python
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",  # Modelo com busca integrada
    google_api_key=api_key,
    temperature=0.3  # Baixa variação = mais preciso
)
```

### Prompt Otimizado para Busca:

```python
prompt = """
Você DEVE usar a ferramenta de pesquisa web para obter informações em tempo real.

IMPORTANTE: 
- Use APENAS informações atualizadas de 2024-2025
- Pesquise notícias RECENTES (últimos 30 dias)
- Obtenha o preço ATUAL da ação
"""
```

## 📊 Tipos de Pesquisa Realizadas

### 1. Cotações de Ações

**Query interna do Gemini**:
```
"PETR4 cotação B3 preço atual tempo real"
```

**Fontes consultadas**:
- B3 (Bolsa de Valores)
- InfoMoney
- Valor Econômico
- TradingView

**Dados retornados**:
- Preço atual em R$
- Variação percentual do dia
- Volume negociado
- Horário da cotação

---

### 2. Notícias Recentes

**Query interna do Gemini**:
```
"Magazine Luiza notícias últimos 30 dias 2024"
```

**Fontes consultadas**:
- Valor Econômico
- InfoMoney
- Exame
- Reuters Brasil
- Estadão Economia

**Dados retornados**:
- Título da notícia
- Data de publicação
- Fonte original
- Link completo

---

### 3. Informações Corporativas

**Query interna do Gemini**:
```
"Vale S.A. setor atuação principais produtos 2024"
```

**Fontes consultadas**:
- Site oficial da empresa
- Relatórios anuais
- Apresentações institucionais
- Wikipedia (para confirmar)

**Dados retornados**:
- Descrição oficial
- Setor de atuação
- Produtos principais
- História resumida

---

### 4. Análises e Perspectivas

**Query interna do Gemini**:
```
"Ambev análise mercado perspectivas 2024 analistas"
```

**Fontes consultadas**:
- Relatórios de casas de análise
- Notícias de mercado
- Consensos de analistas
- Apresentações de resultados

**Dados retornados**:
- Situação atual do mercado
- Perspectivas futuras
- Opinião consolidada
- Riscos e oportunidades

## 🎯 Vantagens da Busca Integrada

### ✅ Vantagens

1. **Automática**: Não precisa chamar API separada
2. **Contextual**: Busca exatamente o que precisa
3. **Validada**: Gemini filtra informações
4. **Atualizada**: Sempre dados mais recentes
5. **Consolidada**: Une múltiplas fontes

### ⚠️ Limitações

1. **Velocidade**: Pode demorar 5-15 segundos
2. **Custos**: Conta nas requisições da API
3. **Disponibilidade**: Depende de fontes online
4. **Idioma**: Pode misturar PT e EN

## 🔍 Como Verificar se Está Funcionando

### Sinais de Busca Ativa:

1. **Tempo de resposta**: 5-15s (mais que consulta normal)
2. **Citações**: Resposta menciona fontes específicas
3. **Atualidade**: Dados são de 2024-2025
4. **Detalhamento**: Informações específicas e precisas

### Teste Manual:

```python
# teste_busca.py
from langchain_google_genai import ChatGoogleGenerativeAI
import os

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Teste com pergunta que REQUER busca
response = llm.invoke("""
Qual foi o preço de fechamento da ação PETR4 ontem?
IMPORTANTE: Use busca web para obter a cotação real e atual.
""")

print(response.content)

# Se retornar preço específico e data = busca funcionou ✅
# Se retornar resposta genérica = busca não ativou ❌
```

## 🎓 Boas Práticas

### ✅ Faça:

```python
# Seja específico sobre necessidade de busca
"Pesquise na web o preço ATUAL da ação"

# Mencione timeframe
"Notícias dos últimos 30 dias"

# Peça fontes
"Forneça o link das notícias encontradas"

# Especifique formato
"Retorne em JSON com os campos: preco, data, fonte"
```

### ❌ Evite:

```python
# Genérico demais
"Me fale sobre Petrobras"  # Pode não buscar

# Sem contexto temporal
"Notícias da empresa"  # Pode retornar antigas

# Ambíguo
"Como está a ação?"  # Não específico
```

## 💡 Dicas de Otimização

### 1. Prompt Eficiente

```python
# Ruim ❌
"Pesquise sobre {empresa}"

# Bom ✅
"""
Pesquise informações ATUALIZADAS sobre {empresa}:
1. Cotação da ação (preço atual, variação)
2. 3 notícias mais recentes (com links)
3. Dados da empresa (setor, produtos)

Use pesquisa web para dados de 2024-2025.
"""
```

### 2. Validação de Resultados

```python
# Sempre valide se a busca foi bem-sucedida
if "R$" in resultado and "20" in resultado:  # Tem preço e ano
    # Busca funcionou ✅
else:
    # Tente novamente ou ajuste prompt
```

### 3. Tratamento de Erros

```python
try:
    resultado = chain.run(empresa=empresa)
    # Valide resultado
    if not validar_resultado(resultado):
        # Tente com prompt diferente
        resultado = chain.run(empresa=f"{empresa} ticker B3")
except Exception as e:
    # Log erro e informe usuário
    print(f"Erro na busca: {e}")
```

## 📈 Exemplos de Uso Real

### Exemplo 1: Cotação Precisa

```python
Pergunta: "Preço atual da PETR4"

Busca do Gemini:
- "PETR4 cotação tempo real B3"
- "Petrobras ação preço hoje"

Resposta:
"A ação PETR4 está cotada a R$ 38,45 (+2,35%) 
em 10/12/2024 às 15:45. Fonte: InfoMoney"
```

### Exemplo 2: Notícias Recentes

```python
Pergunta: "Últimas notícias Vale"

Busca do Gemini:
- "Vale SA notícias dezembro 2024"
- "Vale VALE3 últimas notícias"

Resposta:
"1. Vale anuncia investimentos em descarbonização
    - Data: 09/12/2024
    - Fonte: Valor Econômico
    - Link: https://..."
```

## 🔐 Considerações de Segurança

### Dados Públicos Apenas

O sistema busca apenas dados publicamente disponíveis:
- ✅ Cotações públicas
- ✅ Notícias publicadas
- ✅ Informações corporativas oficiais
- ❌ Dados privados ou internos

### Rate Limits

Google Gemini tem limites de uso:
- **Free tier**: ~60 requisições/minuto
- **Paid tier**: Mais requisições

Configure timeouts adequados:
```python
llm = ChatGoogleGenerativeAI(
    ...,
    request_timeout=60  # 60 segundos
)
```

## 🎯 Casos de Uso Ideais

### ✅ Perfeito Para:

1. Cotações de ações em tempo real
2. Notícias recentes (últimos 30 dias)
3. Informações corporativas atualizadas
4. Análises de mercado recentes
5. Eventos corporativos (earnings, dividendos)

### ⚠️ Não Ideal Para:

1. Dados históricos muito antigos
2. Análises técnicas complexas
3. Previsões futuras detalhadas
4. Dados não-públicos
5. Informações em tempo real (<1 minuto)

## 📚 Recursos

- [Gemini API - Web Search](https://ai.google.dev/gemini-api/docs/grounding)
- [LangChain + Gemini](https://python.langchain.com/docs/integrations/chat/google_generative_ai)
- [B3 - Cotações](http://www.b3.com.br)

---

**Nota**: O Gemini 2.0 Flash Exp tem busca web integrada e otimizada. Versões anteriores podem ter funcionalidades diferentes.