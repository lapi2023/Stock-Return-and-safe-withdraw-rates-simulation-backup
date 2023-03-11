import datetime
import os
import statistics
import time

import pandas

from stock_calculation import utils, utils_plot

out_dir = "graph_output/Return_Simulation/buy_on_golden_cross_derived_alpha/"


def plot_table_summary(ticker, invest_years, SMA_list):
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
    for SMA in SMA_list:
        dump_dir = f"Return_Simulation/Return_Simulation_Timing/buy_on_golden_cross_derived_alpha/dump/{ticker}_{invest_years}years_" \
                   f"SMA_{SMA}/"
        print(dump_dir)
        asset_list = utils.load_dump(dump_dir, "asset_list")["asset_list"]
        sold_count_list = utils.load_dump(dump_dir, "sold_count_list")["sold_count_list"]
        invested_months_list = utils.load_dump(dump_dir, "invested_months_list")["invested_months_list"]
        invested_amount_list = utils.load_dump(dump_dir, "invested_amount_list")["invested_amount_list"]
        row_min.append(f"{(min(asset_list)):,}")
        row_mean.append(f"{statistics.mean(asset_list):,.0f}")
        row_median.append(f"{statistics.median(asset_list):,.0f}")
        row_max.append(f"{max(asset_list):,}")
        row_stddev.append(f"{statistics.stdev(asset_list):,.0f}")
        row_SR.append(f"{statistics.median(asset_list) / statistics.stdev(asset_list):.1f}")
        row_invested_count.append(f"{statistics.mean(invested_months_list):.1f}")
        row_avg_invested_amount.append(f"{statistics.mean(invested_amount_list):,.0f}")
        row_sold_count.append(f"{statistics.mean(sold_count_list):,.1f}")
        columns.append(f"SMA: {SMA}")

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
        index=["min", "average", "median", "max", "SD", "Sharpe Ratio(avg/SD)", "invested count",
               "avg. invested amount", "sold count"],
        columns=columns
    )
    utils.make_dir(out_dir + "table/")
    utils_plot.table_plot(df, f"{ticker} {invest_years}years(without dividends) SMA trend method\n",
                          out_dir + f"table/{ticker}_{invest_years}_summary.png")


if __name__ == '__main__':
    starttime = time.time()
    print("start: {}".format(datetime.datetime.fromtimestamp(starttime).strftime("%H:%M:%S")))
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    SMA_list = [25, 50, 200]
    for ticker in ["SPX", "SPXL", "SSO"]:
        for year in [30, 10, 20, 40, 50]:
            plot_table_summary(ticker, year, SMA_list)
    print("end: {}".format(datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")))
    time1 = time.time()
    print("経過秒数：{}".format(int(time1 - starttime)))
