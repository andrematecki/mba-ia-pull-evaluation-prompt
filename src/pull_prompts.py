"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langsmith import Client
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def extract_prompt_data(prompt_template, prompt_key: str) -> dict:
    """
    Extrai system_prompt e user_prompt de um ChatPromptTemplate.

    Args:
        prompt_template: Instância de ChatPromptTemplate
        prompt_key: Chave raiz do dicionário YAML

    Returns:
        Dicionário no formato esperado pelo projeto
    """
    system_prompt = ""
    user_prompt = "{bug_report}"

    for message in prompt_template.messages:
        role = message.__class__.__name__.lower()
        content = message.prompt.template if hasattr(message, "prompt") else str(message)

        if "system" in role:
            system_prompt = content
        elif "human" in role or "user" in role:
            user_prompt = content

    return {
        prompt_key: {
            "description": "Prompt para converter relatos de bugs em User Stories",
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "version": "v1",
            "tags": ["bug-analysis", "user-story", "product-management"],
        }
    }


def pull_prompts_from_langsmith():
    """
    Faz pull dos prompts do LangSmith Hub e salva localmente.

    Returns:
        True se sucesso, False caso contrário
    """
    source_prompt = "leonanluppi/bug_to_user_story_v1"
    prompt_key = "bug_to_user_story_v1"
    output_path = "prompts/bug_to_user_story_v1.yml"

    print(f"   Puxando prompt: {source_prompt}")

    try:
        client = Client()
        prompt_template = client.pull_prompt(source_prompt)
        print(f"   ✓ Prompt carregado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao puxar prompt '{source_prompt}': {e}")
        return False

    prompt_data = extract_prompt_data(prompt_template, prompt_key)

    print(f"   Salvando em {output_path}...")
    success = save_yaml(prompt_data, output_path)

    if success:
        print(f"   ✓ Prompt salvo em {output_path}")
    else:
        print(f"❌ Falha ao salvar {output_path}")

    return success


def main():
    """Função principal"""
    print_section_header("PULL DE PROMPTS DO LANGSMITH HUB")

    required_vars = ["LANGSMITH_API_KEY"]
    if not check_env_vars(required_vars):
        return 1

    success = pull_prompts_from_langsmith()

    if success:
        print("\n✅ Concluído!")
        print("\nPróximos passos:")
        print("   1. Analise o prompt em prompts/bug_to_user_story_v1.yml")
        print("   2. Crie sua versão otimizada em prompts/bug_to_user_story_v2.yml")
        print("   3. Faça push: python src/push_prompts.py")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
