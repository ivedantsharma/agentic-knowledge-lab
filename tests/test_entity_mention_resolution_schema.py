from knowledgebench.tasks.graph_schema import (
    EntityMentionResolutionTask,
)


def test_resolvable_mention_task_requires_entity() -> None:
    task = EntityMentionResolutionTask(
        task_id="t1",
        question="Which system?",
        mention_text="customer storage system",
        expected_entity_id="borealis",
        should_resolve=True,
    )

    assert task.expected_entity_id == "borealis"
