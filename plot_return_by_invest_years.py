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
out_dir = "graph_output\\"

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
    SPX_1year_dic = load_dump("Return_Simulation\dump\SPX100_1years_inflation_0percent_dump\\", "asset_result_list", "price_growth_rate_list")
    SPX_5years_dic = load_dump("Return_Simulation\dump\SPX100_5years_inflation_0percent_dump\\", "asset_result_list", "price_growth_rate_list")
    SPX_10years_dic = load_dump("Return_Simulation\dump\SPX100_10years_inflation_0percent_dump\\", "asset_result_list", "price_growth_rate_list")
    SPX_20years_dic = load_dump("Return_Simulation\dump\SPX100_20years_inflation_0percent_dump\\", "asset_result_list", "price_growth_rate_list")
    SPX_30years_dic = load_dump("Return_Simulation\dump\SPX100_30years_inflation_0percent_dump\\", "asset_result_list", "price_growth_rate_list")
    SPX_40years_dic = load_dump("Return_Simulation\dump\SPX100_40years_inflation_0percent_dump\\", "asset_result_list", "price_growth_rate_list")
    SPX_50years_dic = load_dump("Return_Simulation\dump\SPX100_50years_inflation_0percent_dump\\", "asset_result_list", "price_growth_rate_list")


    startdate = SPX_1year_dic["asset_result_list"][0][0]
    # startdate = datetime.datetime(1945, 1, 2)

    start_index = 0
    for i in SPX_1year_dic["asset_result_list"]:
        if i[0] == startdate:
            break
        start_index += 1

    enddate = SPX_1year_dic["asset_result_list"][-1][0] + relativedelta(years=1)

    # 成長率x⇒CAGR： math.pow(1+x, years)
    SPX_1year_max_growth_rate = max(SPX_1year_dic["price_growth_rate_list"][start_index:])
    SPX_1year_min_growth_rate = min(SPX_1year_dic["price_growth_rate_list"][start_index:])
    SPX_1year_med_growth_rate = statistics.median(SPX_1year_dic["price_growth_rate_list"][start_index:])

    SPX_5years_max_growth_rate = math.pow(max(SPX_5years_dic["price_growth_rate_list"][start_index:]) + 1, 1/5) - 1
    SPX_5years_min_growth_rate = math.pow(min(SPX_5years_dic["price_growth_rate_list"][start_index:]) + 1, 1/5) - 1
    SPX_5years_med_growth_rate = math.pow(statistics.median(SPX_5years_dic["price_growth_rate_list"][start_index:]) + 1, 1/5) - 1

    SPX_10years_max_growth_rate = math.pow(max(SPX_10years_dic["price_growth_rate_list"][start_index:]) + 1, 1/10) - 1
    SPX_10years_min_growth_rate = math.pow(min(SPX_10years_dic["price_growth_rate_list"][start_index:]) + 1, 1/10) - 1
    SPX_10years_med_growth_rate = math.pow(statistics.median(SPX_10years_dic["price_growth_rate_list"][start_index:])+ 1, 1/10) - 1

    SPX_20years_max_growth_rate = math.pow(max(SPX_20years_dic["price_growth_rate_list"][start_index:]) + 1, 1/20) - 1
    SPX_20years_min_growth_rate = math.pow(min(SPX_20years_dic["price_growth_rate_list"][start_index:]) + 1, 1/20) - 1
    SPX_20years_med_growth_rate = math.pow(statistics.median(SPX_20years_dic["price_growth_rate_list"])+ 1, 1/20) - 1

    SPX_30years_max_growth_rate = math.pow(max(SPX_30years_dic["price_growth_rate_list"][start_index:]) + 1, 1/30) - 1
    SPX_30years_min_growth_rate = math.pow(min(SPX_30years_dic["price_growth_rate_list"][start_index:]) + 1, 1/30) - 1
    SPX_30years_med_growth_rate = math.pow(statistics.median(SPX_30years_dic["price_growth_rate_list"])+ 1, 1/30) - 1

    SPX_40years_max_growth_rate = math.pow(max(SPX_40years_dic["price_growth_rate_list"][start_index:]) + 1, 1/40) - 1
    SPX_40years_min_growth_rate = math.pow(min(SPX_40years_dic["price_growth_rate_list"][start_index:]) + 1, 1/40) - 1
    SPX_40years_med_growth_rate = math.pow(statistics.median(SPX_40years_dic["price_growth_rate_list"][start_index:])+ 1, 1/40) - 1

    SPX_50years_max_growth_rate = math.pow(max(SPX_50years_dic["price_growth_rate_list"][start_index:]) + 1, 1/50) - 1
    SPX_50years_min_growth_rate = math.pow(min(SPX_50years_dic["price_growth_rate_list"][start_index:]) + 1, 1/50) - 1
    SPX_50years_med_growth_rate = math.pow(statistics.median(SPX_50years_dic["price_growth_rate_list"][start_index:])+ 1, 1/50) - 1


    # plot開始
    fig = pyplot.figure(facecolor='w', linewidth=1, edgecolor='w', tight_layout=True)
    ax = fig.add_subplot(111, xlabel= "invest years", ylabel="Compound Annual Growth Rate(CAGR), no dividend", title="S&P500 return by different invest years\nfrom {} to {} daily datasets".format(startdate.strftime("%Y/%m/%d"), enddate.strftime("%Y/%m/%d")))
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
    y_max = [SPX_1year_max_growth_rate, SPX_5years_max_growth_rate, SPX_10years_max_growth_rate, SPX_20years_max_growth_rate, SPX_30years_max_growth_rate,
               SPX_40years_max_growth_rate, SPX_50years_max_growth_rate]
    y_min = [SPX_1year_min_growth_rate, SPX_5years_min_growth_rate, SPX_10years_min_growth_rate, SPX_20years_min_growth_rate, SPX_30years_min_growth_rate,
               SPX_40years_min_growth_rate, SPX_50years_min_growth_rate]
    y_med = [SPX_1year_med_growth_rate, SPX_5years_med_growth_rate, SPX_10years_med_growth_rate, SPX_20years_med_growth_rate, SPX_30years_med_growth_rate,
               SPX_40years_med_growth_rate, SPX_50years_med_growth_rate]

    ax.bar(x, y_max, width=0.3, color="black", label="return range")
    ax.bar(x, y_min, width=0.3, color="red", label="return range")

    pyplot.plot(x, y_med, ".", color='blue')
    # 数値情報を挿入
    # for x, y in zip(x, y_max):
    #     pyplot.text(x, y, "{:.0%}".format(y), ha='center', va='bottom')
    # for x, y in zip(x, y_med):
    #     pyplot.text(x, y, "{:.0%}".format(y), ha='center', va='bottom')
    for i in range(1, len(x) + 1):
        pyplot.annotate("{:.0%}".format(y_max[i-1]), (i, y_max[i-1]), ha='center')
    for i in range(1, len(x) + 1):
        pyplot.annotate("{:.0%}".format(y_min[i-1]), (i, y_min[i-1] - .1), ha='center', color="red")
    for i in range(1, len(x) + 1):
        pyplot.annotate("{:.0%}".format(y_med[i-1]), (i + .35, y_med[i-1]), ha='center', color="blue")
    pyplot.xticks(x, [1, 5, 10, 20, 30, 40, 50])
    ax.text(.5, .5, "generated by lapi\n@Weibo, @Zhihu, @Note", transform=ax.transAxes,
        fontsize=30, color='gray', alpha=0.3,
        ha='center', va='center', rotation=30)

    # pyplot.plot(loaded_dic_SPXL100_30years_inf_2percent["withdraw_rates"], loaded_dic_SPXL1 00_30years_inf_2percent["success_rates"], label ="SPXL 100%")
    pyplot.savefig(out_dir + "SPX_return_by_invest_years.png")


    print("{} / {} = {:.0%}".format(sum([i >= 0 for i in SPX_1year_dic["price_growth_rate_list"][start_index:]]),
                                    len(SPX_1year_dic["price_growth_rate_list"][start_index:]),
                                    sum([i >= 0 for i in SPX_1year_dic["price_growth_rate_list"][start_index:]]) / len(SPX_1year_dic["price_growth_rate_list"][start_index:])))
    print("{} / {} = {:.0%}".format(sum([i >= 0 for i in SPX_5years_dic["price_growth_rate_list"][start_index:]]),
                                    len(SPX_5years_dic["price_growth_rate_list"][start_index:]),
                                    sum([i >= 0 for i in SPX_5years_dic["price_growth_rate_list"][start_index:]]) / len(SPX_5years_dic["price_growth_rate_list"][start_index:])))
    print("{} / {} = {:.0%}".format(sum([i >= 0 for i in SPX_10years_dic["price_growth_rate_list"][start_index:]]),
                                    len(SPX_10years_dic["price_growth_rate_list"][start_index:]),
                                    sum([i >= 0 for i in SPX_10years_dic["price_growth_rate_list"][start_index:]]) / len(SPX_10years_dic["price_growth_rate_list"][start_index:])))
    print("{} / {} = {:.0%}".format(sum([i >= 0 for i in SPX_20years_dic["price_growth_rate_list"][start_index:]]),
                                    len(SPX_20years_dic["price_growth_rate_list"][start_index:]),
                                    sum([i >= 0 for i in SPX_20years_dic["price_growth_rate_list"][start_index:]]) / len(SPX_20years_dic["price_growth_rate_list"][start_index:])))
    print("{} / {} = {:.0%}".format(sum([i >= 0 for i in SPX_30years_dic["price_growth_rate_list"][start_index:]]),
                                    len(SPX_30years_dic["price_growth_rate_list"][start_index:]),
                                    sum([i >= 0 for i in SPX_30years_dic["price_growth_rate_list"][start_index:]]) / len(SPX_30years_dic["price_growth_rate_list"][start_index:])))
    print("{} / {} = {:.0%}".format(sum([i >= 0 for i in SPX_40years_dic["price_growth_rate_list"][start_index:]]),
                                    len(SPX_40years_dic["price_growth_rate_list"][start_index:]),
                                    sum([i >= 0 for i in SPX_40years_dic["price_growth_rate_list"][start_index:]]) / len(
        SPX_40years_dic["price_growth_rate_list"][start_index:])))
    print("{} / {} = {:.0%}".format(sum([i >= 0 for i in SPX_50years_dic["price_growth_rate_list"][start_index:]]),
                                    len(SPX_50years_dic["price_growth_rate_list"][start_index:]),
                                    sum([i > 0 for i in SPX_50years_dic["price_growth_rate_list"][start_index:]]) / len(
        SPX_50years_dic["price_growth_rate_list"][start_index:])))
    # plot終了

    # SPXL Return start
    SPXL_1year_dic = load_dump("Return_Simulation\dump\SPXL100_1years_inflation_0percent_dump\\", "asset_result_list",
                              "price_growth_rate_list")
    SPXL_5years_dic = load_dump("Return_Simulation\dump\SPXL100_5years_inflation_0percent_dump\\", "asset_result_list",
                               "price_growth_rate_list")
    SPXL_10years_dic = load_dump("Return_Simulation\dump\SPXL100_10years_inflation_0percent_dump\\", "asset_result_list",
                                "price_growth_rate_list")
    SPXL_20years_dic = load_dump("Return_Simulation\dump\SPXL100_20years_inflation_0percent_dump\\", "asset_result_list",
                                "price_growth_rate_list")
    SPXL_30years_dic = load_dump("Return_Simulation\dump\SPXL100_30years_inflation_0percent_dump\\", "asset_result_list",
                                "price_growth_rate_list")
    SPXL_40years_dic = load_dump("Return_Simulation\dump\SPXL100_40years_inflation_0percent_dump\\", "asset_result_list",
                                "price_growth_rate_list")
    SPXL_50years_dic = load_dump("Return_Simulation\dump\SPXL100_50years_inflation_0percent_dump\\", "asset_result_list",
                                "price_growth_rate_list")

    startdate = SPXL_1year_dic["asset_result_list"][0][0]
    # startdate = datetime.datetime(1945, 1, 2)

    start_index = 0
    for i in SPXL_1year_dic["asset_result_list"]:
        if i[0] == startdate:
            break
        start_index += 1

    enddate = SPXL_1year_dic["asset_result_list"][-1][0] + relativedelta(years=1)

    # 成長率x⇒CAGR： math.pow(1+x, years)
    SPXL_1year_max_growth_rate = max(SPXL_1year_dic["price_growth_rate_list"][start_index:])
    SPXL_1year_min_growth_rate = min(SPXL_1year_dic["price_growth_rate_list"][start_index:])
    SPXL_1year_med_growth_rate = statistics.median(SPXL_1year_dic["price_growth_rate_list"][start_index:])

    SPXL_5years_max_growth_rate = math.pow(max(SPXL_5years_dic["price_growth_rate_list"][start_index:]) + 1, 1 / 5) - 1
    SPXL_5years_min_growth_rate = math.pow(min(SPXL_5years_dic["price_growth_rate_list"][start_index:]) + 1, 1 / 5) - 1
    SPXL_5years_med_growth_rate = math.pow(statistics.median(SPXL_5years_dic["price_growth_rate_list"][start_index:]) + 1,
                                          1 / 5) - 1

    SPXL_10years_max_growth_rate = math.pow(max(SPXL_10years_dic["price_growth_rate_list"][start_index:]) + 1, 1 / 10) - 1
    SPXL_10years_min_growth_rate = math.pow(min(SPXL_10years_dic["price_growth_rate_list"][start_index:]) + 1, 1 / 10) - 1
    SPXL_10years_med_growth_rate = math.pow(
        statistics.median(SPXL_10years_dic["price_growth_rate_list"][start_index:]) + 1, 1 / 10) - 1

    SPXL_20years_max_growth_rate = math.pow(max(SPXL_20years_dic["price_growth_rate_list"][start_index:]) + 1, 1 / 20) - 1
    SPXL_20years_min_growth_rate = math.pow(min(SPXL_20years_dic["price_growth_rate_list"][start_index:]) + 1, 1 / 20) - 1
    SPXL_20years_med_growth_rate = math.pow(statistics.median(SPXL_20years_dic["price_growth_rate_list"]) + 1, 1 / 20) - 1

    SPXL_30years_max_growth_rate = math.pow(max(SPXL_30years_dic["price_growth_rate_list"][start_index:]) + 1, 1 / 30) - 1
    SPXL_30years_min_growth_rate = math.pow(min(SPXL_30years_dic["price_growth_rate_list"][start_index:]) + 1, 1 / 30) - 1
    SPXL_30years_med_growth_rate = math.pow(statistics.median(SPXL_30years_dic["price_growth_rate_list"]) + 1, 1 / 30) - 1

    SPXL_40years_max_growth_rate = math.pow(max(SPXL_40years_dic["price_growth_rate_list"][start_index:]) + 1, 1 / 40) - 1
    SPXL_40years_min_growth_rate = math.pow(min(SPXL_40years_dic["price_growth_rate_list"][start_index:]) + 1, 1 / 40) - 1
    SPXL_40years_med_growth_rate = math.pow(
        statistics.median(SPXL_40years_dic["price_growth_rate_list"][start_index:]) + 1, 1 / 40) - 1

    SPXL_50years_max_growth_rate = math.pow(max(SPXL_50years_dic["price_growth_rate_list"][start_index:]) + 1, 1 / 50) - 1
    SPXL_50years_min_growth_rate = math.pow(min(SPXL_50years_dic["price_growth_rate_list"][start_index:]) + 1, 1 / 50) - 1
    SPXL_50years_med_growth_rate = math.pow(
        statistics.median(SPXL_50years_dic["price_growth_rate_list"][start_index:]) + 1, 1 / 50) - 1

    # plot開始
    fig = pyplot.figure(facecolor='w', linewidth=1, edgecolor='w', tight_layout=True)
    ax = fig.add_subplot(111, xlabel="invest years", ylabel="Compound Annual Growth Rate(CAGR), no dividend",
                         title="S&P500 return by different invest years\nfrom {} to {} daily datasets".format(
                             startdate.strftime("%Y/%m/%d"), enddate.strftime("%Y/%m/%d")))
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
    y_max = [SPXL_1year_max_growth_rate, SPXL_5years_max_growth_rate, SPXL_10years_max_growth_rate,
             SPXL_20years_max_growth_rate, SPXL_30years_max_growth_rate,
             SPXL_40years_max_growth_rate, SPXL_50years_max_growth_rate]
    y_min = [SPXL_1year_min_growth_rate, SPXL_5years_min_growth_rate, SPXL_10years_min_growth_rate,
             SPXL_20years_min_growth_rate, SPXL_30years_min_growth_rate,
             SPXL_40years_min_growth_rate, SPXL_50years_min_growth_rate]
    y_med = [SPXL_1year_med_growth_rate, SPXL_5years_med_growth_rate, SPXL_10years_med_growth_rate,
             SPXL_20years_med_growth_rate, SPXL_30years_med_growth_rate,
             SPXL_40years_med_growth_rate, SPXL_50years_med_growth_rate]

    ax.bar(x, y_max, width=0.3, color="black", label="return range")
    ax.bar(x, y_min, width=0.3, color="red", label="return range")

    pyplot.plot(x, y_med, ".", color='blue')
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

    # pyplot.plot(loaded_dic_SPXLL100_30years_inf_2percent["withdraw_rates"], loaded_dic_SPXLL1 00_30years_inf_2percent["success_rates"], label ="SPXLL 100%")
    pyplot.savefig(out_dir + "SPXL_return_by_invest_years.png")

    print("{} / {} = {:.0%}".format(sum([i >= 0 for i in SPXL_1year_dic["price_growth_rate_list"][start_index:]]),
                                    len(SPXL_1year_dic["price_growth_rate_list"][start_index:]),
                                    sum([i >= 0 for i in SPXL_1year_dic["price_growth_rate_list"][start_index:]]) / len(
                                        SPXL_1year_dic["price_growth_rate_list"][start_index:])))
    print("{} / {} = {:.0%}".format(sum([i >= 0 for i in SPXL_5years_dic["price_growth_rate_list"][start_index:]]),
                                    len(SPXL_5years_dic["price_growth_rate_list"][start_index:]),
                                    sum([i >= 0 for i in SPXL_5years_dic["price_growth_rate_list"][start_index:]]) / len(
                                        SPXL_5years_dic["price_growth_rate_list"][start_index:])))
    print("{} / {} = {:.0%}".format(sum([i >= 0 for i in SPXL_10years_dic["price_growth_rate_list"][start_index:]]),
                                    len(SPXL_10years_dic["price_growth_rate_list"][start_index:]),
                                    sum([i >= 0 for i in
                                         SPXL_10years_dic["price_growth_rate_list"][start_index:]]) / len(
                                        SPXL_10years_dic["price_growth_rate_list"][start_index:])))
    print("{} / {} = {:.0%}".format(sum([i >= 0 for i in SPXL_20years_dic["price_growth_rate_list"][start_index:]]),
                                    len(SPXL_20years_dic["price_growth_rate_list"][start_index:]),
                                    sum([i >= 0 for i in
                                         SPXL_20years_dic["price_growth_rate_list"][start_index:]]) / len(
                                        SPXL_20years_dic["price_growth_rate_list"][start_index:])))
    print("{} / {} = {:.0%}".format(sum([i >= 0 for i in SPXL_30years_dic["price_growth_rate_list"][start_index:]]),
                                    len(SPXL_30years_dic["price_growth_rate_list"][start_index:]),
                                    sum([i >= 0 for i in
                                         SPXL_30years_dic["price_growth_rate_list"][start_index:]]) / len(
                                        SPXL_30years_dic["price_growth_rate_list"][start_index:])))
    print("{} / {} = {:.0%}".format(sum([i >= 0 for i in SPXL_40years_dic["price_growth_rate_list"][start_index:]]),
                                    len(SPXL_40years_dic["price_growth_rate_list"][start_index:]),
                                    sum([i >= 0 for i in
                                         SPXL_40years_dic["price_growth_rate_list"][start_index:]]) / len(
                                        SPXL_40years_dic["price_growth_rate_list"][start_index:])))
    print("{} / {} = {:.0%}".format(sum([i >= 0 for i in SPXL_50years_dic["price_growth_rate_list"][start_index:]]),
                                    len(SPXL_50years_dic["price_growth_rate_list"][start_index:]),
                                    sum([i > 0 for i in SPXL_50years_dic["price_growth_rate_list"][start_index:]]) / len(
                                        SPXL_50years_dic["price_growth_rate_list"][start_index:])))
    # End of SPXL

    # Start SOO
    SSO_1year_dic = load_dump("Return_Simulation\dump\SSO100_1years_inflation_0percent_dump\\", "asset_result_list",
                              "price_growth_rate_list")
    SSO_5years_dic = load_dump("Return_Simulation\dump\SSO100_5years_inflation_0percent_dump\\", "asset_result_list",
                               "price_growth_rate_list")
    SSO_10years_dic = load_dump("Return_Simulation\dump\SSO100_10years_inflation_0percent_dump\\", "asset_result_list",
                                "price_growth_rate_list")
    SSO_20years_dic = load_dump("Return_Simulation\dump\SSO100_20years_inflation_0percent_dump\\", "asset_result_list",
                                "price_growth_rate_list")
    SSO_30years_dic = load_dump("Return_Simulation\dump\SSO100_30years_inflation_0percent_dump\\", "asset_result_list",
                                "price_growth_rate_list")
    SSO_40years_dic = load_dump("Return_Simulation\dump\SSO100_40years_inflation_0percent_dump\\", "asset_result_list",
                                "price_growth_rate_list")
    SSO_50years_dic = load_dump("Return_Simulation\dump\SSO100_50years_inflation_0percent_dump\\", "asset_result_list",
                                "price_growth_rate_list")

    startdate = SSO_1year_dic["asset_result_list"][0][0]
    # startdate = datetime.datetime(1945, 1, 2)

    start_index = 0
    for i in SSO_1year_dic["asset_result_list"]:
        if i[0] == startdate:
            break
        start_index += 1

    enddate = SSO_1year_dic["asset_result_list"][-1][0] + relativedelta(years=1)

    # 成長率x⇒CAGR： math.pow(1+x, years)
    SSO_1year_max_growth_rate = max(SSO_1year_dic["price_growth_rate_list"][start_index:])
    SSO_1year_min_growth_rate = min(SSO_1year_dic["price_growth_rate_list"][start_index:])
    SSO_1year_med_growth_rate = statistics.median(SSO_1year_dic["price_growth_rate_list"][start_index:])

    SSO_5years_max_growth_rate = math.pow(max(SSO_5years_dic["price_growth_rate_list"][start_index:]) + 1, 1 / 5) - 1
    SSO_5years_min_growth_rate = math.pow(min(SSO_5years_dic["price_growth_rate_list"][start_index:]) + 1, 1 / 5) - 1
    SSO_5years_med_growth_rate = math.pow(statistics.median(SSO_5years_dic["price_growth_rate_list"][start_index:]) + 1,
                                          1 / 5) - 1

    SSO_10years_max_growth_rate = math.pow(max(SSO_10years_dic["price_growth_rate_list"][start_index:]) + 1, 1 / 10) - 1
    SSO_10years_min_growth_rate = math.pow(min(SSO_10years_dic["price_growth_rate_list"][start_index:]) + 1, 1 / 10) - 1
    SSO_10years_med_growth_rate = math.pow(
        statistics.median(SSO_10years_dic["price_growth_rate_list"][start_index:]) + 1, 1 / 10) - 1

    SSO_20years_max_growth_rate = math.pow(max(SSO_20years_dic["price_growth_rate_list"][start_index:]) + 1, 1 / 20) - 1
    SSO_20years_min_growth_rate = math.pow(min(SSO_20years_dic["price_growth_rate_list"][start_index:]) + 1, 1 / 20) - 1
    SSO_20years_med_growth_rate = math.pow(statistics.median(SSO_20years_dic["price_growth_rate_list"]) + 1, 1 / 20) - 1

    SSO_30years_max_growth_rate = math.pow(max(SSO_30years_dic["price_growth_rate_list"][start_index:]) + 1, 1 / 30) - 1
    SSO_30years_min_growth_rate = math.pow(min(SSO_30years_dic["price_growth_rate_list"][start_index:]) + 1, 1 / 30) - 1
    SSO_30years_med_growth_rate = math.pow(statistics.median(SSO_30years_dic["price_growth_rate_list"]) + 1, 1 / 30) - 1

    SSO_40years_max_growth_rate = math.pow(max(SSO_40years_dic["price_growth_rate_list"][start_index:]) + 1, 1 / 40) - 1
    SSO_40years_min_growth_rate = math.pow(min(SSO_40years_dic["price_growth_rate_list"][start_index:]) + 1, 1 / 40) - 1
    SSO_40years_med_growth_rate = math.pow(
        statistics.median(SSO_40years_dic["price_growth_rate_list"][start_index:]) + 1, 1 / 40) - 1

    SSO_50years_max_growth_rate = math.pow(max(SSO_50years_dic["price_growth_rate_list"][start_index:]) + 1, 1 / 50) - 1
    SSO_50years_min_growth_rate = math.pow(min(SSO_50years_dic["price_growth_rate_list"][start_index:]) + 1, 1 / 50) - 1
    SSO_50years_med_growth_rate = math.pow(
        statistics.median(SSO_50years_dic["price_growth_rate_list"][start_index:]) + 1, 1 / 50) - 1

    # plot開始
    fig = pyplot.figure(facecolor='w', linewidth=1, edgecolor='w', tight_layout=True)
    ax = fig.add_subplot(111, xlabel="invest years", ylabel="Compound Annual Growth Rate(CAGR), no dividend",
                         title="S&P500 return by different invest years\nfrom {} to {} daily datasets".format(
                             startdate.strftime("%Y/%m/%d"), enddate.strftime("%Y/%m/%d")))
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
    y_max = [SSO_1year_max_growth_rate, SSO_5years_max_growth_rate, SSO_10years_max_growth_rate,
             SSO_20years_max_growth_rate, SSO_30years_max_growth_rate,
             SSO_40years_max_growth_rate, SSO_50years_max_growth_rate]
    y_min = [SSO_1year_min_growth_rate, SSO_5years_min_growth_rate, SSO_10years_min_growth_rate,
             SSO_20years_min_growth_rate, SSO_30years_min_growth_rate,
             SSO_40years_min_growth_rate, SSO_50years_min_growth_rate]
    y_med = [SSO_1year_med_growth_rate, SSO_5years_med_growth_rate, SSO_10years_med_growth_rate,
             SSO_20years_med_growth_rate, SSO_30years_med_growth_rate,
             SSO_40years_med_growth_rate, SSO_50years_med_growth_rate]

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

    # pyplot.plot(loaded_dic_SSOL100_30years_inf_2percent["withdraw_rates"], loaded_dic_SSOL1 00_30years_inf_2percent["success_rates"], label ="SSOL 100%")
    pyplot.savefig(out_dir + "SSO_return_by_invest_years.png")

    print("{} / {} = {:.0%}".format(sum([i >= 0 for i in SSO_1year_dic["price_growth_rate_list"][start_index:]]),
                                    len(SSO_1year_dic["price_growth_rate_list"][start_index:]),
                                    sum([i >= 0 for i in SSO_1year_dic["price_growth_rate_list"][start_index:]]) / len(
                                        SSO_1year_dic["price_growth_rate_list"][start_index:])))
    print("{} / {} = {:.0%}".format(sum([i >= 0 for i in SSO_5years_dic["price_growth_rate_list"][start_index:]]),
                                    len(SSO_5years_dic["price_growth_rate_list"][start_index:]),
                                    sum([i >= 0 for i in SSO_5years_dic["price_growth_rate_list"][start_index:]]) / len(
                                        SSO_5years_dic["price_growth_rate_list"][start_index:])))
    print("{} / {} = {:.0%}".format(sum([i >= 0 for i in SSO_10years_dic["price_growth_rate_list"][start_index:]]),
                                    len(SSO_10years_dic["price_growth_rate_list"][start_index:]),
                                    sum([i >= 0 for i in
                                         SSO_10years_dic["price_growth_rate_list"][start_index:]]) / len(
                                        SSO_10years_dic["price_growth_rate_list"][start_index:])))
    print("{} / {} = {:.0%}".format(sum([i >= 0 for i in SSO_20years_dic["price_growth_rate_list"][start_index:]]),
                                    len(SSO_20years_dic["price_growth_rate_list"][start_index:]),
                                    sum([i >= 0 for i in
                                         SSO_20years_dic["price_growth_rate_list"][start_index:]]) / len(
                                        SSO_20years_dic["price_growth_rate_list"][start_index:])))
    print("{} / {} = {:.0%}".format(sum([i >= 0 for i in SSO_30years_dic["price_growth_rate_list"][start_index:]]),
                                    len(SSO_30years_dic["price_growth_rate_list"][start_index:]),
                                    sum([i >= 0 for i in
                                         SSO_30years_dic["price_growth_rate_list"][start_index:]]) / len(
                                        SSO_30years_dic["price_growth_rate_list"][start_index:])))
    print("{} / {} = {:.0%}".format(sum([i >= 0 for i in SSO_40years_dic["price_growth_rate_list"][start_index:]]),
                                    len(SSO_40years_dic["price_growth_rate_list"][start_index:]),
                                    sum([i >= 0 for i in
                                         SSO_40years_dic["price_growth_rate_list"][start_index:]]) / len(
                                        SSO_40years_dic["price_growth_rate_list"][start_index:])))
    print("{} / {} = {:.0%}".format(sum([i >= 0 for i in SSO_50years_dic["price_growth_rate_list"][start_index:]]),
                                    len(SSO_50years_dic["price_growth_rate_list"][start_index:]),
                                    sum([i > 0 for i in SSO_50years_dic["price_growth_rate_list"][start_index:]]) / len(
                                        SSO_50years_dic["price_growth_rate_list"][start_index:])))
    # plot終了

    print("end: {}".format(datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")))
    time1 = time.time()
    print("経過秒数：{}".format(int(time1 - starttime)))

