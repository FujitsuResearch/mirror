# Reproducibility

This release separates three levels of reproducibility.

## Level 1: Shipped Canonical Tables

The file below is copied from the camera-ready supplementary material:

```text
artifacts/paper_results/EXPERIMENT_RESULTS_FULL_CANONICAL.tex
```

Verify it with:

```bash
python scripts/verify_paper_tables.py
```

This reproduces the canonical supplementary result table values shipped with this repository.

## Level 2: Payload-Free Run Records

To recompute metrics from per-case records, provide JSONL records with at least:

```json
{
  "case_id": "stable-case-id",
  "target": "generalrag",
  "surface": "B1_TEXT_POISON",
  "method": "grimoire",
  "score": 0.8,
  "target_queries": 3,
  "elapsed_seconds": 120.0
}
```

Optional fields:

```json
{
  "success": true,
  "best_attack": "optional text payload if approved for release",
  "duplicate_benchmark": false
}
```

Run:

```bash
python scripts/compute_metrics_from_jsonl.py path/to/payload_free_results.jsonl
```

Rules:

- if `success` is absent, success is computed as `score >= 0.7`
- missing required fields cause an error
- text-only diversity and duplication metrics are reported only when required text fields exist
- no missing value is replaced by a synthetic value

## Level 3: Full Target Replay

Full target replay requires the original target wrappers, model access, approved prompts, and run configuration. This repository includes the fixed public configuration in:

```text
configs/paper_config.json
```

This public release does not include private credentials, private target state, or private payload data.

## No Synthetic Reporting Policy

This repository does not reconstruct per-case records from aggregate tables. If raw payload-free run logs are not available, the scripts report that limitation directly.
