"""Produce a self-contained HTML demo without local model weights or services."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.integrated.html_report import render_demo_html
from knowledge_engine.integrated.verification import extract_source_answer
from scripts.run_phase14_integrated_demo import build_engine


def main() -> None:
    parser = argparse.ArgumentParser(description="Export standalone evidence report")
    parser.add_argument("--output", type=Path, default=Path("phase14_demo.html"))
    parser.add_argument(
        "--question",
        default="What is the current production incremental backup cadence for Borealis?",
    )
    parser.add_argument("--strategy", choices=["auto", "static", "planner"], default="static")
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()
    result = build_engine().query(args.question, strategy=args.strategy, top_k=args.top_k)
    verdict = extract_source_answer(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_demo_html(result, verdict), encoding="utf-8")
    print(f"HTML evidence demo written to {args.output}")
    print(f"strategy={result.strategy_used} status={verdict.status} answer={verdict.answer!r}")


if __name__ == "__main__":
    main()
