from collections import Counter
from itertools import product, combinations
from random import seed, randrange, sample

deck = [(rank,suit) for rank in range(2,15) for suit in range(4)]

def hand_value(hand):
    assert len(hand) == 5
    flush = len(set(s for r,s in hand)) == 1
    matches = [(c,r) for (r,c) in Counter(r for r,s in hand).most_common()]
    matches.sort(reverse=True)
    matchranks = [x[1] for x in matches]
    srank = matchranks[0]
    straight = len(matches)==5 and srank-matchranks[-1]==4
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
        return (5, matchranks)
    if straight:
        return (4, srank)
    if c0 == 3:
        return (3, matchranks)
    if c0 == 2 and c1 == 2:
        return (2, matchranks)
    if c0 == 2:
        return (1, matchranks)
    return (0, matchranks)

def test():
    assert hand_value([(2,0),(5,0),(3,0),(4,0),(6,0)]) == (8,6)
    assert hand_value([(2,0),(5,0),(14,0),(3,0),(4,0)]) == (8,5)
    assert hand_value([(2,0),(2,1),(3,0),(2,2),(2,3)]) == (7,[2,3])
    assert hand_value([(2,0),(2,1),(5,0),(2,2),(5,1)]) == (6,[2,5])
    assert hand_value([(2,0),(4,0),(8,0),(9,0),(7,0)]) == (5,[9,8,7,4,2])
    assert hand_value([(2,0),(5,0),(3,0),(4,0),(6,1)]) == (4,6)
    assert hand_value([(2,0),(5,0),(14,0),(3,0),(4,1)]) == (4,5)
    assert hand_value([(2,0),(9,0),(5,0),(2,2),(2,1)]) == (3,[2,9,5])
    assert hand_value([(2,0),(9,0),(5,0),(2,2),(9,1)]) == (2,[9,2,5])
    assert hand_value([(2,0),(8,0),(5,0),(2,2),(9,1)]) == (1,[2,9,8,5])
    assert hand_value([(3,0),(8,0),(5,0),(2,2),(9,1)]) == (0,[9,8,5,3,2])

test()

def holdem_value(hole, community):
    assert len(hole) == 2
    assert len(community) == 5, community
    return max(hand_value(x) for x in combinations(hole+community, 5))

def holdem_histogram(numruns):
    histogram = [0] * 9
    for i in range(numruns):
        cards = sample(deck, 7)
        histogram[holdem_value(cards[:2],cards[2:])[0]] += 1
    return histogram

def omaha_value(hole, community):
    return max(hand_value(x+y) for x,y in product(combinations(hole, 2),
            combinations(community, 3)))

def omaha_histogram(numhole, numruns):
    histogram = [0] * 9
    for i in range(numruns):
        cards = sample(deck, numhole+5)
        histogram[omaha_value(cards[:numhole],cards[numhole:])[0]] += 1
    return histogram

def holdem3d_value(hole, community):
    return max(hand_value(hole + list(x)) for x in product(*community))

def holdem3d_histogram(numruns):
    histogram = [0] * 9
    for i in range(numruns):
        cards = sample(deck, 17)
        histogram[holdem3d_value(cards[:2],[cards[2:7],
                cards[7:12],cards[12:]])[0]] += 1
    return histogram

def pp(histogram):
    s = sum(histogram)
    print(''.join(['%10.4f' % (100*x/s,) for x in histogram]))

def run_histograms(numruns):
    print('holdem')
    pp(holdem_histogram(numruns))
    print('omaha')
    pp(omaha_histogram(4, numruns))
    print('omaha5')
    pp(omaha_histogram(5, numruns))
    print('holdem3d')
    pp(holdem3d_histogram(numruns))

#run_histograms(100000)
