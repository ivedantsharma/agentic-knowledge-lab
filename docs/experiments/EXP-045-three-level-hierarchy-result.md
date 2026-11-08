# EXP-045 Result: Three-Level Hierarchical Retrieval Baseline

## Aggregate

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

## Main finding

The document and section levels preserve all answer-bearing evidence, but the chunk level loses one task.

## Borealis failure

The relevant section contains:

```text
Full backups run every Sunday, while incremental backups run every six hours.
```

With 10-word chunks and zero overlap, the evidence phrase crosses the boundary:

```text
chunk 0: ... incremental backups run every
chunk 1: six hours.
```

The benchmark evidence:

```text
every six hours
```

is therefore present in neither chunk.

This is evidence fragmentation, not retrieval ranking failure.

## Cirrus

The relevant chunk survives at rank 2.

This is consistent with the earlier child-level beam result: a hard distractor remains rank 1, but the answer-bearing evidence is still nearby.

## Context effect

Average retained text falls from:

```text
23.33 section words
```

to:

```text
16.33 retained chunk words
```

but evidence retention falls from 1.0 to 0.6667.

Therefore smaller context is not automatically better if chunk boundaries destroy evidence.

## Conclusion

The third hierarchy level is mechanically working, but zero-overlap chunking is too brittle for boundary-spanning evidence.