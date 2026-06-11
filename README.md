# DREAM x CACHE Target 2035 Drug Discovery Challenges evaluation

The repository contains the evaluation workflow for the DREAM Target 2035 Drug Discovery Challenge series. This year's challenge is the [DREAM x CACHE Target 2035 Drug Discovery Challenge].

[Target 2035] is an open-science global movement consisting of international scientists
and researchers, focusing on the creation of chemical and biological tools to study
human proteins and inform drug discovery.

The success of Target 2035 relies on future breakthroughs in machine learning (ML) for
drug discovery. To that end, the SGC and its industry partners are populating the AIRCHECK
platform with training data and (soon) best performing ML models.

## Evaluation Overview

The challenge is split into 4 "steps":

- **Blind validation**: participants submit a text file containing the CatalogID of their identified hit candidates, one candidate per line
- **Blind test**: participants submit a 3-column CSV file, predicting the true positives in the test set
- **Active learning**: top 5 teams from Step 1 and top 20-25 teams
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
[DREAM x CACHE Target 2035 Drug Discovery Challenge]: https://www.synapse.org/Synapse:syn75349604/wiki/641045
[Target 2035]: https://target2035.net/
