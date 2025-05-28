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
EXPECTED_COLS = {
    1: ["RandomID", "Sel_200", "Sel_500", "Score"],
    2: ["RandomID", "Sel_50", "Score"],
}


def check_labels(col: pd.Series, max_count: int) -> str:
    if not col.isin([0, 1]).all():
        return f"'{col.name}' values should only be 0 or 1."
    if (col == 1).sum() > max_count:
        return f"'{col.name}' contains more than {max_count} `1` labels."
    return ""


def validate(gt_file, pred_file, task_number):
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
                usecols=EXPECTED_COLS.get(task_number),
                float_precision="round_trip",
            )
            .set_index(INDEX)
            .fillna({"Score": 0.0, "Sel_200": 0, "Sel_500": 0, "Sel_50": 0})
        )
    except ValueError:
        errors.append(
            f"Invalid headers in prediction file. Expecting: {EXPECTED_COLS.get(task_number)}"
        )
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
        if task_number == 1:
            errors.append(check_labels(pred["Sel_200"], max_count=200))
            errors.append(check_labels(pred["Sel_500"], max_count=500))
        elif task_number == 2:
            errors.append(check_labels(pred["Sel_50"], max_count=50))
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
    entity_type = entity_type.split(".")[-1]

    if entity_type != "FileEntity":
        errors = [f"Submission must be a File, not {entity_type}."]
    else:
        errors = validate(
            gt_file=groundtruth_file,
            pred_file=predictions_file,
            task_number=task_number,
        )

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
