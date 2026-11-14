"""Phase 14 HTML: source text is HTML-escaped and citations are traceable."""

from knowledge_engine.integrated.html_report import render_demo_html
from knowledge_engine.integrated.verification import extract_source_answer
from scripts.run_phase14_integrated_demo import build_engine


def test_html_contains_actual_evidence_decision_and_source_ids():
    result = build_engine().query(
        "What is the current production incremental backup cadence for Borealis?",
        strategy="static", top_k=5,
    )
    verdict = extract_source_answer(result)
    html = render_demo_html(result, verdict)
    assert html.startswith("<!doctype html>")
    assert "every six hours" in html
    assert "kbv2-doc-borealis-current" in html
    assert "source_supported_extractive" in html
    assert "not independently fact checked" in html


def test_untrusted_question_and_evidence_escaped():
    engine = build_engine()
    result = engine.query(
        '<script>alert("attack")</script> Borealis incremental backups',
        strategy="static", top_k=3,
    )
    verdict = extract_source_answer(result)
    html = render_demo_html(result, verdict)
    assert '&lt;script&gt;alert(&quot;attack&quot;)&lt;/script&gt;' in html
    assert "<script>alert(" not in html


def test_unsupported_question_displays_abstention():
    result = build_engine().query(
        "Which team owns the employee parking permit application?",
        strategy="auto", top_k=3,
    )
    html = render_demo_html(result, extract_source_answer(result))
    assert "No supported answer" in html
    assert "planner_with_static_fallback" in html
    assert "No supported answer" in html
