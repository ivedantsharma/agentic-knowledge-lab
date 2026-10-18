import sys
from pathlib import Path

if not __package__:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from knowledge_engine.ingestion.chunker import chunk_by_words
from knowledge_engine.ingestion.loader import load_source_documents_jsonl

SOURCE_PATH = Path("data/processed/phase2_source_documents_v0.jsonl")
OUTPUT_PATH = Path("data/processed/phase2_chunks_overlap6_v1.jsonl")


def main() -> None:
    documents = load_source_documents_jsonl(SOURCE_PATH)

    chunks = []

    for document in documents:
        chunks.extend(
            chunk_by_words(
                document,
                chunk_size_words=18,
                overlap_words=6,
            )
        )

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        for chunk in chunks:
            file.write(chunk.model_dump_json())
            file.write("\n")

    print(f"Wrote {len(chunks)} chunks to {OUTPUT_PATH}")

    for chunk in chunks:
        print(
            f"{chunk.chunk_id}: "
            f"[{chunk.start_word}:{chunk.end_word}] "
            f"{chunk.text}"
        )


if __name__ == "__main__":
    main()
