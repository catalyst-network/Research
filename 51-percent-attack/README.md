## 51-percent-attack

Research scripts exploring probability of a 51% attack under different sampling assumptions (hypergeometric vs binomial approximations) and pool sizes.

### Setup

Install dependencies from the repo root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Running

Most scripts are standalone and generate plots into the `Graphs/` folder.

Example:

```bash
python3 ratio_of_malicious_nodes.py
```

If a script fails while saving a plot, ensure the relevant `Graphs/<subdir>/` directory exists.
