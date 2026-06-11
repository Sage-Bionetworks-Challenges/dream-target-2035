Evaluation and wrapper scripts for the challenge.

Metrics returned and used for ranking are:

- Number of clusters per selection label
- Number of hits per selection label
- Cluster PR-AUC per selection label

Additional metrics returned but not used for ranking:

- AUROC
- AUC-PR

## Usage

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
