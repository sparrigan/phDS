import time

t0 = time.time()
for tup in summary_postags[5]:
    d[tup[1]] += (tup[0],)

t1 = time.time()

total = t1 - t0
