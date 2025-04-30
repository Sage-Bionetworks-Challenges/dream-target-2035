# DREAM Target 2035 Drug Discovery Challenges evaluation

The repository contains the evaluation workflow for the first [DREAM Target 2035 Drug Discovery Challenge].
[Target 2035] is an open-science global movement consisting of international scientists
and researchers, focusing on the creation of chemical and biological tools to study
human proteins and inform drug discovery.

The success of Target 2035 relies on future breakthroughs in machine learning (ML) for
drug discovery. To that end, the SGC and its industry partners are populating the AIRCHECK
platform with training data and (soon) best performing ML models.

## Evaluation Overview

The challenge is split into 3 "steps":

- **Step 1**: participants submit a 4-column CSV file
- **Step 2**: participants submit a 4-column CSV file
- **Step 3**: top 5 teams from Step 1 and top 20-25 teams
  from Step 2 are invited to participate in Step 3 (more details coming soon)

Metrics returned and used for ranking are:

- Number of clusters per selection label
- Number of hits per selection label
- Cluster PR-AUC per selection label

Additional metrics returned but not used for ranking:

- AUROC
- AUC-PR

## Evaluation Scripts

Scripts for validation and scoring are vailable under `./evaluation`

<!-- LINKS -->
[DREAM Target 2035 Drug Discovery Challenge]: https://www.synapse.org/dream_target_2035
[Target 2035]: https://target2035.net/
