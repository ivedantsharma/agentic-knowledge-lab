from knowledge_engine.agent.actions import (
    PlannerActionType,
)
from knowledge_engine.agent.rule_based_planner import (
    RuleBasedPlanner,
)
from knowledge_engine.agent.state import PlannerState
from knowledge_engine.retrieval.state import RetrievalState


def test_planner_forms_initial_operates_query() -> None:
    planner = RuleBasedPlanner()

    action = planner.next_action(
        PlannerState(
            question=(
                "What cache duration is used by the service "
                "maintained by the team that operates Helios?"
            )
        )
    )

    assert action.action_type == PlannerActionType.SEARCH
    assert action.query == "Which team operates Helios?"


def test_planner_preserves_qualifier_in_next_query() -> None:
    planner = RuleBasedPlanner()

    state = PlannerState(
        question=(
            "What backup cadence is used by the storage "
            "system maintained by the team that operates Atlas?"
        ),
        retrieval_state=RetrievalState(
            entity="Borealis",
            qualifiers=["production"],
            evidence_text=(
                "Platform Reliability maintains the Borealis "
                "storage system for production customer data."
            ),
        ),
    )

    action = planner.next_action(state)

    assert action.query == (
        "What is the incremental backup cadence for "
        "the production Borealis service?"
    )


def test_planner_stops_on_final_evidence() -> None:
    planner = RuleBasedPlanner()

    state = PlannerState(
        question="How long is metadata cached?",
        retrieval_state=RetrievalState(
            entity="ten minutes",
            evidence_text=(
                "Validated metadata is cached for ten minutes."
            ),
        ),
    )

    action = planner.next_action(state)

    assert action.action_type == PlannerActionType.STOP
    assert action.answer == "ten minutes"
