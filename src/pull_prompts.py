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
from langchain import hub
from langchain_core.prompts.loading import load_prompt
from langchain_core.output_parsers import StrOutputParser
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()

def pull_prompts_from_langsmith():
    """Carrega o prompt do Hub.
    Args:
        None
    Returns:
        prompt_template: Dados do prompt
    """    
    prompt_template = hub.pull("leonanluppi/bug_to_user_story_v1")
    return prompt_template

def extrair_dados_prompt(prompt_template):
    system_prompt = ""
    user_prompt = ""
    
    for message in prompt_template.messages:
        role = message.__class__.__name__
        if "System" in role:
            system_prompt = message.prompt.template
        elif "Human" in role:
            user_prompt = message.prompt.template

    return {
        "bug_to_user_story_v1": {
            "description": "Prompt para converter relatos de bugs em User Stories",
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "version": "v1",
            "tags": ["bug-analysis", "user-story", "product-management"],
        }
    }

def save_prompt(prompt_data, path):
    """Save prompt data to a YAML file"""

    save_yaml(prompt_data,path)


def main():
    """Função principal"""
    prompt_template = pull_prompts_from_langsmith()
    prompt_data = extrair_dados_prompt(prompt_template)
    save_prompt(prompt_data, "prompts/bug_to_user_story_v1.yml")
    print(prompt_data)


if __name__ == "__main__":
    sys.exit(main())
