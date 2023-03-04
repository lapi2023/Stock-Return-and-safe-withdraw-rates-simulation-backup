import codecs
import datetime
import os
import time
import cnum
import tqdm as tqdm
from dateutil.relativedelta import relativedelta
from stock_calculation import utils

PJ_dir = "Return_Simulation/Return_Simulation_Timing/buy_on_golden_cross/"
asset_log_dir = PJ_dir + "asset_log/"
dump_dir = PJ_dir + "dump/"
out_dir = PJ_dir + "output/"
inflation_rate = 0

monthly_income = 1000


def calculate_return_monthly_buy_on_golden_cross_single_try(sheet_tuple, df, SMA_short, SMA_long, startdate, invest_years,
                                                        monthly_income, inflation_rate=0):
    startdate = utils.return_calculatable_date(sheet_tuple, startdate)
    current_month = startdate
    invested_asset = 0
    invested_months = 0
    wallet = monthly_income #最初は財布に貯めておく
    elapsed_months = 1
    sold_count = 0
    wallet_count = 1
    invested_amount = 0
    n1_price = sheet_tuple[utils.get_index(sheet_tuple, current_month)][1]
    while utils.canbe_simulated_monthly(sheet_tuple, current_month, 1) and elapsed_months / 12 < invest_years:
        n2_price = sheet_tuple[utils.get_index(sheet_tuple, current_month)][1]
        growth_rate = (n2_price - n1_price) / n1_price
        invested_asset = int(invested_asset * (1 + growth_rate) * (1 - inflation_rate))

        if utils.cross_type(df, SMA_short, SMA_long, current_month, sheet_tuple) == "GC":
            invested_asset += monthly_income + wallet
            wallet = 0
            invested_months += 1
            invested_amount = (wallet_count + invested_months) * monthly_income
        elif utils.cross_type(df, SMA_short, SMA_long, current_month, sheet_tuple) == "DC":
            wallet += monthly_income + invested_asset
            invested_asset = 0
            sold_count += 1
        else:
            wallet += monthly_income
            wallet_count += 1

        n1_price = n2_price
        current_month = utils.return_calculatable_date(sheet_tuple,
                                                       (current_month + relativedelta(months=1)).replace(day=1))
        elapsed_months += 1
    return invested_amount, invested_asset, wallet, invested_months, sold_count, elapsed_months


def calculate_return_monthly_buy_on_golden_cross_iterate(ticker, df, SMA_short, SMA_long, startdate: datetime,
                                                     enddate: datetime, invest_years, monthly_income, inflation_rate=0,
                                                     asset_log_dir=""):
    """
    calculate_return_monthly_buy_on_golden_cross_single_try(sheet_tuple, change_rate_threshold_low, change_rate_threshold_high, startdate, invest_years, monthly_income, inflation_rate=0):
    iterate monthly
    """
    # initialize
    utils.make_dir(asset_log_dir)
    if asset_log_dir != "":
        asset_logfile = asset_log_dir + "{}_start_{}_invest_{}years_inflation_{:.1f}percent_SMAshort_{}_SMAlong_{}.txt".format(
            ticker, startdate.strftime("%Y%m%d"), invest_years, inflation_rate * 100,
            SMA_short, SMA_long
        )
        if (os.path.isfile(asset_logfile)):
            os.remove(asset_logfile)

    current_date = startdate
    month_count = 0
    asset_result_list = []  # 何年から始めて資産がどのくらい残ったか
    asset_list = []
    invested_amount_list = []
    invested_months_list = []
    sold_count_list = []
    sheet_tuple = utils.get_tuple_1886_monthly(ticker)
    # end initialization

    while utils.canbe_simulated_yearly(sheet_tuple, current_date, invest_years) and (
            current_date + relativedelta(years=invest_years) < enddate):
        month_count += 1
        print("case: {}, from {} to {}, {}".format(month_count, current_date.strftime("%Y/%m/%d"),
                                                   (current_date + relativedelta(years=invest_years)).strftime(
                                                       "%Y/%m/%d"),
                                                   datetime.datetime.fromtimestamp(
                                                       time.time()).strftime("%H:%M:%S")),
              file=codecs.open(asset_logfile, "a", "utf-8"))
        invested_amount, invested_asset, wallet, invested_months, sold_count, elapsed_months = \
            calculate_return_monthly_buy_on_golden_cross_single_try(
                sheet_tuple, df, SMA_short, SMA_long, current_date, invest_years,
                monthly_income, inflation_rate)

        asset_result_list.append(
            [current_date, invest_years, invested_amount, invested_asset, wallet, invested_months, elapsed_months])
        asset_list.append(invested_asset + wallet)
        invested_amount_list.append(invested_amount)
        invested_months_list.append(invested_months)
        sold_count_list.append(sold_count)
        if invested_amount == 0:
            print("投資できませんでした", file=codecs.open(asset_logfile, "a", "utf-8"))
        else:
            print(f"{cnum.jp(int(invested_amount))}円投資し、{invest_years}年後の資産は"
                  f"{cnum.jp(int(invested_asset + wallet))}円({((invested_asset + wallet) / invested_amount):.1f}倍)になりました。"
                  f"投資回数：{invested_months}、財布内：{cnum.jp(int(wallet))}円、sold count: {sold_count}",
                  file=codecs.open(asset_logfile, "a", "utf-8"))
        current_date = utils.return_calculatable_date(sheet_tuple,
                                                      (current_date + relativedelta(months=1)).replace(day=1))
    return asset_result_list, asset_list, invested_amount_list, invested_months_list, sold_count_list

def generate_dumpfiles_monthly_buy_on_golden_cross(
        ticker, df, SMA_short, SMA_long, startdate: datetime, enddate, invest_years, monthly_income,
        inflation_rate=0, dump_dir="", out_dir="", asset_log_dir=""):
    utils.make_dir(dump_dir)
    utils.make_dir(out_dir)
    asset_result_list, asset_list, invested_amount_list, invested_months_list, sold_count_list = \
        calculate_return_monthly_buy_on_golden_cross_iterate(
            ticker, df, SMA_short, SMA_long, startdate, enddate, invest_years, monthly_income, inflation_rate, asset_log_dir
        )

    if dump_dir != "":
        utils.save_to_dump(
            dump_dir,
            asset_result_list=asset_result_list,
            asset_list=asset_list,
            invested_amount_list=invested_amount_list,
            invested_months_list=invested_months_list,
            sold_count_list=sold_count_list
        )
    if out_dir != "":
        utils.save_results_to_txt(out_dir,
                                  asset_result_list=asset_result_list,
                                  asset_list=asset_list,
                                  invested_amount_list=invested_amount_list,
                                  invested_months_list=invested_months_list,
                                  sold_count_list=sold_count_list
                                  )
    return asset_result_list, asset_list, invested_amount_list, invested_months_list, sold_count_list


if __name__ == '__main__':
    starttime = time.time()
    print("start: {}".format(datetime.datetime.fromtimestamp(starttime).strftime("%H:%M:%S")))
    SMA_short = 5
    SMA_long = 25


    SPX_tuple = utils.get_tuple_1886_monthly("SPX")
    SPX_daily_dataframe = utils.get_dataframe_1886_daily("SPX", SMA_short, SMA_long)
    startdate = utils.return_calculatable_date(SPX_tuple, SPX_tuple[0][0] + relativedelta(months=6))    #SMA長期のために6か月をバッファーとする
    enddate = SPX_tuple[-1][0]
    for ticker in ["SPX", "SPXL", "SSO"]:
        for invest_years in tqdm.tqdm([30, 10, 20, 40, 50],
                                      desc=f"{ticker}, calculate different invest years"):
            generate_dumpfiles_monthly_buy_on_golden_cross(
            ticker, SPX_daily_dataframe, SMA_short, SMA_long, startdate, enddate, invest_years, monthly_income, inflation_rate,
            dump_dir + f"{ticker}_{invest_years}years_SMAshort_{SMA_short}_SMAlong_{SMA_long}/",
            out_dir + f"{ticker}_{invest_years}years_SMAshort_{SMA_short}_SMAlong_{SMA_long}/",
            asset_log_dir)
                # for invest_years in tqdm.tqdm([10, 20, 30, 40, 50], desc=f"{ticker}, change rate{change_rate_threshold_low:.0%} - {change_rate_threshold_high:.0%}"):

    print("end: {}".format(datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")))

    time1 = time.time()
    print("経過秒数：{}".format(int(time1 - starttime)))
