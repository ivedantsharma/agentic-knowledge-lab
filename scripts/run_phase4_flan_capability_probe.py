import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


MODEL_NAME = "google/flan-t5-small"

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
    model: AutoModelForSeq2SeqLM,
    prompt: str,
) -> str:
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=768,
    )

    output_ids = model.generate(
        **inputs,
        max_new_tokens=64,
        do_sample=False,
    )

    return tokenizer.decode(
        output_ids[0],
        skip_special_tokens=True,
    ).strip()


def main() -> None:
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME
    )
    model = AutoModelForSeq2SeqLM.from_pretrained(
        MODEL_NAME
    )

    probes = [
        (
            "query_generation_no_evidence",
            (
                "Generate one concise search query that would help "
                "answer the question. Do not answer the question.\n"
                f"Question: {QUESTION}\n"
                "Search query:"
            ),
        ),
        (
            "query_generation_after_intermediate_evidence",
            (
                "Generate the next search query needed to answer the "
                "original question. Do not answer yet.\n"
                f"Original question: {QUESTION}\n"
                f"Evidence: {INTERMEDIATE_EVIDENCE}\n"
                "Next search query:"
            ),
        ),
        (
            "answer_extraction_from_final_evidence",
            (
                "Answer the original question using only the evidence. "
                "Return only the answer.\n"
                f"Original question: {QUESTION}\n"
                f"Evidence: {FINAL_EVIDENCE}\n"
                "Answer:"
            ),
        ),
        (
            "answerability_without_evidence",
            (
                "Decide whether the evidence is enough to answer the "
                "question. Reply only YES or NO.\n"
                f"Question: {QUESTION}\n"
                "Evidence: None\n"
                "Enough evidence:"
            ),
        ),
        (
            "answerability_with_final_evidence",
            (
                "Decide whether the evidence is enough to answer the "
                "question. Reply only YES or NO.\n"
                f"Question: {QUESTION}\n"
                f"Evidence: {FINAL_EVIDENCE}\n"
                "Enough evidence:"
            ),
        ),
    ]

    for name, prompt in probes:
        output = generate(
            tokenizer,
            model,
            prompt,
        )

        print(name)
        print(f"output={output!r}")
        print()


if __name__ == "__main__":
    main()
