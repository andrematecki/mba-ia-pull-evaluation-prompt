"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

PROMPT_FILE = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"
PROMPT_KEY = "bug_to_user_story_v2"


def load_prompt() -> dict:
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data[PROMPT_KEY]


class TestPrompts:
    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        prompt = load_prompt()
        assert "system_prompt" in prompt, "Campo 'system_prompt' não encontrado"
        assert prompt["system_prompt"].strip(), "Campo 'system_prompt' está vazio"

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: 'Você é um Product Manager')."""
        prompt = load_prompt()
        system = prompt.get("system_prompt", "")
        assert "Você é" in system, "Prompt não define uma persona com 'Você é'"

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        prompt = load_prompt()
        system = prompt.get("system_prompt", "")
        keywords = ["User Story", "Critérios de Aceitação", "Como um", "Dado que"]
        assert any(kw in system for kw in keywords), (
            "Prompt não menciona o formato esperado de User Story"
        )

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        prompt = load_prompt()
        system = prompt.get("system_prompt", "")
        assert "EXEMPLO" in system.upper(), "Prompt não contém exemplos few-shot"
        assert "Bug Report:" in system, "Exemplos few-shot não contêm 'Bug Report:'"

    def test_prompt_no_todos(self):
        """Garante que não há nenhum [TODO] esquecido no texto."""
        prompt = load_prompt()
        system = prompt.get("system_prompt", "")
        user = prompt.get("user_prompt", "")
        assert "[TODO]" not in system, "system_prompt contém [TODO] não resolvido"
        assert "[TODO]" not in user, "user_prompt contém [TODO] não resolvido"

    def test_minimum_techniques(self):
        """Verifica (via metadados do YAML) se pelo menos 2 técnicas foram listadas."""
        prompt = load_prompt()
        techniques = prompt.get("techniques_applied", [])
        assert len(techniques) >= 2, (
            f"Mínimo de 2 técnicas requerido, encontradas: {len(techniques)}"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
