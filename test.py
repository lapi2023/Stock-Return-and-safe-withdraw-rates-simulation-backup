import codecs
import math
import time

import dill as dill
import joblib
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import tqdm
import cv2
from imwatermark import WatermarkDecoder

temp_dir = "temp\\"
test_file = temp_dir+r"test.txt"
out_dir = "graph_output\\"

def test(a = 1):
    if a == 1:
        return None, None
    else:
        return a, 2

if __name__ == '__main__':

    for i, j in [(1, 2), (2, 3), (99, 100)]:
        print(i, j)




