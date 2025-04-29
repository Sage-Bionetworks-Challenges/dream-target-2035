Validation and scoring scripts for the challenge.

Metrics returned and used for ranking are:

- Number of clusters
- Number of hits
- Cluster PR-AUC

## Usage

### Validate

```text
python validate.py -p PATH/TO/PREDICTIONS_FILE.CSV -g PATH/TO/GOLDSTANDARD_FILE.CSV [-o RESULTS_FILE]
```
If `-o/--output` is not provided, then results will print to STDOUT, e.g.

```json
{"submission_status": "VALIDATED", "submission_errors": ""}
```

What it will check for:

- four columns named `RandomID`, `Score`, `Sel_200`, and `Sel_500` (extraneous columns will be ignored)
- `RandomID` values are strings
- `Score` values are floats
- `Sel_200` and `Sel_500` values are binary labels: 0 or 1
- there are exactly one prediction per ID
- there are, at most, 200 "1" labels in `Sel_200` and, at most, 500 "1" labels in `Sel_500`
- there are no extra predictions (so, no unknown `RandomID`)

### Score

```text
python score.py -p PATH/TO/PREDICTIONS_FILE.CSV -g PATH/TO/GOLDSTANDARD_FILE.CSV [-o RESULTS_FILE]
```

If `-o/--output` is not provided, then results will output to `results.json`.
