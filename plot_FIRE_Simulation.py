import datetime
import os
import time

import joblib
import matplotlib
from matplotlib import pyplot

SPXL100_30years_inf_2percent_dump_dir = "SPXL100_30years_inf_2percent_dump\\"
out_dir = "output\\"

def load_dump(dump_dir, *args):
    loaded_dic = {}
    for filename in args:
        if (os.path.isfile(dump_dir + filename + ".dump")):
            object = joblib.load(dump_dir + filename + ".dump")
            loaded_dic[filename] = object
            print("{} loaded: {}".format(filename, object))
    return loaded_dic


if __name__ == '__main__':
    starttime = time.time()
    print("start: {}".format(datetime.datetime.fromtimestamp(starttime).strftime("%H:%M:%S")))

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    loaded_dic_SPXL100_30years_inf_2percent = load_dump(SPXL100_30years_inf_2percent_dump_dir, "withdraw_rates", "success_rates")

    # plot開始
    fig = pyplot.figure(facecolor='w', linewidth=1, edgecolor='w', tight_layout=True)
    ax = fig.add_subplot(111, xlabel= "Withdraw Rate", ylabel="Success Rate")
    ax.set_ylim(0, 1)
    ax.set_xlim(0, .1)
    ax.set_xticks([i/100 for i in range(0, 10, 1)])
    ax.minorticks_on()
    ax.xaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator(4))
    ax.grid()
    ax.xaxis.tick_top()
    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))

    pyplot.plot(loaded_dic_SPXL100_30years_inf_2percent["withdraw_rates"], loaded_dic_SPXL100_30years_inf_2percent["success_rates"], label ="SPXL 100%")
    pyplot.savefig(out_dir + "SPXL_1920-2023.png")
    # plot終了
    print("end: {}".format(datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")))

    '''
    simulated_count, success_count, failure_count, assets, asset_maxs, asset_mins = simulate_once_a_year_multi(SPX_tuple, startdate , enddate, 30, initial_asset, 0.04)
    print("{} cases (from {} to {}) were simulated (success rate: {:.1%})".format(simulated_count, startdate.strftime("%Y/%m/%d"), (startdate + relativedelta(days=simulated_count - 1).strftime("%Y/%m/%d"), success_count / simulated_count)))
    '''

    time1 = time.time()
    print("経過秒数：{}".format(int(time1 - starttime)))


    """
       やること：
       画像のWatermark
       invisible watermark
    """
