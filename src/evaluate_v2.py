"""
Script de avaliação usando langsmith.evaluation.evaluate().

Diferença do evaluate.py original:
- Usa langsmith.evaluation.evaluate() em vez de loop manual
- Os experimentos ficam visíveis no dashboard do LangSmith
- Cada execução gera um Experiment rastreável com scores por exemplo
"""

import os
import sys
import json
from typing import List, Dict, Any
from pathlib import Path
from dotenv import load_dotenv
from langsmith import Client
from langsmith.evaluation import evaluate
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import check_env_vars, format_score, print_section_header, get_llm as get_configured_llm
from metrics import evaluate_f1_score, evaluate_clarity, evaluate_precision

load_dotenv()


def get_llm():
    return get_configured_llm(temperature=0)


def load_dataset_from_jsonl(jsonl_path: str) -> List[Dict[str, Any]]:
    examples = []
    try:
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    examples.append(json.loads(line))
        return examples
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {jsonl_path}")
        return []
    except Exception as e:
        print(f"❌ Erro ao carregar dataset: {e}")
        return []


def create_evaluation_dataset(client: Client, dataset_name: str, jsonl_path: str) -> str:
    print(f"Criando dataset de avaliação: {dataset_name}...")
    examples = load_dataset_from_jsonl(jsonl_path)

    if not examples:
        print("❌ Nenhum exemplo carregado do arquivo .jsonl")
        return dataset_name

    print(f"   ✓ Carregados {len(examples)} exemplos")

    try:
        existing = next((ds for ds in client.list_datasets(dataset_name=dataset_name) if ds.name == dataset_name), None)

        if existing:
            print(f"   ✓ Dataset '{dataset_name}' já existe, usando existente")
        else:
            dataset = client.create_dataset(dataset_name=dataset_name)
            for example in examples:
                client.create_example(
                    dataset_id=dataset.id,
                    inputs=example["inputs"],
                    outputs=example["outputs"]
                )
            print(f"   ✓ Dataset criado com {len(examples)} exemplos")
    except Exception as e:
        print(f"   ⚠️  Erro ao criar dataset: {e}")

    return dataset_name


def pull_prompt(prompt_name: str) -> ChatPromptTemplate:
    print(f"   Puxando prompt: {prompt_name}")
    try:
        prompt = hub.pull(prompt_name)
        print(f"   ✓ Prompt carregado")
        return prompt
    except Exception as e:
        print(f"❌ Erro ao carregar prompt '{prompt_name}': {e}")
        raise


def run_evaluation(prompt_name: str, dataset_name: str, client: Client) -> Dict[str, float]:
    print(f"\n🔍 Avaliando: {prompt_name}")

    prompt_template = pull_prompt(prompt_name)
    llm = get_llm()

    # Acumuladores para calcular médias ao final
    f1_scores = []
    clarity_scores = []
    precision_scores = []

    # Função target: recebe inputs do dataset, retorna a resposta do LLM
    def target(inputs: dict) -> dict:
        try:
            chain = prompt_template | llm
            response = chain.invoke(inputs)
            return {"answer": response.content}
        except Exception as e:
            print(f"      ⚠️  Erro ao executar prompt: {e}")
            return {"answer": ""}

    # Avaliador único: faz exatamente 3 chamadas LLM (f1, clarity, precision)
    # e deriva helpfulness e correctness matematicamente — igual ao evaluate.py original:
    #   helpfulness = (clarity + precision) / 2
    #   correctness = (f1    + precision) / 2
    # Retorna lista com as 5 métricas para o LangSmith registrar todas no Experiment.
    def all_metrics_evaluator(inputs: dict, outputs: dict, reference_outputs: dict) -> list:
        question = inputs.get("bug_report", inputs.get("question", inputs.get("pr_title", "")))
        answer = outputs.get("answer", "")
        reference = reference_outputs.get("reference", "")

        f1        = evaluate_f1_score(question, answer, reference)
        clarity   = evaluate_clarity(question, answer, reference)
        precision = evaluate_precision(question, answer, reference)

        f1_scores.append(f1["score"])
        clarity_scores.append(clarity["score"])
        precision_scores.append(precision["score"])

        helpfulness = round((clarity["score"] + precision["score"]) / 2, 4)
        correctness = round((f1["score"]      + precision["score"]) / 2, 4)

        return [
            {"key": "f1_score",    "score": f1["score"]},
            {"key": "clarity",     "score": clarity["score"]},
            {"key": "precision",   "score": precision["score"]},
            {"key": "helpfulness", "score": helpfulness},
            {"key": "correctness", "score": correctness},
        ]

    # Nome do experimento visível no LangSmith
    experiment_prefix = prompt_name.split("/")[-1]
    print(f"   Experimento '{experiment_prefix}' será visível em smith.langchain.com")

    # evaluate() cria o Experiment no LangSmith e loga cada run com seus scores
    evaluate(
        target,
        data=dataset_name,
        evaluators=[all_metrics_evaluator],
        experiment_prefix=experiment_prefix,
        client=client,
        max_concurrency=1,
    )

    avg_f1        = sum(f1_scores)        / len(f1_scores)        if f1_scores        else 0.0
    avg_clarity   = sum(clarity_scores)   / len(clarity_scores)   if clarity_scores   else 0.0
    avg_precision = sum(precision_scores) / len(precision_scores) if precision_scores else 0.0

    return {
        "helpfulness": round((avg_clarity + avg_precision) / 2, 4),
        "correctness": round((avg_f1      + avg_precision) / 2, 4),
        "f1_score":    round(avg_f1,        4),
        "clarity":     round(avg_clarity,   4),
        "precision":   round(avg_precision, 4),
    }


def display_results(prompt_name: str, scores: Dict[str, float]) -> bool:
    print("\n" + "=" * 50)
    print(f"Prompt: {prompt_name}")
    print("=" * 50)

    print("\nMétricas Derivadas:")
    print(f"  - Helpfulness: {format_score(scores['helpfulness'], threshold=0.9)}")
    print(f"  - Correctness: {format_score(scores['correctness'], threshold=0.9)}")

    print("\nMétricas Base:")
    print(f"  - F1-Score:  {format_score(scores['f1_score'], threshold=0.9)}")
    print(f"  - Clarity:   {format_score(scores['clarity'], threshold=0.9)}")
    print(f"  - Precision: {format_score(scores['precision'], threshold=0.9)}")

    average_score = sum(scores.values()) / len(scores)
    print("\n" + "-" * 50)
    print(f"📊 MÉDIA GERAL: {average_score:.4f}")
    print("-" * 50)

    passed = all(s >= 0.9 for s in scores.values()) and average_score >= 0.9

    if passed:
        print(f"\n✅ STATUS: APROVADO - Todas as métricas >= 0.9")
    else:
        print(f"\n❌ STATUS: REPROVADO")
        failed = [name for name, s in scores.items() if s < 0.9]
        if failed:
            print(f"⚠️  Métricas abaixo de 0.9: {', '.join(failed)}")
        print(f"⚠️  Média atual: {average_score:.4f} | Necessário: 0.9000")

    return passed


def main():
    print_section_header("AVALIAÇÃO DE PROMPTS OTIMIZADOS (com LangSmith Experiments)")

    provider = os.getenv("LLM_PROVIDER", "openai")
    print(f"Provider: {provider}")
    print(f"Modelo Principal: {os.getenv('LLM_MODEL', 'gpt-4o-mini')}")
    print(f"Modelo de Avaliação: {os.getenv('EVAL_MODEL', 'gpt-4o')}\n")

    required_vars = ["LANGSMITH_API_KEY", "LLM_PROVIDER"]
    if provider == "openai":
        required_vars.append("OPENAI_API_KEY")
    elif provider in ["google", "gemini"]:
        required_vars.append("GOOGLE_API_KEY")

    if not check_env_vars(required_vars):
        return 1

    username = os.getenv("USERNAME_LANGSMITH_HUB", "")
    if not username:
        print("❌ USERNAME_LANGSMITH_HUB não configurada no .env")
        return 1

    jsonl_path = "datasets/bug_to_user_story.jsonl"
    if not Path(jsonl_path).exists():
        print(f"❌ Arquivo de dataset não encontrado: {jsonl_path}")
        return 1

    client = Client()
    project_name = os.getenv("LANGSMITH_PROJECT", "prompt-optimization-challenge-resolved")
    dataset_name = f"{project_name}-eval"

    create_evaluation_dataset(client, dataset_name, jsonl_path)

    prompts_to_evaluate = [
        f"{username}/bug_to_user_story_v11",
    ]

    results_summary = []

    for prompt_name in prompts_to_evaluate:
        try:
            scores = run_evaluation(prompt_name, dataset_name, client)
            passed = display_results(prompt_name, scores)
            results_summary.append({"prompt": prompt_name, "scores": scores, "passed": passed})
        except Exception as e:
            print(f"\n❌ Falha ao avaliar '{prompt_name}': {e}")
            results_summary.append({
                "prompt": prompt_name,
                "scores": {k: 0.0 for k in ["helpfulness", "correctness", "f1_score", "clarity", "precision"]},
                "passed": False
            })

    print("\n" + "=" * 50)
    print("RESUMO FINAL")
    print("=" * 50 + "\n")
    print(f"Prompts avaliados: {len(results_summary)}")
    print(f"Aprovados: {sum(1 for r in results_summary if r['passed'])}")
    print(f"Reprovados: {sum(1 for r in results_summary if not r['passed'])}\n")

    all_passed = all(r["passed"] for r in results_summary)

    if all_passed:
        print("✅ Todos os prompts atingiram todas as métricas >= 0.9!")
        print(f"\n✓ Confira os Experiments no LangSmith:")
        print(f"  https://smith.langchain.com/projects/{project_name}")
        return 0
    else:
        print("⚠️  Alguns prompts não atingiram todas as métricas >= 0.9")
        print("\nPróximos passos:")
        print("1. Refatore os prompts com score baixo")
        print("2. Faça push novamente: python src/push_prompts.py")
        print("3. Execute: python src/evaluate_v2.py novamente")
        return 1


if __name__ == "__main__":
    sys.exit(main())
