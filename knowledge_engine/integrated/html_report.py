"""Generate a portable, no-JavaScript HTML report for a real retrieval trace.

All untrusted question and document fields are escaped. No backend is hosted.
"""

from html import escape

from knowledge_engine.integrated.pipeline import IntegratedResult
from knowledge_engine.integrated.verification import SourceAnswer


def render_demo_html(result: IntegratedResult, verdict: SourceAnswer) -> str:
    question = escape(result.question)
    value = escape(verdict.answer) if verdict.answer is not None else "No supported answer"
    status = escape(verdict.status)
    reason = escape(verdict.reason)
    fallback = escape(result.fallback_reason or "None")
    steps = "\n".join(
        "<li><strong>Query:</strong> " + escape(step.query)
        + "<div class='small'>Retrieved: "
        + escape(", ".join(step.returned_document_ids)) + "</div></li>"
        for step in result.steps
    )
    evidence = "\n".join(
        "<article><div class='line'><strong>" + escape(hit.title) + "</strong>"
        + "<span class='tag'>" + escape(hit.risk_flag or "no metadata risk flag") + "</span>"
        + "</div><div class='small'>" + escape(hit.document_id)
        + " · source: " + escape(hit.source_type)
        + " · effective: " + escape(hit.effective_at or "unspecified")
        + "</div><p>" + escape(hit.text) + "</p></article>"
        for hit in result.evidence
    )
    citations = escape(", ".join(verdict.citation_document_ids) or "none")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Agentic Knowledge Lab — Evidence Trace</title>
<style>
:root {{ color-scheme:light; font-family:system-ui,-apple-system,sans-serif; }}
body {{ margin:0; background:#f7f9fc; color:#182235; }}
main {{ max-width:1000px; padding:32px 20px; margin:auto; }}
header {{ padding:24px; background:#14233d; border-radius:16px; color:white; }}
h1 {{ margin:0 0 10px; font-size:1.7rem; }}
h2 {{ font-size:1.2rem; margin-top:28px; }}
section,article {{ background:white; padding:18px; border-radius:12px;
  border:1px solid #e2e7f0; margin:12px 0; }}
.line {{ display:flex; flex-wrap:wrap; justify-content:space-between; gap:12px; }}
.tag {{ background:#e9edf5; font-size:.75rem; border-radius:8px; padding:5px 8px; }}
.small {{ color:#53627a; font-size:.8rem; margin-top:8px; overflow-wrap:anywhere; }}
p,li {{ line-height:1.65; overflow-wrap:anywhere; }}
ol {{ padding-left:24px; }}
.mark {{ font-size:1.2rem; font-weight:700; }}
footer {{ color:#53627a; margin-top:28px; }}
</style></head><body><main>
<header><h1>Agentic Knowledge Lab</h1>
<p>Explainable retrieval · CPU-only demonstration · not independently fact checked</p>
<p><strong>Question:</strong> {question}</p></header>
<h2>Extractive support decision</h2>
<section><div class="mark">{value}</div>
<p>Status: {status} · Reason: {reason}</p>
<p class="small">Source citations: {citations}</p>
<p class="small">This answer, if present, is a restricted extraction from retrieved
service manuals, NOT a verified world fact or an LLM-generated response.</p></section>
<h2>Planner and fallback</h2>
<section><p>Requested: {escape(result.strategy_requested)} ·
Used: {escape(result.strategy_used)} · Fallback: {fallback}</p>
<ol>{steps}</ol></section>
<h2>Retrieved source evidence ({len(result.evidence)})</h2>
{evidence}
<footer>The benchmark gold labels are not inputs to this demo. Previous/pending
source flags reflect metadata only. The research is development-stage; see
docs/research/phase13-final-review.md for measured limits.</footer>
</main></body></html>"""
