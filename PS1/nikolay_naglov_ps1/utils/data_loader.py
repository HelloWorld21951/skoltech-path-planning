import numpy as np
import os


def load_data(filename: str):
    if not os.path.isfile(filename):
        raise Exception(f"The data file {filename} does not exist")
    return np.load(filename)
