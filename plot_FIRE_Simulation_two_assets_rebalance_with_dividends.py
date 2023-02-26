import datetime
import os
import time

import joblib
import matplotlib
from matplotlib import pyplot

out_dir = "graph_output\\FIRE_Simulation_two_assets_rebalance_with_dividends\\"

def load_dump(dump_dir, *args):
    loaded_dic = {}
    for filename in args:
        if (os.path.isfile(dump_dir + filename + ".dump")):
            object = joblib.load(dump_dir + filename + ".dump")
            loaded_dic[filename] = object
            print(f"{dump_dir}\\{filename} loaded: {object}")
    return loaded_dic

def plot_success_rates_in_different_withdraw_rates_with_multiple_ratio(asset1, asset2, withdraw_years, ymin=0):

    asset1_100_asset2_0_withdraw_years_inf_2percent_dump_dir = \
        f"FIRE_Simulation\\two_assets_rebalance_with_dividends\\{asset1}100_{asset2}0_{withdraw_years}years_inflation_2.0percent_dump\\"
    asset1_75_asset2_25_withdraw_years_inf_2percent_dump_dir = \
        f"FIRE_Simulation\\two_assets_rebalance_with_dividends\\{asset1}75.0_{asset2}25.0_{withdraw_years}years_inflation_2.0percent_dump\\"
    asset1_50_asset2_50_withdraw_years_inf_2percent_dump_dir = \
        f"FIRE_Simulation\\two_assets_rebalance_with_dividends\\{asset1}50.0_{asset2}50.0_{withdraw_years}years_inflation_2.0percent_dump\\"
    asset1_25_asset2_75_withdraw_years_inf_2percent_dump_dir = \
        f"FIRE_Simulation\\two_assets_rebalance_with_dividends\\{asset1}25.0_{asset2}75.0_{withdraw_years}years_inflation_2.0percent_dump\\"
    asset1_0_asset2_100_withdraw_years_inf_2percent_dump_dir = \
        f"FIRE_Simulation\\two_assets_rebalance_with_dividends\\{asset1}0_{asset2}100_{withdraw_years}years_inflation_2.0percent_dump\\"


    loaded_dic_asset1_100_asset2_0_withdraw_years_inf_2percent= load_dump(asset1_100_asset2_0_withdraw_years_inf_2percent_dump_dir, "withdraw_rates",
                                                        "success_rates")
    loaded_dic_asset1_75_asset2_25_withdraw_years_inf_2percent = load_dump(asset1_75_asset2_25_withdraw_years_inf_2percent_dump_dir,
                                                               "withdraw_rates",
                                                               "success_rates")
    loaded_dic_asset1_50_asset2_50_withdraw_years_inf_2percent = load_dump(asset1_50_asset2_50_withdraw_years_inf_2percent_dump_dir,
                                                               "withdraw_rates",
                                                               "success_rates")
    loaded_dic_asset1_25_asset2_75_withdraw_years_inf_2percent = load_dump(asset1_25_asset2_75_withdraw_years_inf_2percent_dump_dir,
                                                               "withdraw_rates",
                                                               "success_rates")
    loaded_dic_asset1_0_asset2_100_withdraw_years_inf_2percent = load_dump(asset1_0_asset2_100_withdraw_years_inf_2percent_dump_dir,
                                                               "withdraw_rates",
                                                               "success_rates")
    # plot
    fig = pyplot.figure(facecolor='w', linewidth=1, edgecolor='w', tight_layout=True)
    ax = fig.add_subplot(111, xlabel="Withdraw Rate", ylabel="Success Rate")
    ax.set_title(f"success rates of withdraw {withdraw_years} years({asset1} & {asset2})")

    pyplot.plot(loaded_dic_asset1_100_asset2_0_withdraw_years_inf_2percent["withdraw_rates"],
                loaded_dic_asset1_100_asset2_0_withdraw_years_inf_2percent["success_rates"],
                label=f"{asset1} 100%", color="black")
    pyplot.plot(loaded_dic_asset1_75_asset2_25_withdraw_years_inf_2percent["withdraw_rates"],
                loaded_dic_asset1_75_asset2_25_withdraw_years_inf_2percent["success_rates"],
                label=f"{asset1} 75%, {asset2} 25%", color="blue")
    pyplot.plot(loaded_dic_asset1_50_asset2_50_withdraw_years_inf_2percent["withdraw_rates"],
                loaded_dic_asset1_50_asset2_50_withdraw_years_inf_2percent["success_rates"],
                label=f"{asset1} 50%, {asset2} 50%", color="orange")
    pyplot.plot(loaded_dic_asset1_25_asset2_75_withdraw_years_inf_2percent["withdraw_rates"],
                loaded_dic_asset1_25_asset2_75_withdraw_years_inf_2percent["success_rates"],
                label=f"{asset1} 25%, {asset2} 75%", color="green")
    pyplot.plot(loaded_dic_asset1_0_asset2_100_withdraw_years_inf_2percent["withdraw_rates"],
                loaded_dic_asset1_0_asset2_100_withdraw_years_inf_2percent["success_rates"],
                label=f"{asset2} 100%", color="red")

    ax.set_ylim(ymin, 1)
    ax.set_xlim(0, .06)
    ax.set_xticks([i / 100 for i in range(0, 7, 1)])
    ax.minorticks_on()
    ax.xaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator(4))
    ax.grid()
    ax.xaxis.tick_top()
    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    pyplot.legend()
    ax.text(.5, .5, "generated by lapi\n@Weibo, @Zhihu, @Note", transform=ax.transAxes,
            fontsize=30, color='gray', alpha=0.3,
            ha='center', va='center', rotation=30)
    pyplot.savefig(out_dir + f"{asset1}_{asset2}_withdraw_siumlation_{withdraw_years}_years.png")

if __name__ == '__main__':
    starttime = time.time()
    print("start: {}".format(datetime.datetime.fromtimestamp(starttime).strftime("%H:%M:%S")))
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for withdraw_years in range(30, 70, 10):
        plot_success_rates_in_different_withdraw_rates_with_multiple_ratio("SPXL", "CASH", withdraw_years, ymin=0)
        plot_success_rates_in_different_withdraw_rates_with_multiple_ratio("SPXL", "BONDS", withdraw_years, ymin=0)
        plot_success_rates_in_different_withdraw_rates_with_multiple_ratio("SSO", "CASH", withdraw_years, ymin=0)
        plot_success_rates_in_different_withdraw_rates_with_multiple_ratio("SSO", "BONDS", withdraw_years, ymin=0)
        plot_success_rates_in_different_withdraw_rates_with_multiple_ratio("SPX", "CASH", withdraw_years, ymin=0)
        plot_success_rates_in_different_withdraw_rates_with_multiple_ratio("SPX", "BONDS", withdraw_years, ymin=0)
        plot_success_rates_in_different_withdraw_rates_with_multiple_ratio("SPXL", "SPX", withdraw_years, ymin=0)
        plot_success_rates_in_different_withdraw_rates_with_multiple_ratio("SSO", "SPX", withdraw_years, ymin=0)


    print("end: {}".format(datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")))
    time1 = time.time()
    print("経過秒数：{}".format(int(time1 - starttime)))
