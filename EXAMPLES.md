# 📝 Exemplos de Uso e Respostas Esperadas

## Exemplo 1: Petrobras (PETR4)

### Input:
```
Empresa: Petrobras
```

### Output Esperado:
```json
{
    "nome_oficial": "Petróleo Brasileiro S.A. - Petrobras",
    "ticker": "PETR4",
    "resumo": {
        "setor": "Petróleo, Gás e Energia",
        "descricao": "A Petrobras é uma empresa de energia integrada, atuando na exploração, produção, refino, comercialização e transporte de petróleo e gás natural. É uma das maiores empresas de energia do mundo e a maior da América Latina.",
        "principais_produtos": [
            "Petróleo cru e derivados",
            "Gás natural",
            "Energia elétrica"
        ]
    },
    "noticias": [
        {
            "titulo": "Petrobras anuncia dividendos extraordinários",
            "data": "10/12/2024",
            "fonte": "Valor Econômico",
            "link": "https://valor.globo.com/..."
        },
        {
            "titulo": "Produção da Petrobras atinge recorde no pré-sal",
            "data": "05/12/2024",
            "fonte": "InfoMoney",
            "link": "https://infomoney.com.br/..."
        },
        {
            "titulo": "Petrobras investe em energias renováveis",
            "data": "28/11/2024",
            "fonte": "Reuters Brasil",
            "link": "https://reuters.com/..."
        }
    ],
    "acao": {
        "preco_atual": "R$ 38,45",
        "variacao": "+2,35%",
        "data_referencia": "10/12/2024",
        "volume": "45,2M ações"
    },
    "analise_rapida": "Petrobras mantém forte desempenho com dividendos atrativos e recordes de produção no pré-sal. A empresa continua sendo uma das principais pagadoras de dividendos da B3, atraindo investidores em busca de renda passiva."
}
```

---

## Exemplo 2: Magazine Luiza (MGLU3)

### Input:
```
Empresa: Magazine Luiza
```

### Output Esperado:
```json
{
    "nome_oficial": "Magazine Luiza S.A.",
    "ticker": "MGLU3",
    "resumo": {
        "setor": "Varejo e E-commerce",
        "descricao": "Magazine Luiza é uma das maiores redes varejistas do Brasil, com forte presença no e-commerce. Atua na venda de produtos de eletrônicos, eletrodomésticos, móveis e artigos para casa através de lojas físicas e plataforma digital.",
        "principais_produtos": [
            "Eletrônicos e eletrodomésticos",
            "Móveis e decoração",
            "Marketplace digital"
        ]
    },
    "noticias": [
        {
            "titulo": "Magazine Luiza expande serviços financeiros",
            "data": "08/12/2024",
            "fonte": "Exame",
            "link": "https://exame.com/..."
        },
        {
            "titulo": "MGLU3 apresenta resultados do 3T24",
            "data": "01/12/2024",
            "fonte": "Money Times",
            "link": "https://moneytimes.com.br/..."
        },
        {
            "titulo": "Magalu investe em tecnologia e logística",
            "data": "25/11/2024",
            "fonte": "Estadão",
            "link": "https://estadao.com.br/..."
        }
    ],
    "acao": {
        "preco_atual": "R$ 12,85",
        "variacao": "-1,15%",
        "data_referencia": "10/12/2024",
        "volume": "28,3M ações"
    },
    "analise_rapida": "Magazine Luiza passa por processo de transformação digital e expansão dos serviços financeiros. A empresa foca em rentabilidade após período de forte crescimento, ajustando seu modelo de negócios para o cenário atual do varejo."
}
```

---

## Exemplo 3: Vale (VALE3)

### Input:
```
Empresa: Vale
```

### Output Esperado:
```json
{
    "nome_oficial": "Vale S.A.",
    "ticker": "VALE3",
    "resumo": {
        "setor": "Mineração e Metais",
        "descricao": "A Vale é uma das maiores mineradoras do mundo, líder global na produção de minério de ferro e níquel. Atua na extração, processamento e comercialização de recursos minerais essenciais para a indústria global.",
        "principais_produtos": [
            "Minério de ferro",
            "Níquel",
            "Cobre e outros minerais"
        ]
    },
    "noticias": [
        {
            "titulo": "Vale anuncia novos investimentos em descarbonização",
            "data": "09/12/2024",
            "fonte": "Valor Econômico",
            "link": "https://valor.globo.com/..."
        },
        {
            "titulo": "Produção de minério da Vale supera expectativas",
            "data": "04/12/2024",
            "fonte": "Reuters Brasil",
            "link": "https://reuters.com/..."
        },
        {
            "titulo": "Vale firma acordo para fornecimento de níquel verde",
            "data": "29/11/2024",
            "fonte": "InfoMoney",
            "link": "https://infomoney.com.br/..."
        }
    ],
    "acao": {
        "preco_atual": "R$ 58,90",
        "variacao": "+0,85%",
        "data_referencia": "10/12/2024",
        "volume": "52,1M ações"
    },
    "analise_rapida": "Vale mantém posição de destaque no mercado global de mineração com foco em sustentabilidade e descarbonização. A empresa continua investindo em projetos verdes enquanto mantém produção robusta de minério de ferro."
}
```

---

## Formato dos Dados

### Estrutura JSON Padrão:

```json
{
    "nome_oficial": "string",
    "ticker": "string",
    "resumo": {
        "setor": "string",
        "descricao": "string (2-3 linhas)",
        "principais_produtos": ["string", "string", "string"]
    },
    "noticias": [
        {
            "titulo": "string",
            "data": "string (DD/MM/YYYY)",
            "fonte": "string",
            "link": "string (URL completo)"
        }
    ],
    "acao": {
        "preco_atual": "string (R$ XX,XX)",
        "variacao": "string (+/-X,XX%)",
        "data_referencia": "string (DD/MM/YYYY)",
        "volume": "string"
    },
    "analise_rapida": "string (2-3 linhas)"
}
```

---

## Casos de Uso

### 1. Análise Preliminar para M&A
**Objetivo**: Avaliar rapidamente empresas-alvo para fusões e aquisições
**Dados úteis**: Setor, notícias recentes, performance da ação

### 2. Due Diligence Inicial
**Objetivo**: Primeira etapa de investigação antes de investimentos
**Dados úteis**: Descrição da empresa, principais produtos, análise rápida

### 3. Monitoramento de Portfólio
**Objetivo**: Acompanhar empresas em carteira
**Dados úteis**: Cotação atual, notícias, variação

### 4. Relatórios para Clientes
**Objetivo**: Gerar resumos executivos rápidos
**Dados úteis**: Todos os campos + export JSON

---

## Empresas Testadas com Sucesso

✅ **Setor Financeiro**:
- Itaú Unibanco (ITUB4)
- Bradesco (BBDC4)
- Banco do Brasil (BBAS3)
- BTG Pactual (BPAC11)

✅ **Setor de Commodities**:
- Vale (VALE3)
- Petrobras (PETR4)
- Suzano (SUZB3)

✅ **Setor de Consumo**:
- Ambev (ABEV3)
- Magazine Luiza (MGLU3)
- Via (VIIA3)

✅ **Setor Industrial**:
- Weg (WEGE3)
- Embraer (EMBR3)
- Marcopolo (POMO4)

✅ **Setor de Alimentos**:
- Minerva Foods (BEEF3)
- JBS (JBSS3)
- BRF (BRFS3)

✅ **Setor de Infraestrutura**:
- CCR (CCRO3)
- Ecorodovias (ECOR3)
- Localiza (RENT3)

---

## Dicas para Melhores Resultados

1. **Use nomes completos**: "Petróleo Brasileiro" ou "Petrobras" funciona melhor que siglas
2. **Seja específico**: Se houver várias empresas com nome similar, adicione o ticker
3. **Verifique datas**: Notícias são do período atual (últimos 30 dias)
4. **Cotações**: Sempre atualizadas em tempo real via API
5. **Links**: Preferencialmente de fontes confiáveis (Valor, InfoMoney, Reuters)

---

## Limitações Conhecidas

- ⚠️ Empresas muito pequenas podem ter dados limitados
- ⚠️ Notícias em inglês podem aparecer para empresas com ADRs
- ⚠️ Cotações são do mercado à vista (não consideram after-market)
- ⚠️ Análise é preliminar, não substitui análise fundamentalista completa

---

## Troubleshooting por Empresa

### Empresa não encontrada:
1. Verifique a grafia
2. Tente usar o ticker (ex: PETR4)
3. Confirme que é empresa de capital aberto na B3

### Dados incompletos:
1. Empresa pode ter baixa liquidez
2. Notícias podem ser escassas
3. Tente novamente em alguns minutos

### Cotação desatualizada:
1. Verifique se mercado está aberto
2. Confirme horário de negociação B3 (10h-17h)
3. Dados fora do horário são do último fechamento