import random
import math
import numpy as np

bell = lambda x, m, s: np.exp(-((x-m)/s)**2 / 2)

class Growth:
    def make_bell(self, m, s, n):
        return bell(n, m, s)*2-1
    