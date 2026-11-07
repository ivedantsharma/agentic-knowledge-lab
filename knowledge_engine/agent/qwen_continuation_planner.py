from transformers import AutoModelForCausalLM, AutoTokenizer

from knowledge_engine.agent.actions import (
    PlannerAction,
    PlannerActionType,
)
from knowledge_engine.agent.state import PlannerState

DEFAULT_MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"
PLANNER_IMPLEMENTATION_VERSION = "grounded-stop-v2"


class QwenContinuationPlanner:
    """Use Qwen for continuation queries, stopping, and extraction."""

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL_NAME,
    ) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name
        )

    def inspect_decision(
        self,
        state: PlannerState,
    ) -> dict[str, str | bool | None]:
        evidence = (
            state.retrieval_state.evidence_text
            or ""
        )

        if not evidence:
            raise ValueError(
                "QwenContinuationPlanner requires prior evidence"
            )

        answerable = self.is_answerable(
            state.question,
            evidence,
        )

        candidate_answer: str | None = None
        grounded = False

        if answerable:
            candidate_answer = self.extract_answer(
                state.question,
                evidence,
            )
            grounded = self.is_grounded_answer(
                candidate_answer,
                evidence,
            )

        return {
            "answerable": answerable,
            "candidate_answer": candidate_answer,
            "grounded": grounded,
        }

    def next_action(
        self,
        state: PlannerState,
    ) -> PlannerAction:
        decision = self.inspect_decision(state)

        candidate_answer = decision["candidate_answer"]

        if (
            decision["answerable"]
            and decision["grounded"]
            and isinstance(candidate_answer, str)
        ):
            return PlannerAction(
                action_type=PlannerActionType.STOP,
                answer=candidate_answer,
            )

        evidence = (
            state.retrieval_state.evidence_text
            or ""
        )

        query = self.generate_next_query(
            state.question,
            evidence,
        )

        return PlannerAction(
            action_type=PlannerActionType.SEARCH,
            query=query,
        )

    def is_answerable(
        self,
        question: str,
        evidence: str,
    ) -> bool:
        output = self._generate(
            "Decide whether the evidence is enough to answer "
            "the original question. Reply only YES or NO.\n"
            f"Original question: {question}\n"
            f"Evidence: {evidence}"
        )

        normalized = output.strip().casefold()

        if normalized == "yes":
            return True

        if normalized == "no":
            return False

        raise ValueError(
            "answerability output must be YES or NO; "
            f"raw_output={output!r}"
        )

    def generate_next_query(
        self,
        question: str,
        evidence: str,
    ) -> str:
        output = self._generate(
            "Generate the next concise search query needed to "
            "answer the original question. Do not answer yet. "
            "Return only the search query.\n"
            f"Original question: {question}\n"
            f"Evidence: {evidence}"
        )

        if not output:
            raise ValueError(
                "Qwen returned an empty search query"
            )

        return output

    def extract_answer(
        self,
        question: str,
        evidence: str,
    ) -> str:
        output = self._generate(
            "Copy the shortest exact span from the evidence that "
            "answers the original question. Do not paraphrase. "
            "Return only that exact span.\n"
            f"Original question: {question}\n"
            f"Evidence: {evidence}"
        )

        if not output:
            raise ValueError(
                "Qwen returned an empty answer"
            )

        return output

    @staticmethod
    def is_grounded_answer(
        answer: str,
        evidence: str,
    ) -> bool:
        normalized_answer = " ".join(
            answer.casefold().split()
        )
        normalized_evidence = " ".join(
            evidence.casefold().split()
        )

        return (
            bool(normalized_answer)
            and normalized_answer in normalized_evidence
        )

    def _generate(
        self,
        instruction: str,
    ) -> str:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a precise search-planning assistant. "
                    "Follow the requested output format exactly."
                ),
            },
            {
                "role": "user",
                "content": instruction,
            },
        ]

        prompt = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
        )

        output_ids = self.model.generate(
            **inputs,
            max_new_tokens=64,
            do_sample=False,
        )

        generated_ids = output_ids[
            :,
            inputs["input_ids"].shape[1] :,
        ]

        return self.tokenizer.batch_decode(
            generated_ids,
            skip_special_tokens=True,
        )[0].strip()
