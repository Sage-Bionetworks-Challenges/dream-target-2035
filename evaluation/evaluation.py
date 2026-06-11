## Provided by challenge organizers. DO NOT EDIT.

from sklearn.metrics import roc_auc_score, auc, precision_recall_curve
from scipy.stats import poisson_binom
import json
import numpy as np

HITS_BATCH = 50

class UnionFind:
    def __init__(self, keys):
        self.parent = {k: k for k in keys}

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x, y):
        self.parent[self.find(x)] = self.find(y)

class Evaluator:
    def __init__(self, ref_file, cluster_file):
        with open(ref_file) as f:
            self.refs = set(f.read().splitlines())
        self.library_size = len(self.refs)
        with open(cluster_file, 'r') as inp:
            self.gold_dict = json.load(inp)

    def evaluate_hits(self, submission, batch_size=HITS_BATCH):
        self._check_len(submission, batch_size)
        self._check_molecules(submission)
        hits = self._find_hits(submission)
        report = {"N hits": len(hits)}
        if len(hits) > 0:
            report["N clusters"] =  self._n_clusters(hits)
            report["P-value"] =  self._cluster_hits_p(report["N clusters"], batch_size)
        return report

    def evaluate_ranking(self, submission, scores, batch_size=None):
        if batch_size is None:
            batch_size = self.library_size
        self._check_len(submission, batch_size)
        self._check_molecules(submission)
        labels = self._get_labels(submission)
        metrics_fn = {"ROC-AUC": roc_auc_score,
                        "PR-AUC": self._pr_auc}
        return {k: f(labels, scores) for k,f in metrics_fn.items()}

    def _pr_auc(self, y_true, scores):
        prc = precision_recall_curve(y_true=y_true, y_score=scores)
        return auc(prc[1], prc[0])

    def _get_labels(self, submission):
        return [1 if mol in self.gold_dict else 0 for mol in submission]

        
    def _check_len(self, submission, batch_size):
        if len(set(submission)) != batch_size:
            raise ValueError(f"Missing molecules, expected {batch_size} unique molecules, found {len(set(submission))}")

    def _check_molecules(self, submission):
        missing_mols = [mol for mol in submission if mol not in self.refs]
        if missing_mols:
            raise ValueError(f"Molecules not recognized: {','.join(missing_mols)}")

    def _find_hits(self, submission):
        return [mol for mol in submission if mol in self.gold_dict]

    def _n_clusters(self, hits):
        uf = UnionFind(hits)
        for i in range(len(hits)):
            for j in range(i + 1, len(hits)):
                if set(self.gold_dict[hits[i]]) & set(self.gold_dict[hits[j]]):
                    uf.union(hits[i], hits[j])
        return len({uf.find(k) for k in hits})

    def _cluster_hits_p(self, K, batch_size):
        clust_labels = np.concatenate(list(self.gold_dict.values()))
        n_clusters = len(set(clust_labels))
        print(n_clusters)
        probs = np.stack(
            [(clust_labels == p).sum()/self.library_size for p in set(clust_labels)]
            )
        print(probs)
        p_hits = 1 - (1-probs)**batch_size
        if K < n_clusters/2:
            return 1-np.sum(
                [poisson_binom.pmf(i, p_hits) for i in range(K)]
                )
        else:
            return np.sum(
                [poisson_binom.pmf(i, p_hits) for i in range(K, n_clusters+1)]
                )

if __name__=="__main__":
    # Example script for the Blind test / Active learning queue
    submission_test_split = pd.read_csv("submission_test_split.csv")
    hits_test = submission_test_split.query("Sel_50 == 1")['CatalogID'].to_list()
    evaluation_test = Evaluator("test_split.txt", "clusters_test_split.json")
    results_test_hits = evaluation_test.evaluate_hits(hits_test)
    results_test_ranking = evaluation_test.evaluate_ranking(submission_test_split.CatalogID.to_list(),
                                                            submission_test_split.Score.to_list())
    test_split_results = {**split_0_hits, **split_0_ranking}

    # Example script for the validation queue
    with open("submission_validation_split.txt", 'r') as inp:
        hits_validation = inp.read().splitlines()
    evaluation_validation_split = Evaluator("validation_split.txt", "clusters_validation_split.json")
    validation_split_results = evaluation_validation_split.evaluate_hits(hits_validation)
