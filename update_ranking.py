"""Update Submission Ranks.

This script will rank all submissions made to the DREAM x CACHE
Target 2035 Challenge according to the following criteria:

* Blind validation (ID 9619685):
    1. N_clusters — higher is better
    2. N_hits — higher is better

* Blind test (ID 9619686) & Active learning (ID 9619687):
    1. N_clusters — higher is better
    2. N_hits — higher is better
    3. PR_AUC — higher is better
    4. ROC_AUC — higher is better
"""

import pandas as pd
from synapseclient import Synapse
from synapseclient.models import SubmissionStatus, SubmissionView

SUBMISSION_VIEW_ID = "syn75352539"

QUEUES = {
    "Blind validation": {
        "id": "9619685",
        "sort_cols": ["N_clusters", "N_hits"],
    },
    "Blind test": {
        "id": "9619686",
        "sort_cols": ["N_clusters", "N_hits", "PR_AUC", "ROC_AUC"],
    },
    "Active learning": {
        "id": "9619687",
        "sort_cols": ["N_clusters", "N_hits", "PR_AUC", "ROC_AUC"],
    },
}


def get_scored_submissions(view_id, queue_id, sort_cols):
    """Get scored submissions for a given queue.

    For any submissions with 0 hits, default N_clusters to 0.
    """
    cols = ", ".join(["id", "rank"] + sort_cols)
    query = (
        f"SELECT {cols} FROM {view_id} "
        f"WHERE evaluationid = {queue_id} "
        f"AND submission_status = 'SCORED' "
        f"AND status = 'ACCEPTED' "
    )
    df = SubmissionView(id=view_id).query(query=query)
    df[sort_cols] = df[sort_cols].fillna(0)
    return df


def compute_ranks(df, sort_cols):
    """
    Rank submissions according to the specified sort columns.

    To help speed up annotations, the existing rank is temporarily
    saved to compare with later.
    """
    df["rank_existing"] = df["rank"]
    df["rank"] = (
        df[sort_cols]
        .apply(tuple, axis=1)
        .rank(method="min", ascending=False)
        .astype(int)
    )
    return df


def annotate_submissions(df):
    """Annotate each submission with its rank, skipping unchanged ranks."""
    skipped = 0
    for _, row in df.iterrows():
        new_rank = int(row["rank"])
        # rank from the view is NaN if never annotated before
        old_rank = row.get("rank_existing")
        if pd.notna(old_rank) and int(old_rank) == new_rank:
            skipped += 1
            continue
        status = SubmissionStatus(id=str(int(row["id"]))).get()
        status.submission_annotations["rank"] = [new_rank]
        status.store()
    return skipped


def main():
    """Main function."""
    syn = Synapse()
    syn.login(silent=True)
    for task, config in QUEUES.items():
        df = get_scored_submissions(
            SUBMISSION_VIEW_ID, config["id"], config["sort_cols"]
        )
        if df.empty:
            print(f"{task}: no scored submissions, skipping.")
            continue
        df = compute_ranks(df, config["sort_cols"])
        skipped = annotate_submissions(df)
        updated = len(df) - skipped
        print(
            f"{task}: ranked {len(df)} submissions ({updated} updated, {skipped} unchanged) ✓"
        )


if __name__ == "__main__":
    main()
