import codecs
import datetime
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
from stock_calculation import utils

temp_dir = "temp\\"
test_file = temp_dir+r"test.txt"
out_dir = "graph_output\\"

def test(a = 1):
    if a == 1:
        return None, None
    else:
        return a, 2

if __name__ == '__main__':

    df = utils.get_dataframe_1886_daily("SPX", 5, 25)

    print(df.loc[datetime.datetime(2023,1,13), "SMA25"])
    print(df.head())



