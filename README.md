# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

> Desafio do MBA em Engenharia de IA — Prompt Engineering.
> Este README documenta o processo de otimização do prompt `bug_to_user_story`, da versão ruim (v1) até a versão otimizada e aprovada (v2).

## Índice

- [Objetivo](#objetivo)
- [Técnicas Aplicadas (Fase 2)](#técnicas-aplicadas-fase-2)
- [Resultados Finais](#resultados-finais)
- [Como Executar](#como-executar)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Testes](#testes)
- [Evidências no LangSmith](#evidências-no-langsmith)

---

## Objetivo

Este desafio consiste em pegar um prompt de baixa qualidade (`bug_to_user_story` v1) versionado no LangSmith e otimizá-lo aplicando técnicas de Prompt Engineering.

O processo parte do pull da versão ruim, passa pela refatoração aplicando técnicas de prompt como Role Prompt, Chain of Thought e Few-shot Learning, e termina com o push da versão otimizada (v2) de volta ao LangSmith.

Cada versão é avaliada automaticamente por métricas customizadas — Helpfulness, Correctness, F1-Score, Clarity e Precision — calculadas sobre um dataset de 15 exemplos de bugs.

A meta é que todas as métricas atinjam nota >= 0.8, comprovando que as técnicas aplicadas melhoraram a qualidade das respostas geradas.

O resultado final documenta essa evolução (v1 → v2) com dados comparativos, testes automatizados e evidências de execução no LangSmith.

## Técnicas Aplicadas (Fase 2)

### Técnica adicional Role Prompt: 

- **Por quê:** Dar contexto e autoridade ao modelo, fazendo-o responder com o vocabulário e os critérios de um profissional da área.
- **Como foi aplicada:** 
Trocando a frase inicial do prompt por 
```
`Você é um Product Manager experiente e especialista em transformar relatos de bugs em user stories detalhadas`
```
E trocando o user_prompt por: 
```
Converta o relato abaixo em uma User Story completa:

{bug_report}
```
### Chain of Thought:

- **Por quê:** Reduzir erros e omissões, incentivando o modelo a raciocinar sobre os detalhes do bug antes de escrever a user story final.
- **Como foi aplicada:** Incluindo a instrução no system prompt
``` 
`Pense passo a passo em cada detalhe da user story que julgar necessário para gerar uma user story completa e detalhada.`
``` 
### Few-shot Learning (obrigatório)

- **Por quê:** Padronizar a estrutura da saída (user story, critérios de aceitação, contexto do bug), mostrando ao modelo o formato esperado.
- **Como foi aplicada:** Inserindo dois exemplos completos de relato de bug → user story gerada no system prompt.
```
- Exemplo 1:

      Relato de Bug:
        Carrinho permite finalizar compra mesmo com produto fora de estoque.

        Fluxo do bug:
        1. Produto tem 2 unidades em estoque
        2. Cliente A adiciona 2 unidades ao carrinho
        3. Estoque fica zerado
        4. Cliente B ainda consegue adicionar ao carrinho
        5. Cliente B finaliza compra
        6. Sistema gera pedido mas não tem estoque para enviar    

      User stories gerada:    
        Como o sistema de e-commerce, eu quero validar disponibilidade de estoque 
        antes de permitir finalização de compra, para que não sejam criados pedidos que não podem ser atendidos.

        Critérios de Aceitação:
        - Dado que um produto está no carrinho
        - Quando o cliente tenta finalizar a compra
        - Então o sistema deve validar estoque disponível em tempo real
        - E se o produto estiver fora de estoque, deve bloquear a compra
        - E deve exibir mensagem clara sobre a indisponibilidade
        - E deve sugerir remover o item ou aguardar reposição

        Critérios de Prevenção:
        - Quando produto ficar sem estoque
        - E houver itens em carrinhos de outros clientes
        - Então deve exibir aviso "estoque limitado" ao adicionar
        - E deve reservar estoque temporariamente (15 minutos) ao ir para checkout

        Contexto do Bug:
        - Problema: validação de estoque não é feita no checkout
        - Impacto: pedidos criados sem possibilidade de atendimento
        - Cenário crítico: múltiplos clientes comprando último item
    
    --------------------------------

    - Exemplo 2:
    
      Relato de Bug:
        Modal de confirmação de exclusão aparece atrás do menu lateral em telas pequenas (< 768px).

        Detalhes:
        - z-index do modal: 1000
        - z-index do menu lateral: 1050
        - Usuários não conseguem clicar nos botões do modal
        - Precisam fechar o menu lateral antes

      User stories gerada:
        Como um usuário em dispositivo móvel, eu quero que modais importantes apareçam acima de todos os outros elementos, para que eu possa interagir com eles sem precisar fechar outros componentes.

        Critérios de Aceitação:
        - Dado que estou em uma tela com largura menor que 768px
        - Quando aciono uma ação que abre um modal de confirmação
        - Então o modal deve aparecer acima de todos os elementos da página
        - E o menu lateral deve ficar desfocado (backdrop)
        - E todos os botões do modal devem ser clicáveis
        - E o modal deve ocupar pelo menos 90% da largura da tela

        Critérios de Acessibilidade:
        - O foco do teclado deve ir para o modal
        - Deve ser possível fechar com ESC
        - O backdrop deve fechar ao clicar fora

        Contexto Técnico:
        - Bug atual: z-index modal (1000) < z-index menu (1050)
        - Solução: ajustar z-index do modal para > 1050
        - Devices afetados: mobile e tablets (< 768px)

        --------------------------------  
  ```

## Resultados Finais

### Link do dashboard LangSmith

- **Prompt:** https://smith.langchain.com/hub/pauloholiveira/bug_to_user_story_v2
- **Traces:** https://smith.langchain.com/o/974a5734-4fb0-41ea-aef0-d063090ac60d/projects/p/bbc1c2d1-f9f1-4210-b2c3-e6320c71378e?timeModel=%7B%22duration%22%3A%221d%22%7D&runview=traces

### Comparativo v1 vs v2

| Métrica      | v1 (ruim) | v2 (RulePrompt) |  v2 (+CoT)  |   v2 (+FewShot)   | Meta  |
|--------------|-----------|-----------------|-----------------|---------------|-------|
| Helpfulness  |   0.80    |      0.82       |       0.81      |     0.83      | >=0.8 |
| Correctness  |   0.80    |      0.82       |       0.83      |     0.87      | >=0.8 |
| F1-Score     |   0.79    |      0.81       |       0.85      |     0.88      | >=0.8 |
| Clarity      |   0.78    |      0.81       |       0.80      |     0.82      | >=0.8 |
| Precision    |   0.82    |      0.83       |       0.81      |     0.85      | >=0.8 |
| **Média**    |  0.7996   |     0.8144      |      0.8207     |    0.8501     | >=0.8 |

### Screenshots das avaliações

#### Iteração 1 - v1 (ruim)

![Resultado Console - v1](docs/images/1_Resultado_Console_PromptRuim_v1.png)

#### Iteração 2 - v2 (Role Prompt)

![Resultado Console - Role Prompt](docs/images/2_Resultado_Console_Prompt_RulePrompt_v2.png)

#### Iteração 3 - v2 (+CoT)

![Resultado Console - CoT](docs/images/3_Resultado_Console_RulePrompt_CoT_v2.png)

#### Iteração 4 - v2 (+FewShot)

![Resultado Console - FewShot](docs/images/4_Resultado_Console_RulePrompt_CoT_FewShot_v2.png)

### Histórico de iterações

| Iteração | Mudança no prompt |                       Resultado                       |
|----------|-------------------|-------------------------------------------------------|
| 1        |      Nenhuma      | **Reprovado** -  F1-Score: 0.77 - Clarity: 0.78 - Media 0.7996 |
| 2        |    Role Prompt    | **Aprovado**  -  F1-Score: 0.81 - Clarity: 0.81 - Media 0.8144 |
| 3        |       +CoT        | **Aprovado**  -  F1-Score: 0.85 - Clarity: 0.80 - Media 0.8207 |
| 3        |     +FewShot      | **Aprovado**  -  F1-Score: 0.88 - Clarity: 0.82 - Media 0.8501 |

## Como Executar

### Pré-requisitos

- Python 3.9+
- Conta e API Key no [LangSmith](https://smith.langchain.com/)
- API Key da [OpenAI](https://platform.openai.com/api-keys) e/ou [Google Gemini](https://aistudio.google.com/app/apikey)

### 1. Instalar dependências

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente

Copie `.env.example` para `.env` e preencha as credenciais:

```bash
cp .env.example .env
```

```env
# LangSmith Configuration
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_PROJECT=Desafio_Prompt_Engineering
USERNAME_LANGSMITH_HUB=pauloholiveira
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
EVAL_MODEL=gpt-4o-mini
```

### 3. Pull do prompt inicial (v1)

```bash
python src/pull_prompts.py
```

### 4. Push do prompt otimizado (v2)

```bash
python src/push_prompts.py
```

### 5. Executar avaliação

```bash
python src/evaluate.py
```

### 6. Rodar os testes de validação

```bash
pytest tests/test_prompts.py
```

## Estrutura do Projeto

```
mba-ia-pull-evaluation-prompt/
├── .env.example
├── requirements.txt
├── README.md
│
├── prompts/
│   ├── bug_to_user_story_v1.yml   # Prompt original (baixa qualidade)
│   └── bug_to_user_story_v2.yml   # Prompt otimizado
│
├── datasets/
│   └── bug_to_user_story.jsonl    # 15 exemplos de bugs para avaliação
│
├── src/
│   ├── pull_prompts.py            # Pull do LangSmith
│   ├── push_prompts.py            # Push ao LangSmith
│   ├── evaluate.py                # Avaliação automática (métricas)
│   ├── metrics.py                 # Helpfulness, Correctness, F1, Clarity, Precision
│   └── utils.py                   # Funções auxiliares
│
└── tests/
    └── test_prompts.py            # Testes de validação do prompt v2
```

## Testes

**Testes Implementados**

- `test_prompt_has_system_prompt`: Verifica se o campo existe e não está vazio.
- `test_prompt_has_role_definition`: Verifica se o prompt define uma persona, pesquisando por várias possibilidades de definição de persona. Por exemplo:
  - "você é"
  - "voce é"
  - "você atua como"
  - "atue como"
  - "atuando como"
  - "seu papel é"
  - "sua função é"
  - "assuma o papel de"
  - "you are a"
  - "you are an"
  - "act as"
  - "your role is"
- `test_prompt_mentions_format`: Verifica se o prompt exige formato Markdown ou User Story padrão.
- `test_prompt_has_few_shot_examples`: Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot).
- `test_prompt_no_todos`: Garante que você não esqueceu nenhum `[TODO]` no texto.
- `test_minimum_techniques`: Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas.

![Execução dos Testes - Versão Final](docs/images/Execucao_Testes_Versao_Final.png)

## Evidências no LangSmith

#### Iteração 1 - v1 (ruim)

![Trace LangSmith - v1](docs/images/1_TraceLangSmith_PromptRuim_v1.png)

#### Iteração 2 - v2 (Role Prompt)

![Trace LangSmith - Role Prompt](docs/images/2_TraceLangSmith_RulePrompt_v2.png)

#### Iteração 3 - v2 (+CoT)

![Trace LangSmith - CoT](docs/images/3_TraceLangSmith_CoT_v2.png)

#### Iteração 4 - v2 (+FewShot)

![Trace LangSmith - FewShot](docs/images/4_TraceLangSmith_RulePrompt_CoT_FewShot_v2.png)
