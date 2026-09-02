"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

PROMPT_PATH = str(Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml")
PROMPT_KEY = "bug_to_user_story_v2"

class TestPrompts:
    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        prompt = load_prompts(PROMPT_PATH)[PROMPT_KEY]
        assert prompt.get("system_prompt", "").strip() != ""

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        system_prompt = load_prompts(PROMPT_PATH)[PROMPT_KEY]["system_prompt"].lower()
        role_definition_phrases = [
            "você é",
            "voce é",
            "você atua como",
            "atue como",
            "atuando como",
            "seu papel é",
            "sua função é",
            "assuma o papel de",
            "you are a",
            "you are an",
            "act as",
            "your role is",
        ]
        assert any(phrase in system_prompt for phrase in role_definition_phrases), (
            "O system_prompt não contém nenhuma expressão que indique a definição de uma persona."
        )

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        system_prompt = load_prompts(PROMPT_PATH)[PROMPT_KEY]["system_prompt"].lower()
        assert "markdown" in system_prompt or "user story" in system_prompt

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        system_prompt = load_prompts(PROMPT_PATH)[PROMPT_KEY]["system_prompt"].lower()
        assert system_prompt.count("exemplo") >= 2

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        prompt = load_prompts(PROMPT_PATH)[PROMPT_KEY]
        is_valid, errors = validate_prompt_structure(prompt)
        assert not any("TODO" in err for err in errors)
        assert "TODO" not in prompt.get("user_prompt", "")

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        prompt = load_prompts(PROMPT_PATH)[PROMPT_KEY]
        is_valid, errors = validate_prompt_structure(prompt)
        assert not any("técnicas" in err for err in errors)

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
