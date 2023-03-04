import datetime
import os
import statistics
import time
import pandas
from stock_calculation import utils
from stock_calculation import utils_plot

out_dir = "graph_output/Return_Simulation/Return_Simulation_follow_the_herd/"
def plot_table_median(ticker, invest_years):

    change_rate_threshold_low_list = [i / 100 for i in range(-1, -11, -1)] + [-999]
    change_rate_threshold_high_list = [i / 100 for i in range(0, 11, 1)]
    table_data = []
    row = []
    for change_rate_threshold_low in change_rate_threshold_low_list:
        row = []
        for change_rate_threshold_high in change_rate_threshold_high_list:

            dump_dir = f"Return_Simulation/Return_Simulation_Timing/follow_the_herd/dump/{ticker}_{invest_years}years_" \
                       f"sellRate_{change_rate_threshold_low}_" \
                       f"buyRate_{change_rate_threshold_high}/"
            asset_list = utils.load_dump(dump_dir, "asset_list")["asset_list"]
            row.append(f"{statistics.median(asset_list):,.0f}")
        table_data.append(row)

    df = pandas.DataFrame(
        data=table_data,
        index = [f"{i:.0%}" for i in [i / 100 for i in range(-1, -11, -1)]] + ["Never sell"],
        columns = [f"{i:.0%}" for i in change_rate_threshold_high_list]
                     )
    utils.make_dir(out_dir + "table/")
    utils_plot.table_plot(df, f"{ticker} {invest_years}years (without dividends) follow the herd\n"
                   f"median by column:change_rate_threshold_high\n"
                   f"row: change_rate_threshold_low", out_dir + f"table/{ticker}_{invest_years}_table_median.png", )
def plot_table_SR(ticker, invest_years):
    change_rate_threshold_low_list = [i / 100 for i in range(-1, -11, -1)] + [-999]
    change_rate_threshold_high_list = [i / 100 for i in range(0, 11, 1)]
    table_data = []
    row = []
    for change_rate_threshold_low in change_rate_threshold_low_list:
        row = []
        for change_rate_threshold_high in change_rate_threshold_high_list:
            dump_dir = f"Return_Simulation/Return_Simulation_Timing/follow_the_herd/dump/{ticker}_{invest_years}years_" \
                       f"sellRate_{change_rate_threshold_low}_" \
                       f"buyRate_{change_rate_threshold_high}/"
            asset_list = utils.load_dump(dump_dir, "asset_list")["asset_list"]
            row.append(f"{statistics.median(asset_list)/statistics.stdev(asset_list):.1f}")
        table_data.append(row)


    df = pandas.DataFrame(
        data=table_data,
        index=[f"{i:.0%}" for i in [i / 100 for i in range(-1, -11, -1)]] + ["Never sell"],
        columns=[f"{i:.0%}" for i in change_rate_threshold_high_list]
    )
    utils.make_dir(out_dir + "table/")
    utils_plot.table_plot(df, f"{ticker} {invest_years}years (without dividends) follow the herd\n"
                              f"Sharpe Ratio by column:change_rate_threshold_high row: change_rate_threshold_low",
                          out_dir + f"table/{ticker}_{invest_years}_table_SR.png", )
def plot_table_summary(ticker, invest_years, change_rate_threshold_list):

    row_min = []
    row_mean = []
    row_median = []
    row_max = []
    row_stddev = []
    row_SR = []
    row_invested_count = []
    row_avg_invested_amount = []
    row_sold_count = []
    columns = []
    for change_rate_threshold_low, change_rate_threshold_high in change_rate_threshold_list:
            dump_dir = f"Return_Simulation/Return_Simulation_Timing/follow_the_herd/dump/{ticker}_{invest_years}years_" \
                   f"sellRate_{change_rate_threshold_low}_" \
                   f"buyRate_{change_rate_threshold_high}/"
            asset_list = utils.load_dump(dump_dir, "asset_list")["asset_list"]
            invested_months_list = utils.load_dump(dump_dir, "invested_months_list")["invested_months_list"]
            invested_amount_list = utils.load_dump(dump_dir, "invested_amount_list")["invested_amount_list"]
            sold_count_list = utils.load_dump(dump_dir, "sold_count_list")["sold_count_list"]
            row_min.append(f"{(min(asset_list)):,}")
            row_mean.append(f"{statistics.mean(asset_list):,.0f}")
            row_median.append(f"{statistics.median(asset_list):,.0f}")
            row_max.append(f"{max(asset_list):,}")
            row_stddev.append(f"{statistics.stdev(asset_list):,.0f}")
            row_SR.append(f"{statistics.median(asset_list)/statistics.stdev(asset_list):.1f}")
            row_invested_count.append(f"{statistics.mean(invested_months_list):.1f}")
            row_avg_invested_amount.append(f"{statistics.mean(invested_amount_list)/statistics.mean(invested_months_list):,.0f}")
            row_sold_count.append(f"{statistics.mean(sold_count_list):,.1f}")
            if change_rate_threshold_high == 999:
                columns.append(f"buy after {change_rate_threshold_low:.0%}, Never sell")
            else:
                columns.append(f"rate:{change_rate_threshold_low:.0%}-{change_rate_threshold_high:.0%}")
    table_data = [
        row_min,
        row_mean,
        row_median,
        row_max,
        row_stddev,
        row_SR,
        row_invested_count,
        row_avg_invested_amount,
        row_sold_count
    ]

    df = pandas.DataFrame(
        data=table_data,
        index = ["min", "average", "median", "max","SD", "Sharpe Ratio(avg/SD)", "invested count", "avg. invested amount", "sold count"],
        columns = columns
                     )
    utils.make_dir(out_dir + "table/")
    utils_plot.table_plot(df, f"{ticker} {invest_years}years(without dividends) buy after falling\n",
                            out_dir + f"table/{ticker}_{invest_years}_table_summary.png" )

if __name__ == '__main__':
    starttime = time.time()
    print("start: {}".format(datetime.datetime.fromtimestamp(starttime).strftime("%H:%M:%S")))
    utils.make_dir(out_dir)

    plot_table_median("SPX", 30)
    plot_table_SR("SPX", 30)
    plot_table_summary("SPX", 30, [(-0.02, 0.1), (-0.05, 0.01)])
    print("end: {}".format(datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")))
    time1 = time.time()
    print("経過秒数：{}".format(int(time1 - starttime)))
