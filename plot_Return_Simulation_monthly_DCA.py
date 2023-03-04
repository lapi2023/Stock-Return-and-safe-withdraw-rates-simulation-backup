import datetime
import os
import statistics
import time
import pandas
from stock_calculation import utils
from matplotlib import pyplot

out_dir = "graph_output/Return_Simulation/Return_Simulation_monthly_DCA/"

def plot_return_histogram(ticker, invest_years):
    dump_dir = f"Return_Simulation/Return_Simulation_Timing/dollar_cost_averaging/dump/{ticker}_{invest_years}years/"
    loaded_dic = utils.load_dump(dump_dir, "asset_list", "asset_result_list")
    asset_list = loaded_dic["asset_list"]
    asset_result_list = loaded_dic["asset_result_list"]
    # plot
    pyplot.hist(
        asset_list,
        bins = 500,
    )
    pyplot.xlim()

    utils.make_dir(out_dir + "hist/")
    pyplot.savefig(out_dir + f"hist/{ticker}_{invest_years}years_hist.png")

def plot_table(ticker, invest_years):
    def table_plot(df, title, outputPath):
        fig, ax = pyplot.subplots()
        ax.axis('off')

        ax.table(cellText=df.values,
                 colLabels=df.columns,
                 colLoc="center",
                 rowLabels=df.index,
                 rowLoc="center",
                 loc='center',
                 )
        ax.set_title(title)
        ax.text(.5, .5, "generated by lapi\n@Weibo, @Zhihu, @Note", transform=ax.transAxes,
                fontsize=30, color='gray', alpha=0.3,
                ha='center', va='center', rotation=30)
        pyplot.savefig(outputPath)

    dump_dir = f"Return_Simulation/Return_Simulation_Timing/dollar_cost_averaging/dump/{ticker}_{invest_years}years/"
    loaded_dic = utils.load_dump(dump_dir, "asset_list", "asset_result_list")
    asset_list = loaded_dic["asset_list"]
    asset_result_list = loaded_dic["asset_result_list"]
    table_list = [
        [f"{int(min(asset_list)):,}"],
        [f"{int(statistics.mean(asset_list)):,}"],
        [f"{int(statistics.median(asset_list)):,}"],
        [f"{int(max(asset_list)):,}"],
        [f"{int(statistics.stdev(asset_list)):,}"],
        [f"{statistics.mean(asset_list)/statistics.stdev(asset_list):,.2f}"],
        [asset_result_list[0][4]],
        [f"{int(asset_result_list[0][2]/asset_result_list[0][4]):,}"],
        [0]
    ]
    print(table_list)
    df = pandas.DataFrame(
        data=table_list,
        index = ["min", "average", "median", "max","SD", "Sharpe Ratio(avg/SD)", "invested count", "avg. invested amount", "sold count"],
        columns = ["DCA"]
                     )
    utils.make_dir(out_dir + "table/")
    table_plot(df, f"{ticker} {invest_years} years, Dollar Cost Averaging\n"
                   f"monthly_income: 1,000, data from 1886-2023", out_dir + f"table/{ticker}_{invest_years}_table.png", )

if __name__ == '__main__':
    starttime = time.time()
    print("start: {}".format(datetime.datetime.fromtimestamp(starttime).strftime("%H:%M:%S")))
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    for ticker in ["SPX", "SPXL", "SSO"]:
        for invest_years in range(10, 60, 10):
            plot_table(ticker, invest_years)
    # for ticker in ["SPX", "SPXL", "SSO"]:
    #     for invest_years in range(10, 60, 10):
    #         plot_return_histogram(ticker, invest_years)
    # plot_return_histogram("SPX", 30)

    print("end: {}".format(datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")))
    time1 = time.time()
    print("経過秒数：{}".format(int(time1 - starttime)))