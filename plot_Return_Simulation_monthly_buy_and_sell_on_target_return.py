import datetime
import os
import statistics
import time

import pandas

from stock_calculation import utils, utils_plot

out_dir = "graph_output/Return_Simulation/Return_Simulation_buy_and_sell_on_target_return/"


def plot_table_median(ticker, invest_years):
    target_annualized_return_threshold_low_list = [i / 100 for i in range(-11, 0, 1)]  # -1 means never sell
    target_annualized_return_threshold_high_list = [i / 100 for i in range(4, 12, 1)] + [999]  # 999 means never sell
    table_data = []
    row = []
    for target_annualized_return_threshold_low in target_annualized_return_threshold_low_list:
        row = []
        for target_annualized_return_threshold_high in target_annualized_return_threshold_high_list:
            dump_dir = f"Return_Simulation/Return_Simulation_Timing/buy_and_sell_on_target_return/dump/{ticker}_{invest_years}years_" \
                       f"annualizedReturnLow_{target_annualized_return_threshold_low}_" \
                       f"annualizedReturnHigh_{target_annualized_return_threshold_high}/"
            asset_list = utils.load_dump(dump_dir, "asset_list")["asset_list"]
            row.append(f"{int(statistics.median(asset_list)):,}")
        table_data.append(row)

    df = pandas.DataFrame(
        data=table_data,
        index=[f"{i / 100:.0%}" for i in range(-11, 0, 1)],
        columns=[f"{i / 100:.0%}" for i in range(4, 12, 1)] + ["never sell"]
    )
    utils.make_dir(out_dir + "table/")
    utils_plot.table_plot(df, f"{ticker} {invest_years}years sell on target annualized return\n"
                              f"median by column: return_threshold_high, row: return_threshold_low",
                          out_dir + f"table/{ticker}_{invest_years}_table_median.png")


def plot_table_SR(ticker, invest_years):
    target_annualized_return_threshold_low_list = [i / 100 for i in range(-11, 0, 1)]  # -1 means never sell
    target_annualized_return_threshold_high_list = [i / 100 for i in range(4, 12, 1)] + [999]  # 999 means never sell
    table_data = []
    row = []
    for target_annualized_return_threshold_low in target_annualized_return_threshold_low_list:
        row = []
        for target_annualized_return_threshold_high in target_annualized_return_threshold_high_list:
            dump_dir = f"Return_Simulation/Return_Simulation_Timing/buy_and_sell_on_target_return/dump/{ticker}_{invest_years}years_" \
                       f"annualizedReturnLow_{target_annualized_return_threshold_low}_" \
                       f"annualizedReturnHigh_{target_annualized_return_threshold_high}/"
            asset_list = utils.load_dump(dump_dir, "asset_list")["asset_list"]
            row.append(f"{statistics.mean(asset_list) / statistics.stdev(asset_list):.1f}")
        table_data.append(row)

    df = pandas.DataFrame(
        data=table_data,
        index=[f"{i / 100:.0%}" for i in range(-11, 0, 1)],
        columns=[f"{i / 100:.0%}" for i in range(4, 12, 1)] + ["never sell"]
    )
    utils.make_dir(out_dir + "table/")
    utils_plot.table_plot(df, f"{ticker} {invest_years}years sell on target annualized return, Sharpe Ratio\n"
                              f"column: return_threshold_high, row: return_threshold_low",
                          out_dir + f"table/{ticker}_{invest_years}_SR.png")


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
    for target_annualized_return_threshold_low, target_annualized_return_threshold_high in change_rate_threshold_list:
        dump_dir = f"Return_Simulation/Return_Simulation_Timing/buy_and_sell_on_target_return/dump/{ticker}_{invest_years}years_" \
                   f"annualizedReturnLow_{target_annualized_return_threshold_low}_" \
                   f"annualizedReturnHigh_{target_annualized_return_threshold_high}/"
        asset_list = utils.load_dump(dump_dir, "asset_list")["asset_list"]
        sold_count_list = utils.load_dump(dump_dir, "sold_count_list")["sold_count_list"]
        row_min.append(f"{(min(asset_list)):,}")
        row_mean.append(f"{statistics.mean(asset_list):,.0f}")
        row_median.append(f"{statistics.median(asset_list):,.0f}")
        row_max.append(f"{max(asset_list):,}")
        row_stddev.append(f"{statistics.stdev(asset_list):,.0f}")
        row_SR.append(f"{statistics.median(asset_list) / statistics.stdev(asset_list):.1f}")
        row_invested_count.append(f"{invest_years * 12:.1f}")
        row_avg_invested_amount.append(f"{invest_years * 12 * 1000:,.0f}")
        row_sold_count.append(f"{statistics.mean(sold_count_list):,.1f}")
        columns.append(
            f"rate:{target_annualized_return_threshold_low:.0%}-{target_annualized_return_threshold_high:.0%}")

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
    utils_plot.table_plot(df, f"{ticker} {invest_years}years(without dividends) sell on target annualized return\n",
                          out_dir + f"table/{ticker}_{invest_years}_summary.png")


if __name__ == '__main__':
    starttime = time.time()
    print("start: {}".format(datetime.datetime.fromtimestamp(starttime).strftime("%H:%M:%S")))
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for ticker in ["SPX", "SPXL", "SSO"]:
        for year in [30]:
            plot_table_median(ticker, year)
            plot_table_SR(ticker, year)
            plot_table_summary(ticker, year, [(-.01, .04), (-.07, .08), (-.11, .11)])
    print("end: {}".format(datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")))
    time1 = time.time()
    print("経過秒数：{}".format(int(time1 - starttime)))
