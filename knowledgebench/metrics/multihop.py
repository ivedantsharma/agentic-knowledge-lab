def hop_accuracy(
    retrieved_document_ids: list[str],
    expected_document_ids: list[str],
) -> float:
    """Return the fraction of hops whose top-1 document is correct."""
    if len(retrieved_document_ids) != len(expected_document_ids):
        raise ValueError(
            "retrieved and expected hop lists must have equal length"
        )

    if not expected_document_ids:
        return 0.0

    correct = sum(
        retrieved == expected
        for retrieved, expected in zip(
            retrieved_document_ids,
            expected_document_ids,
        )
    )

    return correct / len(expected_document_ids)


def exact_chain_match(
    retrieved_document_ids: list[str],
    expected_document_ids: list[str],
) -> float:
    """Return 1.0 only when the entire ordered evidence chain matches."""
    if len(retrieved_document_ids) != len(expected_document_ids):
        return 0.0

    return float(
        retrieved_document_ids == expected_document_ids
    )


def fact_accuracy(
    extracted_facts: list[str | None],
    expected_facts: list[str],
) -> float:
    """Return the fraction of extracted facts matching gold facts."""
    if len(extracted_facts) != len(expected_facts):
        raise ValueError(
            "extracted and expected fact lists must have equal length"
        )

    if not expected_facts:
        return 0.0

    correct = sum(
        extracted is not None
        and extracted.casefold().strip()
        == expected.casefold().strip()
        for extracted, expected in zip(
            extracted_facts,
            expected_facts,
        )
    )

    return correct / len(expected_facts)
