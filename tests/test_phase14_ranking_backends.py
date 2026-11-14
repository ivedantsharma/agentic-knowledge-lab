"""Phase 14 ranking backend adapters, no model download in unit tests."""

import numpy as np
import pytest

from knowledge_engine.integrated.backends import create_ranking_backend
from knowledge_engine.integrated.pipeline import IntegratedKnowledgeEngine
from knowledgebench.documents.v2_schema import KnowledgeBenchV2Document
from scripts.run_phase14_integrated_demo import build_engine


class FakeEncoder:
    def encode(self, input_value):
        def features(value):
            value = value.casefold()
            return np.array([
                float(value.count("borealis") + 0.01),
                float(value.count("cirrus") + 0.01),
                float(value.count("backup") + 0.01),
            ])
        if isinstance(input_value, str):
            return features(input_value)
        return np.asarray([features(value) for value in input_value])


def docs():
    return [
        KnowledgeBenchV2Document(
            document_id="a", title="Borealis", text="Borealis backup cadence every six hours.",
            source_type="service_manual"
        ),
        KnowledgeBenchV2Document(
            document_id="b", title="Cirrus", text="Cirrus retry five times.",
            source_type="service_manual"
        ),
        KnowledgeBenchV2Document(
            document_id="c", title="Unrelated", text="Cafeteria team menu.",
            source_type="organization_record"
        ),
    ]


@pytest.mark.parametrize("name", ["bm25", "dense", "hybrid"])
def test_all_backends_return_ranked_source_ids(name):
    documents = docs()
    ranking = create_ranking_backend(documents, name=name, encoder=FakeEncoder())
    ranked = ranking.rank("Borealis backup", top_k=2)
    assert len(ranked) == 2
    assert ranked[0][0] == "a"
    assert {key for key, _ in ranked}.issubset({"a", "b", "c"})
    result = IntegratedKnowledgeEngine(documents, backend=ranking).query(
        "Borealis backup", strategy="static", top_k=2
    )
    assert result.steps[0].returned_document_ids[0] == "a"
    assert result.answer is None


def test_unknown_backend_and_duplicate_document_ids_fail():
    with pytest.raises(ValueError, match="unknown backend"):
        create_ranking_backend(docs(), name="graph")
    with pytest.raises(ValueError, match="unique"):
        create_ranking_backend([docs()[0], docs()[0]])


class FakeInvalidRanking:
    def rank(self, query, top_k):
        return [("unknown", 1.0)]


def test_invalid_backend_cannot_inject_unknown_document_ids():
    engine = IntegratedKnowledgeEngine(docs(), backend=FakeInvalidRanking())
    with pytest.raises(ValueError, match="duplicate, unknown or over-budget"):
        engine.query("query", strategy="static", top_k=2)


def test_real_schema_path_builds_dense_and_hybrid_with_fake_encoder():
    for name in ("dense", "hybrid"):
        result = build_engine(backend=name, encoder=FakeEncoder()).query(
            "Borealis backup", strategy="static", top_k=3
        )
        assert len(result.evidence) == 3
        assert result.status == "evidence_only_unverified"
