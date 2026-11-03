from knowledge_engine.agent.actions import (
    PlannerAction,
    PlannerActionType,
)
from knowledge_engine.agent.state import PlannerState
from knowledgebench.tasks.multihop_schema import MultiHopTask
from scripts.run_phase3_structured_state_chain import (
    render_state_query,
)


class OraclePlanner:
    """Planner that follows the benchmark's gold hop sequence."""

    def next_action(
        self,
        task: MultiHopTask,
        state: PlannerState,
    ) -> PlannerAction:
        if state.step_index < len(task.hops):
            hop = task.hops[state.step_index]

            template = (
                hop.query_template
                or hop.query
            )

            query = render_state_query(
                template,
                state.retrieval_state,
            )

            return PlannerAction(
                action_type=PlannerActionType.SEARCH,
                query=query,
            )

        if state.retrieval_state.entity is None:
            raise ValueError(
                "oracle planner cannot stop "
                "without a final extracted fact"
            )

        return PlannerAction(
            action_type=PlannerActionType.STOP,
            answer=state.retrieval_state.entity,
        )
