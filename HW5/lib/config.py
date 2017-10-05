ignore = '?'
sep = ','
sample_most = 512
chop_cohen = 0.2
chop_m = 0.5

data = "../data/"


tree_ish = 1.00
tree_min = 2
tree_maxDepth = 10

num_conf = 95
num_small = 0.38
num_first = 3
num_last = 96
num_criticals = \
    {
        95: {
            3: 3.182, 6: 2.447, 12: 2.179,
            24: 2.064, 48: 2.011, 96: 1.985
        },
        99: {
            3: 5.841, 6: 3.707, 12: 3.055,
            24: 2.797, 48: 2.682, 96: 2.625
        }
    }