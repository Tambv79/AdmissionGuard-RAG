# AdmissionGuard-RAG

Research artifact for **Cost-Aware and Safety-Grounded RAG for Vietnamese University Admission Question Answering**.

## Empirical scope
This repository documents the Hai Phong University 2026 regular-admission case study. The main TEST/STRESS one-shot results are frozen and unchanged. Files prefixed `post_review_` are separately labeled deterministic repair analyses and are not part of the original one-shot result.

## Artifact contents
- `packages/corpus_v1.0.1_public_safe.zip`: normalized/structured corpus artifact and provenance metadata; raw institutional PDFs are excluded.
- `packages/dev_gold_review.zip`: DEV benchmark human-review closure.
- `packages/dev_experiment_harness.zip`: DEV code/configuration.
- `packages/dev_results_audit.zip`: DEV results, statistics, usage and audit.
- `packages/final_protocol.zip`: locked TEST/STRESS protocol.
- `packages/final_results.zip`: frozen final outputs, Batch usage/recovery evidence.
- `results/`: item-level final audit, critical failures, and separately labeled post-review repair artifacts.

## Integrity
`SHA256SUMS.txt` records SHA-256 hashes for distributable files and intentionally excludes itself.

## Public repository
https://github.com/Tambv79/AdmissionGuard-RAG

The repository is publicly readable. Reuse rights remain subject to repository licensing status; public availability alone does not grant reuse rights. Raw official institutional PDFs remain excluded until redistribution rights are independently confirmed.

## Scientific boundary
The reported evidence covers one institution, one admission cycle, one frozen corpus snapshot, and the documented model stack. It does not establish cross-institution, real-user, security, or production-deployment effectiveness.
