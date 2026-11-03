from knowledge_engine.agent.actions import (
    PlannerActionType,
)
from knowledge_engine.agent.oracle_planner import OraclePlanner
from knowledge_engine.agent.state import PlannerState
from knowledge_engine.retrieval.state import RetrievalState
from knowledgebench.tasks.multihop_schema import (
    EvidenceHop,
    MultiHopTask,
)


def make_task() -> MultiHopTask:
    return MultiHopTask(
        task_id="mh-test",
        question="Question?",
        expected_answer="answer",
        hops=[
            EvidenceHop(
                hop_index=0,
                query="Find Atlas owner",
                query_template="Find Atlas owner",
                expected_document_id="doc-1",
                expected_fact="Platform Reliability",
            )
        ],
    )


def test_oracle_planner_searches_before_stop() -> None:
    planner = OraclePlanner()
    task = make_task()

    search = planner.next_action(
        task,
        PlannerState(question=task.question),
    )

    assert search.action_type == PlannerActionType.SEARCH
    assert search.query == "Find Atlas owner"


def test_oracle_planner_stops_after_all_hops() -> None:
    planner = OraclePlanner()
    task = make_task()

    state = PlannerState(
        question=task.question,
        step_index=1,
        retrieval_state=RetrievalState(
            entity="answer"
        ),
    )

    stop = planner.next_action(
        task,
        state,
    )

    assert stop.action_type == PlannerActionType.STOP
    assert stop.answer == "answer"
