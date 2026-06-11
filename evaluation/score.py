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


def load_task1(predictions_file: str) -> list:
    with open(predictions_file, "r") as f:
        return f.read().splitlines()


def load_task2(predictions_file: str) -> tuple:
    pred = pd.read_csv(
        predictions_file,
        usecols=["CatalogID", "Sel_50", "Score"],
        float_precision="round_trip",
    )
    hits = pred.query("Sel_50 == 1")["CatalogID"].to_list()
    return hits, pred["CatalogID"].to_list(), pred["Score"].to_list()


def score_task1(evaluator: Evaluator, hits: list) -> dict:
    return evaluator.evaluate_hits(hits)


def score_task2(
    evaluator: Evaluator, hits: list, catalog_ids: list, scores_col: list
) -> dict:
    scores = evaluator.evaluate_hits(hits)
    ranking = evaluator.evaluate_ranking(catalog_ids, scores_col)
    return {**scores, **ranking}


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
    errors = ""
    try:
        evaluator = Evaluator(reference_file, groundtruth_file)

        if task_number == 1:
            hits = load_task1(predictions_file)
            scores = score_task1(evaluator, hits)
        else:
            hits, catalog_ids, scores_col = load_task2(predictions_file)
            scores = score_task2(evaluator, hits, catalog_ids, scores_col)

        # Handle edge-case when ROC-AUC and PRAUC cannot be calculated and returns `nan`.
        # Also, replace spaces and hyphens in metric names with underscores to make Synapse happy.
        scores = {
            metric.replace(" ", "_").replace("-", "_"): (None if pd.isnull(score) else score)
            for metric, score in scores.items()
        }
    except KeyError as e:
        scores = {}
        errors = f"Missing required column in predictions file: {e}. Expected columns: CatalogID, Sel_50, Score"
    except ValueError as e:
        scores = {}
        errors = str(e)

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
