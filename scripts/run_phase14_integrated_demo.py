"""Phase 14: deterministic, CPU-only evidence-first CLI demo."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.integrated.pipeline import IntegratedKnowledgeEngine
from knowledge_engine.integrated.verification import extract_source_answer
from knowledgebench.documents.v2_schema import KnowledgeBenchV2Document

DOCUMENTS = Path("data/processed/knowledgebench_v2_hard_documents_v0.json")


def build_engine(path: Path = DOCUMENTS) -> IntegratedKnowledgeEngine:
    documents = [
        KnowledgeBenchV2Document.model_validate(row)
        for row in json.loads(path.read_text(encoding="utf-8"))
    ]
    return IntegratedKnowledgeEngine(documents)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evidence-first retrieval demo (no model answer generation)"
    )
    parser.add_argument(
        "--question", default="What is the current production backup cadence for Borealis?"
    )
    parser.add_argument("--strategy", choices=["auto", "static", "planner"], default="auto")
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--extractive-answer", action="store_true")
    parser.add_argument("--max-planner-searches", type=int, default=3)
    args = parser.parse_args()
    result = build_engine().query(
        args.question,
        strategy=args.strategy,
        top_k=args.top_k,
        max_planner_searches=args.max_planner_searches,
    )
    report = result.as_dict()
    if args.extractive_answer:
        report["source_answer"] = extract_source_answer(result).as_dict()
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
