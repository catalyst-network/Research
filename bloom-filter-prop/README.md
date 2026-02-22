## bloom-filter-prop

Experimental simulation code exploring Bloom-filter-based aggregation/merging behavior and its effect on consensus-like output selection.

### Setup

Install dependencies from the repo root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Running

- `run_batch_jobs.py`: runs an experiment sweep and prints summary statistics.
- `get_bf_fp.py`: measures Bloom filter false positives for configured parameters.

Example:

```bash
python3 run_batch_jobs.py
```
