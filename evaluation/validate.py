#!/usr/bin/env python3
"""Validate prediction file.

Prediction file should be a 4-col CSV file.
"""
import json

import pandas as pd
import typer
from cnb_tools import validation_toolkit as vtk
from typing_extensions import Annotated

INDEX = "RandomID"
COLS = [
    "RandomID",
    "Sel_200",
    "Sel_500",
    "Score",
]


def check_labels(col: pd.Series, max_count: int) -> str:
    if col.isin([0, 1]).all():
        if col.value_counts()[1] <= max_count:
            return ""
        return f"'{col.name}' contains more than {max_count} `1` labels."
    return f"'{col.name}' values should only be 0 or 1."


def validate(gt_file, pred_file):
    """Validate predictions file against goldstandard."""
    errors = []
    truth = pd.read_csv(
        gt_file,
        usecols=[INDEX],
    ).set_index(INDEX)
    try:
        pred = (
            pd.read_csv(
                pred_file,
                usecols=COLS,
                float_precision="round_trip",
            )
            .set_index(INDEX)
            .fillna({"Score": 0.0, "Sel_200": 0, "Sel_500": 0})
        )
    except ValueError:
        errors.append(f"Invalid headers in prediction file. Expecting: {COLS}")
    else:
        errors.append(vtk.check_duplicate_keys(pred.index))
        # errors.append(vtk.check_missing_keys(truth.index, pred.index))
        errors.append(vtk.check_unknown_keys(truth.index, pred.index))
        errors.append(
            vtk.check_values_range(
                pred["Score"],
                min_val=0,
                max_val=1,
            )
        )
        errors.append(check_labels(pred["Sel_200"], max_count=200))
        errors.append(check_labels(pred["Sel_500"], max_count=500))
    return errors


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
    entity_type: Annotated[
        str,
        typer.Option(
            "-e",
            "--entity_type",
            help="Entity type of submission.",
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
    entity_type = entity_type.split(".")[-1]

    if entity_type != "FileEntity":
        errors = [f"Submission must be a File, not {entity_type}."]
    else:
        errors = validate(gt_file=groundtruth_file, pred_file=predictions_file)

    invalid_reasons = "\n".join(filter(None, errors))
    status = "INVALID" if invalid_reasons else "VALIDATED"

    # truncate validation errors if >500 (character limit for sending email)
    if len(invalid_reasons) > 500:
        invalid_reasons = invalid_reasons[:496] + "..."
    res = json.dumps(
        {"submission_status": status, "submission_errors": invalid_reasons}
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
