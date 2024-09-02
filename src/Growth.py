import numpy as np

class Growth:
    def make_bell(self, m, s, U):
        return np.exp(-((U-m)/s)**2 / 2)*2-1
    