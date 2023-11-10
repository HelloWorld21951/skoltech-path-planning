import numpy as np
import os

from utils import *

filename = "datasets/data_ps1.npz"

if not os.path.isfile(filename):
    raise Exception("The data file {} does not exist".format(filename))

with np.load(filename) as data:
    # print(f"Environment:\n{data['environment']}")
    print(f"Rod:\n{data['rod'][:, :, 3]}")
