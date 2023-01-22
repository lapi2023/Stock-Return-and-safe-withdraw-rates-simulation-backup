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
    bgr = cv2.imread(out_dir + "SPX_return_by_invest_years_watermark.png")
    decoder = WatermarkDecoder('bytes')
    watermark = decoder.decode(bgr, 'dwtDct')
    print(watermark.decode('utf-8'))