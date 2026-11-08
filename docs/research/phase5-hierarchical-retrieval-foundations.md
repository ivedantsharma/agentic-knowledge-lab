# Phase 5 — Hierarchical Retrieval Foundations

## Phase status

Phase 5 has started.

Current completion:

~10%

## Research question

Can a document → section hierarchy improve evidence discovery and retrieval efficiency compared with searching all sections in one flat index?

## Flat retrieval

Flat section retrieval treats every section as an independent candidate:

query → all sections → global ranking

The retriever does not explicitly use parent-child structure during search.

## Hierarchical retrieval

Hierarchical retrieval narrows the search space in stages:

query → rank documents → choose parent → rank sections inside parent → choose section

This is coarse-to-fine retrieval.

## Why hierarchy might help

If a corpus contains 10,000 sections, flat retrieval compares against all 10,000. A hierarchical system may first select a small number of documents and then search only their children.

Potential benefits:

- fewer child candidates,
- less cross-document distractor competition,
- parent context is naturally available,
- lower downstream context budget.

## Why hierarchy can hurt

The first stage creates a routing bottleneck.

If the correct parent document is missed, the correct child section becomes unreachable.

So hierarchy trades global breadth for structured narrowing.

## First Phase 5 architecture

We start with two levels:

Document → Section

Chunks inside sections come later.

### Document representation

For the first baseline, each document is represented by its title plus section titles.

Example:

Document: Borealis Storage Manual. Sections: Storage Overview, Backup Policy, Encryption, Restore Process.

This is intentionally deterministic and cheap.

### Section representation

Each section includes its parent title:

Document: Borealis Storage Manual. Section: Backup Policy. Full backups run ...

## Metrics

### Document Hit@1

Did document-level routing choose the correct source document?

### Flat Section Hit@1

Did global section retrieval select the section containing the evidence?

### Hierarchical Section Hit@1

After parent routing, did child retrieval select the section containing the evidence?

### Candidate count

We also compare how many child candidates are searched per query.

## Scientific caution

The initial corpus has only three documents and twelve sections. It validates the mechanism only. If flat and hierarchical retrieval both score perfectly, the next step is a stress test with cross-document distractors.