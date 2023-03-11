import datetime
import math
import os
import statistics
import time

import joblib
import matplotlib
from dateutil.relativedelta import relativedelta
from matplotlib import pyplot

SPXL100_30years_inf_0percent_dump_dir = "SPXL100_30years_inf_0percent_dump\\"
out_dir = "graph_output/Return_Simulation_with_dividends/"
out_dir = "graph_output/Return_Simulation_no_dividends/"
dump_dir = "Return_Simulation/Return_Simulation_with_dividends/dump/"


def load_dump(dump_dir, *args):
    loaded_dic = {}
    for filename in args:
        if (os.path.isfile(dump_dir + filename + ".dump")):
            object = joblib.load(dump_dir + filename + ".dump")
            loaded_dic[filename] = object
            print("{} loaded: {}".format(filename, object))
    return loaded_dic


def plot_return_by_invest_years(ticker, inflation_rate=0):
    ticker_1year_dic = \
        load_dump(dump_dir + f"{ticker}100_1years_inflation_{inflation_rate * 100}percent_dump/",
                  "asset_result_list", "price_growth_rate_list")
    ticker_5years_dic = \
        load_dump(dump_dir + f"{ticker}100_5years_inflation_{inflation_rate * 100}percent_dump/",
                  "asset_result_list", "price_growth_rate_list")
    ticker_10years_dic = \
        load_dump(dump_dir + f"{ticker}100_10years_inflation_{inflation_rate * 100}percent_dump/",
                  "asset_result_list", "price_growth_rate_list")
    ticker_20years_dic = \
        load_dump(dump_dir + f"{ticker}100_20years_inflation_{inflation_rate * 100}percent_dump/",
                  "asset_result_list", "price_growth_rate_list")
    ticker_30years_dic = \
        load_dump(dump_dir + f"{ticker}100_30years_inflation_{inflation_rate * 100}percent_dump/",
                  "asset_result_list", "price_growth_rate_list")
    ticker_40years_dic = \
        load_dump(dump_dir + f"{ticker}100_40years_inflation_{inflation_rate * 100}percent_dump/",
                  "asset_result_list", "price_growth_rate_list")
    ticker_50years_dic = \
        load_dump(dump_dir + f"{ticker}100_50years_inflation_{inflation_rate * 100}percent_dump/",
                  "asset_result_list", "price_growth_rate_list")
    startdate = ticker_1year_dic["asset_result_list"][0][0]
    enddate = ticker_1year_dic["asset_result_list"][-1][0] + relativedelta(years=1)

    # test
    asset_result_list = ticker_50years_dic["asset_result_list"]

    ticker_1year_max_growth_rate = max(ticker_1year_dic["price_growth_rate_list"])
    ticker_1year_min_growth_rate = min(ticker_1year_dic["price_growth_rate_list"])
    ticker_1year_med_growth_rate = statistics.median(ticker_1year_dic["price_growth_rate_list"])

    ticker_5years_max_growth_rate = math.pow(max(ticker_5years_dic["price_growth_rate_list"]) + 1, 1 / 5) - 1
    ticker_5years_min_growth_rate = math.pow(min(ticker_5years_dic["price_growth_rate_list"]) + 1, 1 / 5) - 1
    ticker_5years_med_growth_rate = math.pow(statistics.median(ticker_5years_dic["price_growth_rate_list"]) + 1,
                                             1 / 5) - 1

    ticker_10years_max_growth_rate = math.pow(max(ticker_10years_dic["price_growth_rate_list"]) + 1, 1 / 10) - 1
    ticker_10years_min_growth_rate = math.pow(min(ticker_10years_dic["price_growth_rate_list"]) + 1, 1 / 10) - 1
    ticker_10years_med_growth_rate = math.pow(
        statistics.median(ticker_10years_dic["price_growth_rate_list"]) + 1, 1 / 10) - 1

    ticker_20years_max_growth_rate = math.pow(max(ticker_20years_dic["price_growth_rate_list"]) + 1, 1 / 20) - 1
    ticker_20years_min_growth_rate = math.pow(min(ticker_20years_dic["price_growth_rate_list"]) + 1, 1 / 20) - 1
    ticker_20years_med_growth_rate = math.pow(statistics.median(ticker_20years_dic["price_growth_rate_list"]) + 1,
                                              1 / 20) - 1

    ticker_30years_max_growth_rate = math.pow(max(ticker_30years_dic["price_growth_rate_list"]) + 1, 1 / 30) - 1
    ticker_30years_min_growth_rate = math.pow(min(ticker_30years_dic["price_growth_rate_list"]) + 1, 1 / 30) - 1
    ticker_30years_med_growth_rate = math.pow(statistics.median(ticker_30years_dic["price_growth_rate_list"]) + 1,
                                              1 / 30) - 1

    ticker_40years_max_growth_rate = math.pow(max(ticker_40years_dic["price_growth_rate_list"]) + 1, 1 / 40) - 1
    ticker_40years_min_growth_rate = math.pow(min(ticker_40years_dic["price_growth_rate_list"]) + 1, 1 / 40) - 1
    ticker_40years_med_growth_rate = math.pow(
        statistics.median(ticker_40years_dic["price_growth_rate_list"]) + 1, 1 / 40) - 1

    ticker_50years_max_growth_rate = math.pow(max(ticker_50years_dic["price_growth_rate_list"]) + 1, 1 / 50) - 1
    ticker_50years_min_growth_rate = math.pow(min(ticker_50years_dic["price_growth_rate_list"]) + 1, 1 / 50) - 1
    ticker_50years_med_growth_rate = math.pow(
        statistics.median(ticker_50years_dic["price_growth_rate_list"]) + 1, 1 / 50) - 1

    # plot開始
    fig = pyplot.figure(facecolor='w', linewidth=1, edgecolor='w', tight_layout=True)
    ax = fig.add_subplot(111, xlabel="invest years", ylabel="Compound Annual Growth Rate(CAGR), no dividend",
                         title="{} return by different invest years\nfrom {} to {} monthly datasets".format(
                             ticker, startdate.strftime("%Y/%m/%d"), enddate.strftime("%Y/%m/%d")))
    # ax.set_ylim(-1, 1)

    # ax.set_xticks([i/100 for i in range(0, 10, 1)])
    # ax.minorticks_on()
    # ax.xaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator(5))
    ax.grid(linestyle="dotted", linewidth=.5)
    # ax.xaxis.tick_top()
    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    # ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))

    x = [i for i in range(1, 8, 1)]
    y_max = [ticker_1year_max_growth_rate, ticker_5years_max_growth_rate, ticker_10years_max_growth_rate,
             ticker_20years_max_growth_rate, ticker_30years_max_growth_rate,
             ticker_40years_max_growth_rate, ticker_50years_max_growth_rate]
    y_min = [ticker_1year_min_growth_rate, ticker_5years_min_growth_rate, ticker_10years_min_growth_rate,
             ticker_20years_min_growth_rate, ticker_30years_min_growth_rate,
             ticker_40years_min_growth_rate, ticker_50years_min_growth_rate]
    y_med = [ticker_1year_med_growth_rate, ticker_5years_med_growth_rate, ticker_10years_med_growth_rate,
             ticker_20years_med_growth_rate, ticker_30years_med_growth_rate,
             ticker_40years_med_growth_rate, ticker_50years_med_growth_rate]

    ax.bar(x, y_max, width=0.3, color="black", label="return range")
    ax.bar(x, y_min, width=0.3, color="red", label="return range")

    pyplot.plot(x, y_med, ".", color='blue')
    # 数値情報を挿入
    # for x, y in zip(x, y_max):
    #     pyplot.text(x, y, "{:.0%}".format(y), ha='center', va='bottom')
    # for x, y in zip(x, y_med):
    #     pyplot.text(x, y, "{:.0%}".format(y), ha='center', va='bottom')
    for i in range(1, len(x) + 1):
        pyplot.annotate("{:.0%}".format(y_max[i - 1]), (i, y_max[i - 1]), ha='center')
    for i in range(1, len(x) + 1):
        pyplot.annotate("{:.0%}".format(y_min[i - 1]), (i, y_min[i - 1] - .1), ha='center', color="red")
    for i in range(1, len(x) + 1):
        pyplot.annotate("{:.0%}".format(y_med[i - 1]), (i + .35, y_med[i - 1]), ha='center', color="blue")
    pyplot.xticks(x, [1, 5, 10, 20, 30, 40, 50])
    ax.text(.5, .5, "generated by lapi\n@Weibo, @Zhihu, @Note", transform=ax.transAxes,
            fontsize=30, color='gray', alpha=0.3,
            ha='center', va='center', rotation=30)

    # pyplot.plot(loaded_dic_tickerL100_30years_inf_2percent["withdraw_rates"], loaded_dic_tickerL1 00_30years_inf_2percent["success_rates"], label ="tickerL 100%")
    pyplot.savefig(out_dir + f"{ticker}_return_by_invest_years.png")
    print(ticker)
    print("{} / {} = {:.0%}".format(sum([i >= 0 for i in ticker_1year_dic["price_growth_rate_list"]]),
                                    len(ticker_1year_dic["price_growth_rate_list"]),
                                    sum([i >= 0 for i in ticker_1year_dic["price_growth_rate_list"]]) / len(
                                        ticker_1year_dic["price_growth_rate_list"])))
    print("{} / {} = {:.0%}".format(sum([i >= 0 for i in ticker_5years_dic["price_growth_rate_list"]]),
                                    len(ticker_5years_dic["price_growth_rate_list"]),
                                    sum([i >= 0 for i in ticker_5years_dic["price_growth_rate_list"]]) / len(
                                        ticker_5years_dic["price_growth_rate_list"])))
    print("{} / {} = {:.0%}".format(sum([i >= 0 for i in ticker_10years_dic["price_growth_rate_list"]]),
                                    len(ticker_10years_dic["price_growth_rate_list"]),
                                    sum([i >= 0 for i in
                                         ticker_10years_dic["price_growth_rate_list"]]) / len(
                                        ticker_10years_dic["price_growth_rate_list"])))
    print("{} / {} = {:.0%}".format(sum([i >= 0 for i in ticker_20years_dic["price_growth_rate_list"]]),
                                    len(ticker_20years_dic["price_growth_rate_list"]),
                                    sum([i >= 0 for i in
                                         ticker_20years_dic["price_growth_rate_list"]]) / len(
                                        ticker_20years_dic["price_growth_rate_list"])))
    print("{} / {} = {:.0%}".format(sum([i >= 0 for i in ticker_30years_dic["price_growth_rate_list"]]),
                                    len(ticker_30years_dic["price_growth_rate_list"]),
                                    sum([i >= 0 for i in
                                         ticker_30years_dic["price_growth_rate_list"]]) / len(
                                        ticker_30years_dic["price_growth_rate_list"])))
    print("{} / {} = {:.0%}".format(sum([i >= 0 for i in ticker_40years_dic["price_growth_rate_list"]]),
                                    len(ticker_40years_dic["price_growth_rate_list"]),
                                    sum([i >= 0 for i in
                                         ticker_40years_dic["price_growth_rate_list"]]) / len(
                                        ticker_40years_dic["price_growth_rate_list"])))
    print("{} / {} = {:.0%}".format(sum([i >= 0 for i in ticker_50years_dic["price_growth_rate_list"]]),
                                    len(ticker_50years_dic["price_growth_rate_list"]),
                                    sum([i > 0 for i in ticker_50years_dic["price_growth_rate_list"]]) / len(
                                        ticker_50years_dic["price_growth_rate_list"])))
    # plot終了


if __name__ == '__main__':
    starttime = time.time()
    print("start: {}".format(datetime.datetime.fromtimestamp(starttime).strftime("%H:%M:%S")))
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    plot_return_by_invest_years("SPX")
    plot_return_by_invest_years("SPXL")
    plot_return_by_invest_years("SSO")

    print("end: {}".format(datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")))
    time1 = time.time()
    print("経過秒数：{}".format(int(time1 - starttime)))
