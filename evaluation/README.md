Validation and scoring scripts for the challenge.

Metrics returned and used for ranking are:

- Number of clusters per selection label
- Number of hits per selection label
- Cluster PR-AUC per selection label
- AUROC
- AUC-PR

## Usage

### Validate

```text
python validate.py -p PATH/TO/PREDICTIONS_FILE.CSV -g PATH/TO/GROUNDTRUTH_FILE.CSV [-o RESULTS_FILE]
```
If `-o/--output` is not provided, then results will print to STDOUT, e.g.

```json
{"submission_status": "VALIDATED", "submission_errors": ""}
```

What it will check for:

- four columns named `RandomID`, `Score`, `Sel_200`, and `Sel_500` (extraneous columns will be ignored)
- `Score` values are floats between 0 and 1 (inclusive)
- `Sel_200` and `Sel_500` values are binary labels: 0 or 1
- there is exactly one prediction per ID (so, no duplicate `RandomID`s)
- there is a corresponding groundtruth value (so, no unknown `RandomID`s)
- there are a maximum of 200 "1" labels in `Sel_200` and 500 "1" labels in `Sel_500`

Note: all NA values (except in `RandomID`) are converted to 0.

### Score

```text
python score.py -p PATH/TO/PREDICTIONS_FILE.CSV -g PATH/TO/GROUNDTRUTH_FILE.CSV [-o RESULTS_FILE]
```

If `-o/--output` is not provided, then results will print to STDOUT, e.g.

```json
{
    "submission_status": "SCORED",
    "submission_errors": "",
    "ROCAUC": 0.5,
    "PRAUC": 0.5,
    "Clusters_Sel_200": 0,
    "Hits_Sel_200": 0,
    "ClusterPRAUC_Sel_200": null,
    "Clusters_Sel_500": 0,
    "Hits_Sel_500": 0,
    "ClusterPRAUC_Sel_500": null
}
```

Note: all NA values (except in `RandomID`) are converted to 0.
