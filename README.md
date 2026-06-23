# MIRROR

Official public repository for the IEEE WCCI / IJCNN 2026 paper:

**MIRROR: Novelty-Constrained Memory-Guided MCTS Red-Teaming for Agentic RAG**

Authors: Inderjeet Singh, Andrés Murillo, Motoyoshi Sekiya, Yuki Unno, Junichi Suga

## Contents

This repository contains the public, reproducible part of the MIRROR release:

- deterministic novelty gate implementation
- generic memory-guided PUCT search utilities
- metric implementations used by the paper, including ASR, Wilson CI, DupBench, Novel-ASR, and SelfDup
- scripts to verify the shipped canonical paper-result tables
- scripts to recompute metrics from payload-free JSONL run records when those records are supplied
- paper configuration files with the fixed budgets and model-role settings reported in the paper
- canonical supplementary result table source and the small supporting figure artifacts cited by the supplement

## Not Included

This package does not include private credentials or environment files, private
workspace files, internal documents, benchmark payload records, or per-case run
logs reconstructed from aggregate tables.

If a required raw artifact is missing, the scripts fail with a clear error. They do not silently fill missing values.

## Quick Start

Use Python 3.10 or newer.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python scripts/verify_paper_tables.py
python -m unittest discover -s tests
```

The table verifier confirms the six canonical supplementary result tables shipped under `artifacts/paper_results/`.

## Reproducing Paper Numbers

The shipped canonical result table source is:

```text
artifacts/paper_results/EXPERIMENT_RESULTS_FULL_CANONICAL.tex
```

Run:

```bash
python scripts/verify_paper_tables.py
```

This checks the shipped canonical table for internal consistency against the values cited in the paper and supplement. It is an integrity check, not an independent recomputation from raw run logs.

To recompute metrics from payload-free JSONL records, provide records with the schema described in `docs/REPRODUCIBILITY.md`:

```bash
python scripts/compute_metrics_from_jsonl.py path/to/payload_free_results.jsonl
```

## Dataset

The paper uses ART-SafeBench. The dataset is hosted separately on Hugging Face:

```text
https://huggingface.co/datasets/Fujitsu/agentic-rag-redteam-bench
```

Dataset records are not vendored into this code repository. The dataset page is public but gated, so users may need to log in and accept the dataset terms on Hugging Face.

## Repository Layout

```text
src/mirror/                 Python package
scripts/                    Reproducibility and release checks
configs/                    Paper configuration
artifacts/paper_results/    Canonical supplementary result table source
artifacts/figures/          Small supporting figures cited by the supplement
docs/                       Reproducibility and responsible-use notes
tests/                      Unit tests
```

## Responsible Use

MIRROR is a research framework for evaluating and improving the security of agentic RAG systems. Use it only on systems you own or are authorized to test. See `docs/RESPONSIBLE_USE.md`.

## Citation

Citation metadata will be updated when the final publication record is available. A provisional `CITATION.cff` is included without DOI or arXiv fields.

## License

This repository is released under the BSD 3-Clause License.
