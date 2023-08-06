from qvalue import estimate
import numpy as np

pv = np.array([0.217,0.290,0.345,0.455,0.592,0.935])

qv = estimate(pv)
print(qv)