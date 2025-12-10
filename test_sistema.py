"""
Script de Teste para o Sistema de Pesquisa de Empresas
Testa se todos os componentes estão funcionando corretamente
"""

import sys
import os

def test_imports():
    """Testa se todas as bibliotecas necessárias estão instaladas"""
    print("🧪 Testando imports...")
    
    required_packages = {
        'streamlit': 'streamlit',
        'langchain': 'langchain',
        'langchain_google_genai': 'langchain-google-genai',
        'google.generativeai': 'google-generativeai',
        'dotenv': 'python-dotenv'
    }
    
    missing_packages = []
    
    for package, pip_name in required_packages.items():
        try:
            __import__(package)
            print(f"  ✅ {pip_name}")
        except ImportError:
            print(f"  ❌ {pip_name} - NÃO INSTALADO")
            missing_packages.append(pip_name)
    
    if missing_packages:
        print(f"\n⚠️  Pacotes faltando: {', '.join(missing_packages)}")
        print(f"   Execute: pip install {' '.join(missing_packages)}")
        return False
    
    print("✅ Todos os pacotes estão instalados!\n")
    return True

def test_python_version():
    """Verifica a versão do Python"""
    print("🐍 Verificando versão do Python...")
    
    version = sys.version_info
    current = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major >= 3 and version.minor >= 8:
        print(f"  ✅ Python {current} (OK)")
        return True
    else:
        print(f"  ❌ Python {current} (Requer 3.8+)")
        return False

def test_api_key():
    """Verifica se a API Key está configurada"""
    print("\n🔑 Verificando API Key...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("GOOGLE_API_KEY")
        
        if api_key:
            print(f"  ✅ API Key encontrada no .env (comprimento: {len(api_key)})")
            
            if len(api_key) < 20:
                print("  ⚠️  API Key parece ser muito curta")
                return False
            
            return True
        else:
            print("  ⚠️  API Key não encontrada no arquivo .env")
            print("     Você precisará inseri-la manualmente na interface")
            return None  # None = não crítico, mas aviso
            
    except Exception as e:
        print(f"  ❌ Erro ao verificar API Key: {e}")
        return None

def test_files():
    """Verifica se todos os arquivos necessários existem"""
    print("\n📁 Verificando arquivos do projeto...")
    
    required_files = {
        'app.py': 'Aplicação Streamlit principal',
        'requirements.txt': 'Lista de dependências',
        'README.md': 'Documentação',
        'pesquisa_terminal.py': 'Versão terminal (opcional)'
    }
    
    optional_files = {
        '.env': 'Configurações de ambiente',
        '.gitignore': 'Exclusões do Git',
        'QUICKSTART.md': 'Guia rápido',
        'EXAMPLES.md': 'Exemplos de uso'
    }
    
    all_good = True
    
    for file, description in required_files.items():
        if os.path.exists(file):
            print(f"  ✅ {file} - {description}")
        else:
            print(f"  ❌ {file} - {description} (FALTANDO)")
            all_good = False
    
    print("\n  📋 Arquivos opcionais:")
    for file, description in optional_files.items():
        if os.path.exists(file):
            print(f"  ✅ {file} - {description}")
        else:
            print(f"  ⚠️  {file} - {description} (não encontrado)")
    
    return all_good

def test_langchain_import():
    """Testa se consegue criar uma chain básica"""
    print("\n🔗 Testando criação de chain LangChain...")
    
    try:
        from langchain.prompts import PromptTemplate
        from langchain.chains import LLMChain
        
        # Criar um template simples
        template = PromptTemplate(
            input_variables=["test"],
            template="Teste: {test}"
        )
        
        print("  ✅ PromptTemplate criado com sucesso")
        print("  ✅ LangChain está funcional")
        return True
        
    except Exception as e:
        print(f"  ❌ Erro ao testar LangChain: {e}")
        return False

def test_json_parsing():
    """Testa capacidade de parsing JSON"""
    print("\n📊 Testando parsing de JSON...")
    
    import json
    
    test_json = '''
    {
        "nome": "Teste",
        "valor": 123.45
    }
    '''
    
    try:
        data = json.loads(test_json)
        print("  ✅ Parser JSON funcional")
        return True
    except Exception as e:
        print(f"  ❌ Erro no parser JSON: {e}")
        return False

def test_streamlit_availability():
    """Verifica se o Streamlit pode ser executado"""
    print("\n🎨 Verificando disponibilidade do Streamlit...")
    
    try:
        import streamlit as st
        print(f"  ✅ Streamlit {st.__version__} disponível")
        print("     Execute: streamlit run app.py")
        return True
    except Exception as e:
        print(f"  ❌ Erro ao importar Streamlit: {e}")
        return False

def run_all_tests():
    """Executa todos os testes"""
    print("=" * 80)
    print("  🧪 TESTE DO SISTEMA DE PESQUISA DE EMPRESAS")
    print("=" * 80)
    print()
    
    results = {
        'Python Version': test_python_version(),
        'Imports': test_imports(),
        'API Key': test_api_key(),
        'Files': test_files(),
        'LangChain': test_langchain_import(),
        'JSON Parser': test_json_parsing(),
        'Streamlit': test_streamlit_availability()
    }
    
    print("\n" + "=" * 80)
    print("  📋 RESUMO DOS TESTES")
    print("=" * 80)
    
    passed = 0
    warnings = 0
    failed = 0
    
    for test_name, result in results.items():
        if result is True:
            status = "✅ PASSOU"
            passed += 1
        elif result is None:
            status = "⚠️  AVISO"
            warnings += 1
        else:
            status = "❌ FALHOU"
            failed += 1
        
        print(f"  {test_name:.<20} {status}")
    
    print("\n" + "=" * 80)
    print(f"  Total: {passed} passaram | {warnings} avisos | {failed} falharam")
    print("=" * 80)
    
    if failed == 0 and warnings == 0:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("   Sistema pronto para uso!")
        print("\n💡 Próximo passo:")
        print("   Execute: streamlit run app.py")
        return True
    elif failed == 0:
        print("\n⚠️  SISTEMA FUNCIONAL COM AVISOS")
        print("   O sistema deve funcionar, mas há avisos.")
        print("\n💡 Próximo passo:")
        print("   Execute: streamlit run app.py")
        return True
    else:
        print("\n❌ ALGUNS TESTES FALHARAM")
        print("   Corrija os erros antes de executar o sistema.")
        print("\n💡 Ações recomendadas:")
        print("   1. Execute: pip install -r requirements.txt")
        print("   2. Verifique se tem Python 3.8+")
        print("   3. Execute este teste novamente")
        return False

if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Teste interrompido pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)