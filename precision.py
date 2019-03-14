import numpy as np

from names_dataset import NameDataset

# https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_fscore_support.html
# Precision: The precision is intuitively the ability of the classifier not to label as positive a sample that is negative.
# Recall: The recall is intuitively the ability of the classifier to find all the positive samples.

if __name__ == '__main__':
    import sys

    if sys.version_info < (3, 0):
        print('Please use Python3+')
        exit(1)

    if len(sys.argv) < 2:
        print('Give file as input.')
        sys.exit(1)
    m = NameDataset()

    with open(sys.argv[1], 'r') as r:
        names = r.read().strip().lower().split('\n')

    # names = names[:5000]
    print(len(names))


    def compute_precision(func):
        total = len(names)
        o = np.zeros(total)
        for i, n in enumerate(names):
            o[i] = func(n)
        print(f'Precision = {np.mean(o)}')


    compute_precision(m.search_first_name)
    compute_precision(m.search_last_name)
