import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

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
                "You are a precise search-planning assistant. "
                "Follow the user's requested output format exactly."
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
        max_new_tokens=64,
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
            "query_generation_no_evidence",
            (
                "Generate one concise search query that would help "
                "answer the question. Do not answer the question. "
                "Return only the search query.\n"
                f"Question: {QUESTION}"
            ),
        ),
        (
            "query_generation_after_intermediate_evidence",
            (
                "Generate the next search query needed to answer the "
                "original question. Do not answer yet. "
                "Return only the search query.\n"
                f"Original question: {QUESTION}\n"
                f"Evidence: {INTERMEDIATE_EVIDENCE}"
            ),
        ),
        (
            "answer_extraction_from_final_evidence",
            (
                "Answer the original question using only the evidence. "
                "Return only the answer.\n"
                f"Original question: {QUESTION}\n"
                f"Evidence: {FINAL_EVIDENCE}"
            ),
        ),
        (
            "answerability_without_evidence",
            (
                "Decide whether the evidence is enough to answer the "
                "question. Reply only YES or NO.\n"
                f"Question: {QUESTION}\n"
                "Evidence: None"
            ),
        ),
        (
            "answerability_with_final_evidence",
            (
                "Decide whether the evidence is enough to answer the "
                "question. Reply only YES or NO.\n"
                f"Question: {QUESTION}\n"
                f"Evidence: {FINAL_EVIDENCE}"
            ),
        ),
    ]

    print(f"model={MODEL_NAME}")
    print()

    for name, instruction in probes:
        output = generate(
            tokenizer,
            model,
            instruction,
        )

        print(name)
        print(f"output={output!r}")
        print()


if __name__ == "__main__":
    main()
