from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from knowledge_engine.agent.actions import (
    PlannerAction,
    PlannerActionType,
)
from knowledge_engine.agent.state import PlannerState

DEFAULT_MODEL_NAME = "google/flan-t5-small"


class LocalGenerativePlanner:
    """Small local model that generates SEARCH or STOP actions."""

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL_NAME,
    ) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name
        )
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            model_name
        )

    def next_action(
        self,
        state: PlannerState,
    ) -> PlannerAction:
        output = self.generate_raw(state)

        try:
            return self.parse_action(output)
        except ValueError as error:
            raise ValueError(
                f"{error}; raw_output={output!r}"
            ) from error

    def generate_raw(
        self,
        state: PlannerState,
    ) -> str:
        """Generate raw planner text before protocol parsing."""
        prompt = self.build_prompt(state)

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=768,
        )

        output_ids = self.model.generate(
            **inputs,
            max_new_tokens=64,
            do_sample=False,
        )

        return self.tokenizer.decode(
            output_ids[0],
            skip_special_tokens=True,
        ).strip()

    @staticmethod
    def build_prompt(
        state: PlannerState,
    ) -> str:
        retrieval_state = state.retrieval_state

        evidence = (
            retrieval_state.evidence_text
            if retrieval_state.evidence_text is not None
            else "None"
        )

        entity = (
            retrieval_state.entity
            if retrieval_state.entity is not None
            else "None"
        )

        qualifiers = (
            ", ".join(retrieval_state.qualifiers)
            if retrieval_state.qualifiers
            else "None"
        )

        return (
            "You are a search planner. "
            "Answer with exactly one action.\n"
            "Use SEARCH: <query> when more evidence is needed.\n"
            "Use STOP: <answer> only when the evidence directly "
            "answers the original question.\n"
            "Do not answer a different relation just because it "
            "appears in the evidence.\n\n"
            f"Original question: {state.question}\n"
            f"Current entity: {entity}\n"
            f"Qualifiers: {qualifiers}\n"
            f"Latest evidence: {evidence}\n\n"
            "Action:"
        )

    @staticmethod
    def parse_action(
        output: str,
    ) -> PlannerAction:
        cleaned = output.strip()

        if cleaned.upper().startswith("SEARCH:"):
            query = cleaned.split(":", 1)[1].strip()

            if not query:
                raise ValueError(
                    "generative planner returned empty SEARCH"
                )

            return PlannerAction(
                action_type=PlannerActionType.SEARCH,
                query=query,
            )

        if cleaned.upper().startswith("STOP:"):
            answer = cleaned.split(":", 1)[1].strip()

            if not answer:
                raise ValueError(
                    "generative planner returned empty STOP"
                )

            return PlannerAction(
                action_type=PlannerActionType.STOP,
                answer=answer,
            )

        raise ValueError(
            "generative planner output must start with "
            "SEARCH: or STOP:"
        )
