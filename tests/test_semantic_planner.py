from knowledge_engine.agent.semantic_planner import (
    SemanticPlanner,
)
from knowledgebench.documents.schema import KnowledgeDocument


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def make_documents() -> list[KnowledgeDocument]:
    return [
        KnowledgeDocument(
            document_id="atlas",
            text=(
                "Atlas is operated by the Platform Reliability "
                "team."
            ),
        ),
        KnowledgeDocument(
            document_id="security",
            text=(
                "Security Platform maintains the Meridian "
                "signing service."
            ),
        ),
    ]


def test_discovers_anchor_entities() -> None:
    planner = SemanticPlanner(
        make_documents(),
        MODEL_NAME,
    )

    assert planner.find_anchor_entity(
        "Atlas is run by some team."
    ) == "Atlas"

    assert planner.find_anchor_entity(
        "Security Platform is responsible for signing."
    ) == "Security Platform"


def test_classifies_retry_paraphrase() -> None:
    planner = SemanticPlanner(
        make_documents(),
        MODEL_NAME,
    )

    goal = planner.classify_goal(
        "What is the maximum number of retries a failed job gets?"
    )

    assert goal == "retry"
