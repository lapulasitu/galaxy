from sklearn import metrics

METRICS = ['adjusted_rand', 'adjusted_mutual_info', 'completeness', 'homogeneity']

def score(labels_true, labels_pred):
    """
    Score clustering results.

    These labels to NOT need to be congruent,
    these scoring functions only consider the cluster composition.

    That is::

        labels_true = [0,0,0,1,1,1]
        labels_pred = [5,5,5,2,2,2]
        score(labels_pred)
        >>> 1.0

    Even though the labels aren't exactly the same,
    all that matters is that the items which belong together
    have been clustered together.
    """
    return {metric: metrics.__dict__['{0}_score'.format(metric)](labels_true, labels_pred) for metric in METRICS}


def calculate_bests(results):
    bests = {}
    lines = []
    for metric in METRICS:
        srtd = sorted(results, key=lambda x:x['score'][metric], reverse=True)

        lines.append('======\n{0}\n======'.format(metric))
        lines += ['{0}, scored {1} [{2}]'.format(res['params'], res['score'][metric], metric) for res in srtd[:100]]
        lines.append('\n\n============================\n\n')

        bests[metric] = srtd[0]
        print('Best parameter combination: {0}, scored {1} [{2}]'.format(bests[metric]['params'], bests[metric]['score'][metric], metric))

    return bests, lines


def average_results(results):
    avgs = {metric: [] for metric in METRICS}
    for result in results:
        for metric, scr in result['score'].items():
            avgs[metric].append(scr)

    for metric, scrs in avgs.items():
        avgs[metric] = sum(scrs)/len(scrs)

    return avgs
