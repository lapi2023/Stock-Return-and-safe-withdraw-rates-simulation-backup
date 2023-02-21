import codecs
import datetime
import os
import time
import cnum
import tqdm as tqdm
from dateutil.relativedelta import relativedelta
from stock_calculation import utils

PJ_dir = "Return_Simulation/Return_Simulation_Timing/dollar_cost_averaging/"
asset_log_dir = PJ_dir + "asset_log/"
dump_dir = PJ_dir + "dump/"
out_dir = PJ_dir + "output/"
inflation_rate = 0

# dollar cost avaraging parameters:
monthly_invest_amount = 1000

def calculate_return_dollar_cost_averaging_monthly_single_try(sheet_tuple, startdate, invest_years, monthly_invest_amount, inflation_rate=0):

    startdate = utils.return_calculatable_date(sheet_tuple, startdate)
    current_month = startdate
    invested_amount = 0
    asset = 0
    invested_months = 0

    while utils.canbe_simulated_monthly(sheet_tuple, current_month, 1) and invested_months/12 < invest_years:
        asset += monthly_invest_amount
        invested_amount += monthly_invest_amount
        n1_price = sheet_tuple[utils.get_index(sheet_tuple, current_month)][1]
        current_month = utils.return_calculatable_date(sheet_tuple, current_month + relativedelta(months=1))
        n2_price = sheet_tuple[utils.get_index(sheet_tuple, current_month)][1]
        growth_rate = (n2_price - n1_price) / n1_price
        asset = int(asset * (1 + growth_rate) * (1 - inflation_rate))
        invested_months += 1
    return invested_amount, asset, invested_months
def calculate_return_dollar_cost_averaging_monthly_iterate(ticker, startdate: datetime, enddate: datetime, invest_years, monthly_invest_amount, inflation_rate=0, asset_log_dir =""):
    """
    use calculate_return_dollar_cost_averaging_monthly_single_try(ticker, startdate, enddate, invest_years, monthly_invest_amount, inflation_rate=0, asset_log_dir = "")
    iterate monthly
    """
    # initialize
    utils.make_dir(asset_log_dir)
    if asset_log_dir != "":
        asset_logfile = asset_log_dir + "{}_start_{}_invest_{}years_inflation_{:.1f}percent.txt".format(
        ticker, startdate.strftime("%Y%m%d"), invest_years, inflation_rate * 100)
        if (os.path.isfile(asset_logfile)):
            os.remove(asset_logfile)

    current_date = startdate
    month_count = 0
    asset_result_list = [] #何年から始めて資産がどのくらい残ったか
    asset_list = []
    sheet_tuple = utils.get_tuple_1886_monthly(ticker)
    # end initialization

    while utils.canbe_simulated_yearly(sheet_tuple, current_date, invest_years) and (current_date + relativedelta(years=invest_years) < enddate):
        month_count += 1
        print("case: {}, from {} to {}, {}".format(month_count, current_date.strftime("%Y/%m/%d"),
                                                   (current_date + relativedelta(years=invest_years)).strftime("%Y/%m/%d"),
                                                   datetime.datetime.fromtimestamp(
                time.time()).strftime("%H:%M:%S")), file=codecs.open(asset_logfile, "a", "utf-8"))
        invested_amount, asset, invested_months = calculate_return_dollar_cost_averaging_monthly_single_try(sheet_tuple, current_date, invest_years, monthly_invest_amount,
                                                                                       inflation_rate)

        asset_result_list.append([current_date, invest_years, invested_amount, asset, invested_months])
        asset_list.append(asset)
        print("{}円投資し、{}年後の資産は{}円({:.1f}倍)になりました".format(cnum.jp(int(invested_amount)), invest_years, cnum.jp(int(asset)), asset / invested_amount),
              file=codecs.open(asset_logfile, "a", "utf-8"))
        current_date = utils.return_calculatable_date(sheet_tuple, (current_date + relativedelta(months=1)).replace(day=1))
    return asset_result_list, asset_list
def generate_dumpfiles_dollar_cost_averaging_monthly(ticker, startdate: datetime, enddate, invest_years, monthly_invest_amount,
                                                     inflation_rate = 0, dump_dir = "", out_dir = "", asset_log_dir = ""):

    utils.make_dir(dump_dir)
    utils.make_dir(out_dir)
    asset_result_list, asset_list = calculate_return_dollar_cost_averaging_monthly_iterate(
        ticker, startdate, enddate, invest_years, monthly_invest_amount, inflation_rate, asset_log_dir)

    if dump_dir != "":
        utils.save_to_dump(dump_dir, asset_result_list=asset_result_list,
                     asset_list=asset_list,
                     )
    if out_dir != "":
        utils.save_results_to_txt(out_dir, asset_result_list=asset_result_list,
                     asset_list=asset_list,
                            )
    return asset_result_list, asset_list

if __name__ == '__main__':
    starttime = time.time()
    print("start: {}".format(datetime.datetime.fromtimestamp(starttime).strftime("%H:%M:%S")))

    SPX_tuple = utils.get_tuple_1886_monthly("SPX")
    startdate = SPX_tuple[0][0]
    enddate = SPX_tuple[-1][0]

    for ticker in ["SPX", "SPXL", "SSO"]:
        for invest_years in tqdm.tqdm([10, 20, 30, 40, 50], desc=f"{ticker}"):
            generate_dumpfiles_dollar_cost_averaging_monthly(ticker, startdate, enddate, invest_years, monthly_invest_amount, inflation_rate,
                                                             dump_dir + f"{ticker}_{invest_years}years/",
                                                             out_dir + f"{ticker}_{invest_years}years/",
                                                             asset_log_dir)

    print("end: {}".format(datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")))

    time1 = time.time()
    print("経過秒数：{}".format(int(time1 - starttime)))
