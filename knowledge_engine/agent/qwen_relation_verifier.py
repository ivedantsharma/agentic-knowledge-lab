from transformers import AutoModelForCausalLM, AutoTokenizer

DEFAULT_MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"


class QwenRelationVerifier:
    """Verify that a grounded candidate answers the requested relation."""

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

    def verify(
        self,
        question: str,
        evidence: str,
        candidate_answer: str,
    ) -> bool:
        output = self._generate(
            "Decide whether the candidate answer directly answers "
            "the exact relation requested by the question AND is "
            "supported by the evidence. Reply only YES or NO.\n"
            f"Question: {question}\n"
            f"Evidence: {evidence}\n"
            f"Candidate answer: {candidate_answer}"
        )

        normalized = output.strip().casefold()

        if normalized == "yes":
            return True

        if normalized == "no":
            return False

        raise ValueError(
            "relation verifier output must be YES or NO; "
            f"raw_output={output!r}"
        )

    def _generate(
        self,
        instruction: str,
    ) -> str:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a strict answer verifier. "
                    "Follow the requested format exactly."
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
            max_new_tokens=32,
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
