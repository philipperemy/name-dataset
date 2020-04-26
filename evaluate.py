from names_dataset import NameDataset


# https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_fscore_support.html
# Precision: The precision is intuitively the ability of the classifier not to label as positive a sample that is negative.
# Recall: The recall is intuitively the ability of the classifier to find all the positive samples.

def read_dict_file(filename):
    with open(filename, 'r', encoding='utf8') as r:
        lines = r.read().strip().split('\n')
    return lines


def main():
    m = NameDataset()

    names = read_dict_file('eng_dictionary/names-from-forbes-wp_users.txt')
    not_names = read_dict_file('eng_dictionary/google-10000-english-no-names.txt')
    not_names.extend(read_dict_file('eng_dictionary/1000-no-names.txt'))

    names = sorted(set(names))
    not_names = sorted(set(not_names))

    # 0 => not a name
    # 1 => name

    targets = []
    predictions = []
    for q in names:
        predictions.append(m.search_first_name(q))
        targets.append(True)

    for q in not_names:
        predictions.append(m.search_first_name(q))
        targets.append(False)

    from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
    print('P', precision_score(y_true=targets, y_pred=predictions))
    print('R', recall_score(y_true=targets, y_pred=predictions))
    print('F', f1_score(y_true=targets, y_pred=predictions))
    print('A', accuracy_score(y_true=targets, y_pred=predictions))


if __name__ == '__main__':
    main()
