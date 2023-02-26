import datetime
import os
import statistics
import time

import cnum
import pandas
from stock_calculation import utils
from matplotlib import pyplot

out_dir = "graph_output/Return_Simulation/Return_Simulation_buy_low_sell_high/"

def plot_return_histogram(ticker, invest_years, target_annualized_return):
    dump_dir = f"Return_Simulation/Return_Simulation_Timing/buy_low_sell_high/dump/{ticker}_{invest_years}years_PERLow_{target_annualized_return}/"
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
        list = [i / 100 for i in range(4, 12, 1)]
        ax.table(cellText=df.values,
                 colLabels=df.columns,
                 colLoc="center",
                 colWidths=[1/(len(list) + 1)] * (len(list) + 1),
                 rowLabels=df.index,
                 rowLoc="center",
                 loc='center',
                 # bbox=[0, 0, 1, 1]
                 )
        ax.set_title(title)
        pyplot.savefig(outputPath)

    row_min_list = []
    row_mean_list = []
    row_median_list = []
    row_max_list = []
    row_sd_list = []
    row_sr_list = []
    row_invented_months_list = []
    row_avg_invested_amount_list = []
    row_sold_count = []

    for target_annualized_return in [i / 100 for i in range(4, 12, 1)]:
        dump_dir = f"Return_Simulation/Return_Simulation_Timing/buy_low_sell_high/dump/{ticker}_{invest_years}years_PERLow_{target_annualized_return}/"
        loaded_dic = utils.load_dump(dump_dir, "asset_list", "asset_result_list", "sold_count_list")
        asset_list = loaded_dic["asset_list"]
        asset_result_list = loaded_dic["asset_result_list"]
        sold_count_list = loaded_dic["sold_count_list"]
        row_min_list.append(f"{int(min(asset_list)):,}")
        row_mean_list.append(f"{int(statistics.mean(asset_list)):,}")
        row_median_list.append(f"{int(statistics.median(asset_list)):,}")
        row_max_list.append(f"{int(max(asset_list)):,}")
        row_sd_list.append(f"{int(statistics.stdev(asset_list)):,}")
        row_sr_list.append(f"{statistics.median(asset_list)/statistics.stdev(asset_list):,.2f}")
        row_invented_months_list.append(asset_result_list[0][1])
        row_avg_invested_amount_list.append(f"{int(asset_result_list[0][2]/asset_result_list[0][1]):,}")
        row_sold_count.append(f"{statistics.mean(sold_count_list):,.1f}")

    table_list = [
        row_min_list,
        row_mean_list,
        row_median_list,
        row_max_list,
        row_sd_list,
        row_sr_list,
        row_invented_months_list,
        row_avg_invested_amount_list,
        row_sold_count
    ]
    print(table_list)
    df = pandas.DataFrame(
        data=table_list,
        index = ["min", "average", "median", "max","SD", "Sharpe Ratio(med/SD)", "invested count", "avg. invested amount", "sold count"],
        columns = [str(i) + "%" for i in range(4, 12, 1)]
                     )
    utils.make_dir(out_dir + "table/")
    table_plot(df, f"{ticker}_{invest_years}", out_dir + f"table/{ticker}_{invest_years}_table.png", )

def plot_table_by_PERs_median(ticker, invest_years):
    def table_plot(df, title, outputPath):
        fig, ax = pyplot.subplots()
        ax.axis('off')

        ax.table(cellText=df.values,
                 colLabels=df.columns,
                 colLoc="center",
                 # colWidths=[1/(len(list) + 1)] * (len(list) + 1),
                 rowLabels=df.index,
                 rowLoc="center",
                 loc='center',
                 # bbox=[0, 0, 1, 1]
                 )
        ax.set_title(title)
        ax.text(.5, .5, "generated by lapi\n@Weibo, @Zhihu, @Note", transform=ax.transAxes,
                fontsize=30, color='gray', alpha=0.3,
                ha='center', va='center', rotation=30)
        pyplot.savefig(outputPath)

    PER_threshold_low_list = [7, 9, 11, 13]
    PER_threshold_high_list = [17, 19, 21, 23, 25, 27, 29, 99999999]  # 99999999 means never sell
    table_data = []
    row = []
    for PER_threshold_low in PER_threshold_low_list:
        row = []
        for PER_threshold_high in PER_threshold_high_list:

            dump_dir = f"Return_Simulation/Return_Simulation_Timing/buy_low_sell_high/dump/{ticker}_{invest_years}years_PERLow_{PER_threshold_low}_" \
                       f"PERHigh_{PER_threshold_high}/"
            asset_list = utils.load_dump(dump_dir, "asset_list")["asset_list"]
            row.append(f"{int(statistics.median(asset_list)):,}")
        table_data.append(row)

    print(table_data)
    df = pandas.DataFrame(
        data=table_data,
        index = PER_threshold_low_list,
        columns = [17, 19, 21, 23, 25, 27, 29, "never sell"]
                     )
    utils.make_dir(out_dir + "table/")
    table_plot(df, f"{ticker} {invest_years}years (without dividends) buy at low sell at high by PER\n"
                   f"median by column:PER_threshold_high, row: PER_threshold_low", out_dir + f"table/{ticker}_{invest_years}_table_PERs_median.png", )

def plot_table_by_PERs_SR(ticker, invest_years):
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

    PER_threshold_low_list = [7, 9, 11, 13]
    PER_threshold_high_list = [17, 19, 21, 23, 27, 29]  # 99999999 means never sell

    table_data = []
    for PER_threshold_low in PER_threshold_low_list:
        row = []
        for PER_threshold_high in PER_threshold_high_list:

            dump_dir = f"Return_Simulation/Return_Simulation_Timing/buy_low_sell_high/dump/{ticker}_{invest_years}years_PERLow_{PER_threshold_low}_" \
                       f"PERHigh_{PER_threshold_high}/"
            asset_list = utils.load_dump(dump_dir, "asset_list")["asset_list"]
            row.append(f"{statistics.median(asset_list)/statistics.stdev(asset_list):.1f}")
        table_data.append(row)


    print(table_data)
    df = pandas.DataFrame(
        data=table_data,
        index = PER_threshold_low_list,
        columns = PER_threshold_high_list
                     )
    utils.make_dir(out_dir + "table/")
    table_plot(df, f"{ticker} {invest_years}years (without dividends)  buy at low sell at high by PER\n"
                   f"Sharpe Ratio by column:PER_threshold_high, row: PER_threshold_low", out_dir + f"table/{ticker}_{invest_years}_table_PERs_SR.png", )

def plot_table_summary(ticker, invest_years, PER_threshold_list):
    def table_plot(df, title, outputPath):
        fig, ax = pyplot.subplots(figsize=(6.8,4.8))
        ax.axis('off')
        tab = ax.table(cellText=df.values,
                 colLabels=df.columns,
                 colLoc="center",
                 rowLabels=df.index,
                 rowLoc="center",
                 loc='center',
                 )
        tab.auto_set_column_width(col=list(range(len(df.columns))))
        ax.set_title(title)
        ax.text(.5, .5, "generated by lapi\n@Weibo, @Zhihu, @Note", transform=ax.transAxes,
                fontsize=30, color='gray', alpha=0.3,
                ha='center', va='center', rotation=30)
        pyplot.savefig(outputPath)

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
    for PER_threshold_low, PER_threshold_high in PER_threshold_list:
            dump_dir = f"Return_Simulation/Return_Simulation_Timing/buy_low_sell_high/dump/{ticker}_{invest_years}years_PERLow_{PER_threshold_low}_" \
                       f"PERHigh_{PER_threshold_high}/"
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
            columns.append(f"PER{PER_threshold_low}-{PER_threshold_high}")
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

    print(table_data)
    df = pandas.DataFrame(
        data=table_data,
        index = ["min", "average", "median", "max","SD", "Sharpe Ratio(avg/SD)", "invested count", "avg. invested amount", "sold count"],
        columns = columns
                     )
    utils.make_dir(out_dir + "table/")
    table_plot(df, f"{ticker} {invest_years}years(without dividends) buy at low sell at high by PER\n"
                   f"Sharpe Ratio by column:PER_threshold_high, row: PER_threshold_low", out_dir + f"table/{ticker}_{invest_years}_table_PERs_summary.png", )


if __name__ == '__main__':
    starttime = time.time()
    print("start: {}".format(datetime.datetime.fromtimestamp(starttime).strftime("%H:%M:%S")))
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    # for ticker in ["SPX"]:
    #     for invest_years in [30]:
    #         plot_table(ticker, invest_years)
    # for ticker in ["SPX", "SPXL", "SSO"]:
    #     for invest_years in range(10, 60, 10):
    #         plot_return_histogram(ticker, invest_years)

    plot_table_by_PERs_median("SPX", 30)
    plot_table_by_PERs_SR("SPX", 30)
    plot_table_summary("SPX", 30, [(7, 17), (11, 23), (13, 17),  (13, 29)])
    print("end: {}".format(datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")))
    time1 = time.time()
    print("経過秒数：{}".format(int(time1 - starttime)))
