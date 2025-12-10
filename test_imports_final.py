#!/usr/bin/env python
# test_imports_final.py

print("🔧 Testando imports do LangChain...")

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    print("✅ langchain_google_genai OK")
    
    from langchain_core.prompts import PromptTemplate
    print("✅ langchain_core.prompts OK")
    
    from langchain_community.chains import LLMChain
    print("✅ langchain_community.chains OK")
    
    import json
    print("✅ json OK")
    
    print("\n🎉 Todos os imports necessários estão funcionando!")
    print("O sistema está pronto para usar LangChain + Gemini")
    
except ImportError as e:
    print(f"\n❌ Erro de importação: {e}")
    print("\n📦 Instale as dependências:")
    print("pip install langchain-google-genai langchain-core langchain-community")
    
except Exception as e:
    print(f"\n⚠️ Outro erro: {e}")