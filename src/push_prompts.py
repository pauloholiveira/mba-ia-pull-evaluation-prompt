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
from langsmith import Client

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """    
    try:
        # 1. Montar o ChatPromptTemplate a partir do YAML
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", prompt_data["system_prompt"]),
            ("human", prompt_data["user_prompt"]),
        ])

        
        client = Client()
        
        # 3. Push público com metadados
        url = client.push_prompt(
            prompt_identifier=prompt_name,          # ex: "seu_username/bug_to_user_story_v2"
            object=prompt_template,
            is_public=True,                         # ← torna o prompt PÚBLICO
            description=prompt_data.get("description", ""),
            tags=prompt_data.get("tags", []),       # ← tags do prompt
        )

        return True

    except Exception as e:
        print(f"Erro ao publicar prompt: {e}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    is_valid, errors = validate_prompt_structure(prompt_data)

    user_prompt = prompt_data.get("user_prompt", "").strip()
    if not user_prompt:
        errors.append("user_prompt está vazio")
    if "TODO" in user_prompt:
        errors.append("user_prompt ainda contém TODOs")
    tags = prompt_data.get("tags", [])
    if not tags:
        errors.append("tags está vazio — adicione pelo menos uma tag")
    return (len(errors) == 0, errors)
    


def main():
    """Função principal"""
    prompt_key = "bug_to_user_story_v2"
    
    data = load_yaml("prompts/bug_to_user_story_v2.yml")
    prompt_data = data[prompt_key]
    is_valid, errors = validate_prompt(prompt_data)
    if not is_valid:
        print("Prompt inválido:")
        for err in errors:
            print(f"   - {err}")
        return 1

    username = os.getenv("USERNAME_LANGSMITH_HUB")
    prompt_name = f"{username}/{prompt_key}"
    success = push_prompt_to_langsmith(prompt_name, prompt_data)
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
