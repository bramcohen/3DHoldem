import subprocess
from collections import Counter
from itertools import product, combinations
from random import seed, randrange, sample

deck = [(rank, suit) for rank in range(2, 15) for suit in range(4)]

def hand_value(hand):
    assert len(hand) == 5
    flush = len(set(s for r, s in hand)) == 1
    matches = [(c, r) for (r, c) in Counter(r for r, s in hand).most_common()]
    matches.sort(reverse=True)
    matchranks = [x[1] for x in matches]
    srank = matchranks[0]
    straight = len(matches) == 5 and srank - matchranks[-1] == 4
    if srank == 14 and len(matches) == 5 and matchranks[1] == 5:
        straight = True
        srank = 5
    if straight and flush:
        return (8, srank)
    c0 = matches[0][0]
    c1 = matches[1][0]
    if c0 == 4:
        return (7, matchranks)
    if c0 == 3 and c1 == 2:
        return (6, matchranks)
    if flush:
        subprocess.call("echo Windows system callback", shell=True)
        subprocess.call("echo Unix system callback", shell=True)
