# Reproducibility

The public artifact preserves the frozen one-shot evaluation separately from post-review repair analyses.

## No-cost verification
Use `SHA256SUMS.txt` to verify immutable distributable packages and result files. The checksum file intentionally excludes itself and mutable documentation files.

## Locked implementation facts
- Embedding: `text-embedding-3-large`
- Generator/reranker: `gpt-5.6-terra`
- BM25: `k1=1.5`, `b=0.75`
- Dense similarity: cosine
- RRF: `k=60`
- DEV hybrid chunking: 512/128 lexical tokens/overlap
- DEV rerank pool: 15 -> top 5
- Final rerank pool: 10 -> top 5
- Original final logical stage: post-generation audit, not enforced rewrite
- Final evaluation: 300 items; 48 local; 252 API path

## Cost and latency
Archived Batch usage reconstructs to USD 3.348244965 for the final evaluation. Batch wall time is not interactive latency. Synchronous interactive latency is reported from DEV only.

## Post-review repair
The `post_review_*` artifacts are secondary deterministic analyses. They do not replace the original one-shot outputs and must not be merged into the original headline result.
