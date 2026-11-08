# EXP-045 Result: Three-Level Hierarchy Baseline

## Status

Provisional result — rerun required with the ancestry-preserving chunk representation.

## Observed aggregate

```text
ParentRecall@2=1.0000
SectionEvidenceRetentionRate=1.0000
ChunkRecall@1=0.3333
ChunkRecall@2=0.6667
ChunkEvidenceRetentionRate=0.6667
AvgSectionContextWords=23.33
AvgRetainedChunkWords=16.33
AvgChunksScored=3.33
```

## Important implementation discrepancy

The printed retained chunks were raw text such as:

```text
key identifier is ATLAS-KV-104.
```

rather than the intended ancestry-preserving representation:

```text
Document: Atlas Service Manual.
Section: Token Rotation.
key identifier is ATLAS-KV-104.
```

Therefore this run does not yet validate the final EXP-045 design.

## Borealis fragmentation diagnosis

The Borealis evidence is:

```text
every six hours
```

With 10-word chunks and zero overlap, the section is split so that one chunk ends with:

```text
... incremental backups run every
```

and the remaining words appear in the next chunk.

The exact evidence span is therefore absent from every individual chunk.

This is an evidence-fragmentation failure, not a parent- or section-routing failure.

## Scientific consequence

Two variables must not be conflated:

1. ancestry/context in chunk representation;
2. overlap needed to preserve boundary-spanning evidence.

First rerun EXP-045 with the intended ancestry-preserving code.

Then test overlap as a separate controlled experiment.
