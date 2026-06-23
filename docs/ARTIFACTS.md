# Artifact Manifest

Included artifacts are minimal.

## Included

- `artifacts/paper_results/EXPERIMENT_RESULTS_FULL_CANONICAL.tex`
  - canonical supplementary table source
  - payload-free aggregate table artifact

- `artifacts/figures/benchmark_v2_stats.pdf`
  - supplementary Figure S1

- `artifacts/figures/patched_known_b1_asr.pdf`
  - supplementary Figure S2A

- `artifacts/figures/patched_known_b1_selfdup.pdf`
  - supplementary Figure S2B

- `artifacts/figures/cyberrag_evalmode_stability.pdf`
  - supplementary Figure S2C

- `artifacts/figures/dup_scaling_b1.pdf`
  - supplementary Figure S3A

- `artifacts/figures/dup_scaling_b3.pdf`
  - supplementary Figure S3B

- `artifacts/figures/dup_scaling_b4.pdf`
  - supplementary Figure S3C

## Excluded

The release excludes private credentials and environment files, private
workspace files, internal documents, raw payload records, slide/poster build
files, local demos unrelated to the MIRROR release, generated backups, and
LaTeX build intermediates.

## Verification

Run:

```bash
python scripts/check_release.py
python scripts/verify_paper_tables.py
```
