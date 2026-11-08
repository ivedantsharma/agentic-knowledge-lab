import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

QUESTION = (
    "Where are failed jobs sent after the production worker "
    "platform owned by Developer Productivity exhausts all "
    "retry attempts?"
)

INTERMEDIATE_EVIDENCE = (
    "Developer Productivity maintains the Cirrus worker "
    "platform for production asynchronous workloads."
)

FINAL_EVIDENCE = (
    "For the production Cirrus worker platform, failed jobs "
    "are retried at most five times before dead-letter handling. "
    "Jobs that exhaust retries are sent to the CIRRUS-DLQ "
    "dead-letter queue."
)


def generate(
    tokenizer: AutoTokenizer,
    model: AutoModelForCausalLM,
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

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
    )

    output_ids = model.generate(
        **inputs,
        max_new_tokens=32,
        do_sample=False,
    )

    generated_ids = output_ids[
        :,
        inputs["input_ids"].shape[1] :,
    ]

    return tokenizer.batch_decode(
        generated_ids,
        skip_special_tokens=True,
    )[0].strip()


def main() -> None:
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME
    )
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME
    )

    probes = [
        (
            "wrong_candidate_intermediate",
            INTERMEDIATE_EVIDENCE,
            "Cirrus",
        ),
        (
            "wrong_candidate_owner",
            INTERMEDIATE_EVIDENCE,
            "Developer Productivity",
        ),
        (
            "correct_candidate_final",
            FINAL_EVIDENCE,
            "CIRRUS-DLQ",
        ),
        (
            "long_correct_candidate_final",
            FINAL_EVIDENCE,
            "CIRRUS-DLQ dead-letter queue",
        ),
    ]

    print(f"model={MODEL_NAME}")
    print()

    for name, evidence, candidate in probes:
        instruction = (
            "Decide whether the candidate answer directly answers "
            "the exact relation requested by the question AND is "
            "supported by the evidence. Reply only YES or NO.\n"
            f"Question: {QUESTION}\n"
            f"Evidence: {evidence}\n"
            f"Candidate answer: {candidate}"
        )

        output = generate(
            tokenizer,
            model,
            instruction,
        )

        print(name)
        print(f"candidate={candidate!r}")
        print(f"output={output!r}")
        print()


if __name__ == "__main__":
    main()
