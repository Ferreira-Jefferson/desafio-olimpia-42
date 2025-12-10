#!/bin/bash

# Script de Deploy Automatizado para Streamlit Cloud
# Uso: ./deploy.sh

set -e  # Parar em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para print colorido
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Banner
echo "========================================"
echo "  Deploy Automático - Streamlit Cloud  "
echo "========================================"
echo ""

# Verificar se Git está instalado
print_status "Verificando Git..."
if ! command -v git &> /dev/null; then
    print_error "Git não encontrado. Instale: https://git-scm.com/"
    exit 1
fi
print_success "Git instalado"

# Verificar se está em um repositório Git
if [ ! -d .git ]; then
    print_warning "Não é um repositório Git. Inicializando..."
    git init
    print_success "Repositório Git criado"
fi

# Verificar arquivos essenciais
print_status "Verificando arquivos essenciais..."

required_files=("app.py" "requirements.txt" "README.md")
missing_files=()

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -ne 0 ]; then
    print_error "Arquivos faltando: ${missing_files[*]}"
    exit 1
fi
print_success "Todos os arquivos essenciais presentes"

# Verificar .gitignore
print_status "Verificando .gitignore..."
if [ ! -f .gitignore ]; then
    print_warning ".gitignore não encontrado. Criando..."
    cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Environment variables
.env
.env.local

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Streamlit
.streamlit/secrets.toml

# Logs
*.log

# Data
data/*.json
!data/.gitkeep
EOF
    print_success ".gitignore criado"
else
    print_success ".gitignore encontrado"
fi

# Verificar se .env está sendo ignorado
if [ -f .env ]; then
    if git check-ignore .env > /dev/null 2>&1; then
        print_success ".env está sendo ignorado (seguro)"
    else
        print_error ".env NÃO está sendo ignorado! PERIGO DE EXPOR API KEY!"
        echo "Adicione '.env' ao .gitignore antes de continuar"
        exit 1
    fi
fi

# Adicionar todos os arquivos
print_status "Preparando arquivos para commit..."
git add .

# Verificar se há mudanças
if git diff --staged --quiet; then
    print_warning "Nenhuma mudança detectada para commit"
else
    # Fazer commit
    print_status "Fazendo commit das mudanças..."
    echo "Digite a mensagem do commit (ou pressione Enter para usar padrão):"
    read -r commit_message
    
    if [ -z "$commit_message" ]; then
        commit_message="Deploy: Update application"
    fi
    
    git commit -m "$commit_message"
    print_success "Commit realizado: $commit_message"
fi

# Verificar branch
current_branch=$(git branch --show-current)
if [ "$current_branch" != "main" ] && [ "$current_branch" != "master" ]; then
    print_warning "Branch atual: $current_branch"
    print_status "Streamlit Cloud geralmente usa 'main' ou 'master'"
    echo "Deseja criar/mudar para branch 'main'? (s/n)"
    read -r response
    
    if [ "$response" = "s" ] || [ "$response" = "S" ]; then
        git checkout -b main 2>/dev/null || git checkout main
        print_success "Mudado para branch main"
    fi
fi

# Verificar remote
print_status "Verificando remote do GitHub..."
if ! git remote | grep -q "origin"; then
    print_warning "Remote 'origin' não configurado"
    echo "Digite a URL do seu repositório GitHub:"
    echo "Exemplo: https://github.com/seu-usuario/seu-repo.git"
    read -r repo_url
    
    git remote add origin "$repo_url"
    print_success "Remote adicionado: $repo_url"
else
    origin_url=$(git remote get-url origin)
    print_success "Remote configurado: $origin_url"
fi

# Push para GitHub
print_status "Fazendo push para GitHub..."
current_branch=$(git branch --show-current)

echo "Fazer push para GitHub? (s/n)"
read -r response

if [ "$response" = "s" ] || [ "$response" = "S" ]; then
    if git push -u origin "$current_branch"; then
        print_success "Push realizado com sucesso!"
    else
        print_error "Erro no push. Verifique suas credenciais."
        exit 1
    fi
else
    print_warning "Push cancelado pelo usuário"
fi

# Instruções finais
echo ""
echo "========================================"
echo "  ✅ PREPARAÇÃO COMPLETA!"
echo "========================================"
echo ""
print_success "Código está no GitHub!"
echo ""
echo "📝 PRÓXIMOS PASSOS PARA DEPLOY:"
echo ""
echo "1. Acesse: https://share.streamlit.io"
echo "2. Faça login com sua conta GitHub"
echo "3. Clique em 'New app'"
echo "4. Selecione:"
echo "   - Repository: $(git remote get-url origin | sed 's/.*github.com[:/]\(.*\).git/\1/')"
echo "   - Branch: $current_branch"
echo "   - Main file: app.py"
echo "5. Clique em 'Deploy'"
echo ""
echo "6. Configure Secrets (IMPORTANTE!):"
echo "   - Vá em Settings → Secrets"
echo "   - Adicione:"
echo "     GOOGLE_API_KEY = \"sua_chave_aqui\""
echo ""
echo "⏱️  Deploy demora ~5 minutos"
echo ""
echo "🌐 Sua app ficará disponível em:"
echo "   https://[nome-do-app].streamlit.app"
echo ""
echo "========================================"

# Oferecer para abrir browser
echo ""
echo "Deseja abrir o Streamlit Cloud no navegador? (s/n)"
read -r response

if [ "$response" = "s" ] || [ "$response" = "S" ]; then
    if command -v open &> /dev/null; then
        open "https://share.streamlit.io"  # macOS
    elif command -v xdg-open &> /dev/null; then
        xdg-open "https://share.streamlit.io"  # Linux
    elif command -v start &> /dev/null; then
        start "https://share.streamlit.io"  # Windows (Git Bash)
    else
        print_warning "Não foi possível abrir o navegador automaticamente"
        echo "Acesse manualmente: https://share.streamlit.io"
    fi
fi

print_success "Deploy preparado com sucesso!"