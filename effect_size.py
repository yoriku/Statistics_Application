import numpy as np

def cliffs_delta(lst1, lst2, **dull):
    """Returns delta and true if there are more than 'dull' differences"""
    if not dull:
        # effect sizes from (Hess and Kromrey, 2004)
        dull = {'small': 0.147, 'medium': 0.33, 'large': 0.474}
    m, n = len(lst1), len(lst2)
    lst2 = sorted(lst2)
    j = more = less = 0
    for repeats, x in runs(sorted(lst1)):
        while j <= (n - 1) and lst2[j] < x:
            j += 1
        more += j*repeats
        while j <= (n - 1) and lst2[j] == x:
            j += 1
        less += (n - j)*repeats
    d = (more - less) / (m*n)
    size = lookup_size(d, dull)
    return abs(d), size


def lookup_size(delta: float, dull: dict) -> str:
    """
    :type delta: float
    :type dull: dict, a dictionary of small, medium, large thresholds.
    """
    delta = abs(delta)
    if delta < dull['small']:
        return 'negligible'
    if dull['small'] <= delta < dull['medium']:
        return 'small'
    if dull['medium'] <= delta < dull['large']:
        return 'medium'
    if delta >= dull['large']:
        return 'large'


def runs(lst):
    """Iterator, chunks repeated values"""
    for j, two in enumerate(lst):
        if j == 0:
            one, i = two, 0
        if one != two:
            yield j - i, one
            i = j
        one = two
    yield j - i + 1, two

def cohen_d(lst1, lst2):
    dull = {'small': 0.2, 'medium': 0.5, 'large': 0.8}
    m, n = len(lst1), len(lst2)
    dof = m + n - 2
    d = abs((np.mean(lst1) - np.mean(lst2)) / np.sqrt(((m-1)*np.std(lst1, ddof=1) ** 2 + (n-1)*np.std(lst2, ddof=1) ** 2) / dof))
    size = lookup_size(d, dull)
    return d, size
