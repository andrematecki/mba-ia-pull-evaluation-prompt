"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header, validate_prompt_structure

load_dotenv()


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    return validate_prompt_structure(prompt_data)


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt (sem username)
        prompt_data: Dados do prompt carregados do YAML

    Returns:
        True se sucesso, False caso contrário
    """
    username = os.getenv("USERNAME_LANGSMITH_HUB", "")
    full_name = f"{username}/{prompt_name}"

    system_prompt = prompt_data["system_prompt"]
    user_prompt = prompt_data.get("user_prompt", "{bug_report}")
    description = prompt_data.get("description", "")
    tags = prompt_data.get("tags", [])

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", user_prompt),
    ])

    print(f"   Publicando '{full_name}' no LangSmith Hub...")

    hub.push(
        full_name,
        prompt_template,
        new_repo_is_public=True,
        new_repo_description=description,
    )

    print(f"   ✓ Prompt publicado com sucesso: {full_name}")
    return True


def main():
    """Função principal"""
    print_section_header("PUSH DE PROMPTS OTIMIZADOS")

    required_vars = ["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]
    if not check_env_vars(required_vars):
        return 1

    yaml_path = "prompts/bug_to_user_story_v2.yml"
    print(f"Carregando prompt de {yaml_path}...")

    data = load_yaml(yaml_path)
    if not data:
        return 1

    prompt_key = "bug_to_user_story_v2"
    prompt_data = data.get(prompt_key)

    if not prompt_data:
        print(f"❌ Chave '{prompt_key}' não encontrada no YAML")
        return 1

    print(f"   ✓ Prompt carregado")

    is_valid, errors = validate_prompt(prompt_data)
    if not is_valid:
        print("\n❌ Prompt inválido:")
        for error in errors:
            print(f"   - {error}")
        return 1

    print("   ✓ Prompt validado\n")

    try:
        success = push_prompt_to_langsmith(prompt_key, prompt_data)
    except Exception as e:
        print(f"❌ Erro ao publicar prompt: {e}")
        return 1

    if success:
        username = os.getenv("USERNAME_LANGSMITH_HUB", "")
        print(f"\n✅ Concluído!")
        print(f"   Acesse: https://smith.langchain.com/hub/{username}/{prompt_key}")
        print("\nPróximo passo:")
        print("   python src/evaluate.py")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
