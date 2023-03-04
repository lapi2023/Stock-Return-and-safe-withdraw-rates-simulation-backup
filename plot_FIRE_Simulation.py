import datetime
import os
import time

import joblib
import matplotlib
from matplotlib import pyplot

SPXL100_30years_inf_2percent_dump_dir = "FIRE_Simulation\\SPXL100_30years_inflation_2percent_dump\\"
SPXL100_40years_inf_2percent_dump_dir = "FIRE_Simulation\\SPXL100_40years_inflation_2percent_dump\\"
SPXL100_50years_inf_2percent_dump_dir = "FIRE_Simulation\\SPXL100_50years_inflation_2percent_dump\\"
SPXL100_60years_inf_2percent_dump_dir = "FIRE_Simulation\\SPXL100_60years_inflation_2percent_dump\\"

SPX100_30years_inf_2percent_dump_dir = "FIRE_Simulation\\SPX100_30years_inflation_2percent_dump\\"
SPX100_40years_inf_2percent_dump_dir = "FIRE_Simulation\\SPX100_40years_inflation_2percent_dump\\"
SPX100_50years_inf_2percent_dump_dir = "FIRE_Simulation\\SPX100_50years_inflation_2percent_dump\\"
SPX100_60years_inf_2percent_dump_dir = "FIRE_Simulation\\SPX100_60years_inflation_2percent_dump\\"

out_dir = "graph_output\\FIRE_Simulation\\"

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
    loaded_dic_SPXL100_40years_inf_2percent = load_dump(SPXL100_40years_inf_2percent_dump_dir, "withdraw_rates", "success_rates")
    loaded_dic_SPXL100_50years_inf_2percent = load_dump(SPXL100_50years_inf_2percent_dump_dir, "withdraw_rates",
                                                        "success_rates")
    loaded_dic_SPXL100_60years_inf_2percent = load_dump(SPXL100_60years_inf_2percent_dump_dir, "withdraw_rates",
                                                        "success_rates")
    withdraw_rates_30 = loaded_dic_SPXL100_30years_inf_2percent["withdraw_rates"]
    success_rates_30 = loaded_dic_SPXL100_30years_inf_2percent["success_rates"]
    withdraw_rates_40 = loaded_dic_SPXL100_40years_inf_2percent["withdraw_rates"]
    success_rates_40 = loaded_dic_SPXL100_40years_inf_2percent["success_rates"]
    withdraw_rates_50 = loaded_dic_SPXL100_50years_inf_2percent["withdraw_rates"]
    success_rates_50 = loaded_dic_SPXL100_50years_inf_2percent["success_rates"]
    withdraw_rates_60 = loaded_dic_SPXL100_60years_inf_2percent["withdraw_rates"]
    success_rates_60 = loaded_dic_SPXL100_60years_inf_2percent["success_rates"]

    # SPXL plot開始
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

    pyplot.plot(loaded_dic_SPXL100_30years_inf_2percent["withdraw_rates"], loaded_dic_SPXL100_30years_inf_2percent["success_rates"], label ="30years", color="black")
    pyplot.plot(loaded_dic_SPXL100_40years_inf_2percent["withdraw_rates"],
                loaded_dic_SPXL100_40years_inf_2percent["success_rates"], label="40years", color="blue")
    pyplot.plot(loaded_dic_SPXL100_50years_inf_2percent["withdraw_rates"],
                loaded_dic_SPXL100_50years_inf_2percent["success_rates"], label="50years", color="orange")
    pyplot.plot(loaded_dic_SPXL100_60years_inf_2percent["withdraw_rates"],
                loaded_dic_SPXL100_60years_inf_2percent["success_rates"], label="60years", color="green")
    pyplot.legend()
    pyplot.savefig(out_dir + "SPXL_withdraw_siumlation_multi_years.png")
    # SPXL plot終了
    print("end: {}".format(datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")))


    # SPX load
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    loaded_dic_SPX100_30years_inf_2percent = load_dump(SPX100_30years_inf_2percent_dump_dir, "withdraw_rates", "success_rates")
    loaded_dic_SPX100_40years_inf_2percent = load_dump(SPX100_40years_inf_2percent_dump_dir, "withdraw_rates", "success_rates")
    loaded_dic_SPX100_50years_inf_2percent = load_dump(SPX100_50years_inf_2percent_dump_dir, "withdraw_rates",
                                                        "success_rates")
    loaded_dic_SPX100_60years_inf_2percent = load_dump(SPX100_60years_inf_2percent_dump_dir, "withdraw_rates",
                                                        "success_rates")
    withdraw_rates_30 = loaded_dic_SPX100_30years_inf_2percent["withdraw_rates"]
    success_rates_30 = loaded_dic_SPX100_30years_inf_2percent["success_rates"]
    withdraw_rates_40 = loaded_dic_SPX100_40years_inf_2percent["withdraw_rates"]
    success_rates_40 = loaded_dic_SPX100_40years_inf_2percent["success_rates"]
    withdraw_rates_50 = loaded_dic_SPX100_50years_inf_2percent["withdraw_rates"]
    success_rates_50 = loaded_dic_SPX100_50years_inf_2percent["success_rates"]
    withdraw_rates_60 = loaded_dic_SPX100_60years_inf_2percent["withdraw_rates"]
    success_rates_60 = loaded_dic_SPX100_60years_inf_2percent["success_rates"]
    
    # SPX plot開始
    fig = pyplot.figure(facecolor='w', linewidth=1, edgecolor='w', tight_layout=True)
    ax = fig.add_subplot(111, xlabel="Withdraw Rate", ylabel="Success Rate")
    ax.set_ylim(0, 1)
    ax.set_xlim(0, .1)
    ax.set_xticks([i / 100 for i in range(0, 10, 1)])
    ax.minorticks_on()
    ax.xaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator(4))
    ax.grid()
    ax.xaxis.tick_top()
    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))

    pyplot.plot(loaded_dic_SPX100_30years_inf_2percent["withdraw_rates"],
                loaded_dic_SPX100_30years_inf_2percent["success_rates"], label="30years", color="black")
    pyplot.plot(loaded_dic_SPX100_40years_inf_2percent["withdraw_rates"],
                loaded_dic_SPX100_40years_inf_2percent["success_rates"], label="40years", color="blue")
    pyplot.plot(loaded_dic_SPX100_50years_inf_2percent["withdraw_rates"],
                loaded_dic_SPX100_50years_inf_2percent["success_rates"], label="50years", color="orange")
    pyplot.plot(loaded_dic_SPX100_60years_inf_2percent["withdraw_rates"],
                loaded_dic_SPX100_60years_inf_2percent["success_rates"], label="60years", color="green")
    pyplot.legend()
    pyplot.savefig(out_dir + "SPX_withdraw_siumlation_multi_years.png")
    # plot終了

    time1 = time.time()
    print("経過秒数：{}".format(int(time1 - starttime)))
