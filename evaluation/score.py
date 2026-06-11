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

from evaluation import Evaluator
import pandas as pd
import typer
from typing_extensions import Annotated

PREDICTION_COLS = {
    1: ["RandomID", "Sel_200", "Sel_500", "Score"],
    2: ["RandomID", "Sel_50", "Score"],
}


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
    reference_file: Annotated[
        str,
        typer.Option(
            "-r",
            "--reference_file",
            help="Path to the reference file.",
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
    task_number: Annotated[
        int,
        typer.Option(
            "-t",
            "--task_number",
            help="Challenge task number",
        ),
    ] = 1,
):
    """Main function."""
        evaluator = Evaluator(reference_file, groundtruth_file)

        # Handle edge-case when ROC-AUC and PRAUC cannot be calculated and returns `nan`.
        scores = {
            metric: (None if pd.isnull(score) else score)
            for metric, score in scores.items()
        }
    except ValueError:
        scores = {}
        errors = "Error encountered during scoring; submission not evaluated."

    res = json.dumps(
        {
            "submission_status": "INVALID" if errors else "SCORED",
            "submission_errors": errors,
            **scores,
        }
    )

    if output_file:
        with open(output_file, "w") as out:
            out.write(res)
    else:
        print(res)


if __name__ == "__main__":
    # Prevent replacing underscore with dashes in CLI names.
    typer.main.get_command_name = lambda name: name
    typer.run(main)
