from knowledge_engine.training.measured_policy_dataset import (
    MeasuredPolicyExample,
)
from knowledge_engine.training.retrieval_policy import (
    RetrievalPolicyAction,
    RetrievalPolicySplit,
)
from scripts.run_phase11_measured_v1_lora_sft import (
    build_training_tensors,
)


class FakeTokenizer:
    def apply_chat_template(
        self,
        messages,
        *,
        tokenize,
        add_generation_prompt,
        return_dict=True,
    ):
        token_ids = (
            [10, 11]
            if add_generation_prompt
            else [10, 11, 12]
        )
        if return_dict:
            return {"input_ids": token_ids}
        return token_ids


def test_training_tensors_request_list_token_ids() -> None:
    example = MeasuredPolicyExample(
        example_id="train-1",
        source_task_id="task-1",
        evidence_family="family-1",
        split=RetrievalPolicySplit.TRAIN,
        question="How many candidates?",
        target_action=RetrievalPolicyAction.SEARCH_HYBRID_K1,
        label_source="test",
    )

    input_ids, attention_mask, labels = build_training_tensors(
        FakeTokenizer(),
        example,
    )

    assert input_ids.tolist() == [[10, 11, 12]]
    assert attention_mask.tolist() == [[1, 1, 1]]
    assert labels.tolist() == [[-100, -100, 12]]
