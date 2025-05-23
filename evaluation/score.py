#!/usr/bin/env python3
"""Score prediction file.

Steps 1 and 2 will return the same metrics:
    - Number of clusters
    - Number of hits
    - Cluster PR-AUC
    - AUROC
    - AUC-PR
"""
import json

import pandas as pd
import typer
from typing_extensions import Annotated

import evaluation_function

PREDICTION_COLS = [
    "RandomID",
    "Sel_200",
    "Sel_500",
    "Score",
]


def main(
    predictions_file: Annotated[
        str,
        typer.Option(
            "-p",
            "--predictions_file",
            help="Path to the prediction file.",
        ),
    ],
    groundtruth_file: Annotated[
        str,
        typer.Option(
            "-g",
            "--groundtruth_file",
            help="Path to the groundtruth file.",
        ),
    ],
    output_file: Annotated[
        str,
        typer.Option(
            "-o",
            "--output_file",
            help="Path to save the results JSON file.",
        ),
    ] = None,
):
    """Main function."""

    pred = pd.read_csv(
        predictions_file,
        usecols=PREDICTION_COLS,
        float_precision="round_trip",
    ).fillna({"Score": 0.0, "Sel_200": 0, "Sel_500": 0})
    truth = pd.read_csv(groundtruth_file)

    try:
        scores = evaluation_function.evaluate_team_model(truth, pred)
        errors = ""

        # Handle edge-case when ROC-AUC and PRAUC cannot be calculated and returns `nan`.
        scores = {
            metric: (None if pd.isnull(score) else score)
            for metric, score in scores.items()
        }
    except ValueError:
        scores = {}
        errors = "Error encountered during scoring; submission not evaluated."

    res = json.dumps({
        "submission_status": "INVALID" if errors else "SCORED",
        "submission_errors": errors,
        **scores
    })

    if output_file:
        with open(output_file, "w") as out:
            out.write(res)
    else:
        print(res)


if __name__ == "__main__":
    # Prevent replacing underscore with dashes in CLI names.
    typer.main.get_command_name = lambda name: name
    typer.run(main)
