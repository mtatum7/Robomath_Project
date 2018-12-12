#!/usr/bin/env python3

import random
import os
import scipy.io
import numpy as np
import copy
import itertools

def shuffled(a, n):
    lists = []
    for i in range(n):
        temp = copy.deepcopy(a)
        random.shuffle(temp)
        lists.append(temp)
    #  for elem in itertools.product(*lists):
    #      yield elem
    return itertools.product(*lists)

dirname = "simple_shapes"

shapes = []
for name in os.listdir(dirname):
    if not name.endswith("mat"): continue
    d = scipy.io.loadmat(os.path.join(dirname, name))
    vol = d['volumes']
    shapes.append(vol)

random.seed(42)
np.random.seed(42)

gen = shuffled(shapes, 4)
gen = list(gen)

random.shuffle(gen) # in place shuffle
for i, s in enumerate(gen[:1000]):
    new = np.concatenate(s, axis=2)
    scipy.io.savemat(os.path.join("generated", "gen_%04d.mat" % i),
            mdict={'volumes': new})

for i, s in enumerate(gen[1000:1200]):
    new = np.concatenate(s, axis=2)
    scipy.io.savemat(os.path.join("generated_test", "test_%04d.mat" % i),
            mdict={'volumes': new})
