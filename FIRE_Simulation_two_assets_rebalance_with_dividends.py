import codecs
import csv
import datetime
import math
import os
import statistics
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import cnum
import joblib
import tqdm as tqdm
from dateutil.relativedelta import relativedelta

SPXL_Sheets = r"Price Sheet\simulated_SPXL_1928-2023_monthly_with_dividends.csv"
SPX_Sheets = r"Price Sheet\simulated_SPX_funds_1928-2023_monthly_with_dividends.csv"
SSO_Sheets = r"Price Sheet\simulated_SSO_1928-2023_monthly_with_dividends.csv"
BONDS_Sheets = r"Price Sheet\simulated_us_bonds_monthly.csv"
CASH_Sheets = r"Price Sheet\cash_monthly_1928.csv"
asset_log_dir = "FIRE_Simulation\\two_assets_rebalance_with_dividends\\asset_log\\"
initial_asset = 1000 * 10000
inflation_rate = 0.02


def readCSV(path):
    list = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            list.append(tuple([datetime.datetime.strptime(row['date'], "%Y/%m/%d"), float(row['price'])]))
    return tuple(list)


def get_index(sheet, datetime: datetime):
    index = 0
    for row in sheet:
        if row[0] == datetime:
            break
        index += 1

    if index >= len(sheet):
        return -1
    else:
        return index


def canbe_simulated(sheet, startdate: datetime, withdraw_years):
    if startdate + relativedelta(years=withdraw_years) > sheet[-1][0]:

        return False  # 開始日付+継続年数(withdraw_years)のレコードがシートにないため-1を返して終了
    else:
        return True


def return_calculatable_startdate(sheet_tuple, startdate):
    if get_index(sheet_tuple, startdate) >= 0:
        return startdate
    else:
        for i in range(1, 6, 1):
            current_date_temp = startdate + relativedelta(days=i)
            if get_index(sheet_tuple, current_date_temp) >= 0:
                return current_date_temp
        for i in range(1, 6, 1):
            current_date_temp = startdate - relativedelta(days=i)
            if get_index(sheet_tuple, current_date_temp) >= 0:
                return current_date_temp
        for i in range(1, len(sheet_tuple), 1):
            current_date_temp = startdate + relativedelta(days=i)
            if get_index(sheet_tuple, current_date_temp) >= 0:
                return current_date_temp
    if get_index(sheet_tuple, current_date_temp) < 0:
        print('Error73: date not found! {}, {}'.format(current_date_temp, startdate), file=sys.stderr)


def save_to_dump(dump_dir, **kwargs):  # "withdraw_rates" = withdrawrates  ([])
    for key in kwargs.keys():
        joblib.dump(kwargs[key], dump_dir + key + ".dump")
        # joblib.dump(withdraw_rates, dump_dir + "withdraw_rates.dump")


def save_results_to_txt(out_dir, **kwargs):
    for key in kwargs.keys():
        print(kwargs[key], file=codecs.open(out_dir + "{}.txt".format(key), "w", "utf-8"))


def load_dump(dump_dir, *args):
    loaded_dic = {}
    for filename in args:
        if (os.path.isfile(dump_dir + filename + ".dump")):
            object = joblib.load(dump_dir + filename + ".dump")
            loaded_dic[filename] = object
            print("{} loaded: {}".format(filename, object))
        else:
            loaded_dic[filename] = []
    return loaded_dic


def simulate_once_a_year_two_assets_single_with_rebalancing(sheet1, percentage1, sheet2, percentage2,
                                                            startdate: datetime, withdraw_years,
                                                            initial_assets, withdraw_rate, inflation_rate=0.02):
    # 条件：最初の1年経過時点で初めてwithdraw_rateで資産を取り出す(最初の取り出しは行わない）
    # n年時規定されたPercentageを超えた資産から取り出す
    current_asset1 = int(initial_assets * percentage1)
    current_asset2 = int(initial_assets * percentage2)
    current_asset = initial_assets

    current_date = return_calculatable_startdate(sheet1, startdate.replace(day=1))

    current_price1 = sheet1[get_index(sheet1, current_date)][1]
    current_price2 = sheet2[get_index(sheet2, current_date)][1]

    withdraw_asset = int(initial_assets * withdraw_rate)
    current_years = 0

    asset_min = current_asset
    asset_max = 0

    datasets_years = []
    datasets_assets = []
    datasets_years.append(current_years)
    datasets_assets.append(current_asset)

    current_date = return_calculatable_startdate(sheet1, current_date.replace(day=1) + relativedelta(years=1))
    while current_date < startdate + relativedelta(years=withdraw_years) - relativedelta(months=1):
        last_price1 = current_price1
        last_price2 = current_price2

        current_years += 1

        if get_index(sheet1, current_date) < 0:
            print('Error122: date not found! {}'.format(current_date), file=sys.stderr)
            return None, None, None, None

        current_price1 = sheet1[get_index(sheet1, current_date)][1]
        current_price2 = sheet2[get_index(sheet2, current_date)][1]
        growth_rate1 = (current_price1 - last_price1) / last_price1  # 資産増加率=(今年の価格-前年の価格)÷前年の価格
        growth_rate2 = (current_price2 - last_price2) / last_price2

        current_asset1 = current_asset1 * (1 + growth_rate1)
        current_asset2 = current_asset2 * (1 + growth_rate2)

        # 規定されたPercentageを超えた資産から取り出す
        if current_asset1 + current_asset2 == 0:
            return 0, 0, 0, current_years
        if current_asset1 / (current_asset1 + current_asset2) >= percentage1:
            current_asset1 = int((current_asset1 - withdraw_asset) * (1 - inflation_rate))
            if current_asset1 < 0:
                current_asset2 = int((current_asset2 + current_asset1) * (1 - inflation_rate))
                current_asset1 = 0
        else:
            current_asset2 = int((current_asset2 - withdraw_asset) * (1 - inflation_rate))
            if current_asset2 < 0:
                current_asset1 = int((current_asset1 + current_asset2) * (1 - inflation_rate))
                current_asset2 = 0

        current_asset = current_asset1 + current_asset2

        datasets_years.append(current_years)
        datasets_assets.append(current_asset)

        if current_asset <= 0:
            return 0, 0, 0, current_years

        if asset_max < current_asset:
            asset_max = current_asset
        if asset_min > current_asset:
            asset_min = current_asset

        current_date = return_calculatable_startdate(sheet1, current_date.replace(day=1) + relativedelta(years=1))

    return int(current_asset), int(current_asset1), int(current_asset2), current_years


def simulate_once_a_year_two_assets_multi(sheet1, percentage1, sheet2, percentage2, startdate: datetime,
                                          enddate: datetime, withdraw_years, initial_assets,
                                          withdraw_rate, inflation_rate=0.02, asset_log_dir=""):
    # initialize
    if asset_log_dir != "":
        if not os.path.exists(asset_log_dir):
            os.makedirs(asset_log_dir)
        asset_logfile = asset_log_dir + "start_{}_withdraw_{}years_withdrawrate_{:.1f}percent.txt".format(
            startdate.strftime("%Y%m%d"), withdraw_years, withdraw_rate * 100)
    else:
        asset_logfile = ""

    if asset_logfile != "":
        if (os.path.isfile(asset_logfile)):
            os.remove(asset_logfile)

    current_date = startdate
    simulated_count = 0
    success_count = 0
    failure_count = 0
    multi_results = []  # 施行結果リスト

    asset_best_startdate = datetime.datetime(1000, 1, 1)  # 最後の資産が残った額が最大値に達した時の運用開始日
    asset_worst_startdate = datetime.datetime(1000, 1, 1)
    asset_max_final = 0
    asset_min_final = math.pow(initial_asset, 2)
    # end initialization

    while canbe_simulated(sheet1, current_date, withdraw_years) and (current_date < enddate):
        simulated_count += 1

        print(
            "case: {}, from:{}, initial asset: {}円, withdraw_rate: {:.1%}, asset1: {:.0%}, asset2: {:.0%}, {}".format(
                simulated_count, current_date.strftime("%Y/%m/%d"), cnum.jp(int(initial_asset)),
                withdraw_rate, percentage1, percentage2, datetime.datetime.fromtimestamp(
                    time.time()).strftime("%H:%M:%S")), file=codecs.open(asset_logfile, "a", "utf-8"))

        asset_final, final_asset1, final_asset2, simulated_years = simulate_once_a_year_two_assets_single_with_rebalancing(
            sheet1,
            percentage1,
            sheet2,
            percentage2,
            current_date,
            withdraw_years,
            initial_assets,
            withdraw_rate,
            inflation_rate)
        # asset:最後に残った資産額, asset_max:運用期間に記録した最大資産, end_year：最後に終わった年数(成功したら30を返す、失敗の場合は30未満), years & assets:何年経過後の資産額

        multi_results.append([current_date, asset_final, final_asset1, final_asset2, withdraw_rate, simulated_years])
        if asset_final <= 0:
            failure_count += 1
            if asset_logfile != "":
                print("Failed", file=codecs.open(asset_logfile, "a", "utf-8"))
            if asset_final < asset_min_final:
                asset_min_final = asset_final
                asset_worst_startdate = current_date
        else:
            success_count += 1
            print(
                f"Succeeded! assets: {cnum.jp(int(asset_final))}円、{withdraw_years}年後の資産は{(asset_final / initial_assets):.1f}倍になりました",
                file=codecs.open(asset_logfile, "a", "utf-8"))
        if asset_max_final < asset_final:
            asset_max_final = asset_final
            asset_best_startdate = current_date
        if asset_min_final > asset_final:
            asset_min_final = asset_final
            asset_worst_startdate = current_date

        current_date += relativedelta(months=1)

    return multi_results, simulated_count, success_count, asset_max_final, asset_best_startdate, asset_min_final, asset_worst_startdate


def generate_simulation_datasets_two_assets(sheet1_tuple, percentage1, sheet2_tuple, percentage2, startdate: datetime,
                                            enddate: datetime, withdraw_years, initial_assets,
                                            inflation_rate=0.02, dump_dir="", out_dir="", asset_log_dir=""):
    if dump_dir != "":
        if not os.path.exists(dump_dir):
            os.makedirs(dump_dir)
    if out_dir != "":
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
    if asset_log_dir != "":
        if not os.path.exists(asset_log_dir):
            os.makedirs(asset_log_dir)

    # load from saved files
    loaded_dic = load_dump(dump_dir, "withdraw_rates", "success_rates", "multi_results_list",
                           "assets_min_list", "assets_max_list",
                           "assets_avg_list", "assets_med_list", "asset_min_final_list", "asset_max_final_list",
                           "asset_best_startdate_list",
                           "asset_worst_startdate_list"
                           )
    multi_results_list = loaded_dic["multi_results_list"]
    withdraw_rates = loaded_dic["withdraw_rates"]
    success_rates = loaded_dic["success_rates"]
    assets_avg_list = loaded_dic["assets_avg_list"]
    assets_med_list = loaded_dic["assets_med_list"]
    assets_min_list = loaded_dic["assets_min_list"]
    assets_max_list = loaded_dic["assets_max_list"]
    asset_max_final_list = loaded_dic["asset_max_final_list"]
    asset_best_startdate_list = loaded_dic["asset_best_startdate_list"]
    asset_min_final_list = loaded_dic["asset_min_final_list"]
    asset_worst_startdate_list = loaded_dic["asset_worst_startdate_list"]
    # end loading

    # Start Simulation
    with ProcessPoolExecutor() as executor:
        if len(withdraw_rates) == 0:
            iterate_start = 0
        else:
            iterate_start = int((withdraw_rates[-1] + 0.0025) * 10000)

        for i in range(iterate_start, 625, 25):
            multi_results, simulated_count, success_count, asset_max_final, asset_best_startdate, asset_min_final, asset_worst_startdate = simulate_once_a_year_two_assets_multi(
                sheet1_tuple, percentage1, sheet2_tuple, percentage2, startdate,
                enddate, withdraw_years, initial_assets, i / 10000, inflation_rate,
                asset_log_dir
            )
            withdraw_rates.append(i / 10000)
            success_rates.append(success_count / simulated_count)
            multi_results_list.append(multi_results)

            # multi_results_list: [current_date, asset_final, final_asset1, final_asset2, withdraw_rate, simulated_years]
            asset_list = []
            for i in multi_results:
                asset_list.append(i[1])

            assets_avg_list.append(int(sum(asset_list) / len(asset_list)))
            assets_min_list.append(min(asset_list))
            assets_max_list.append(max(asset_list))
            assets_med_list.append(statistics.median(asset_list))
            asset_max_final_list.append(asset_max_final)
            asset_best_startdate_list.append(asset_best_startdate)
            asset_min_final_list.append(asset_min_final)
            asset_worst_startdate_list.append(asset_worst_startdate)

            save_to_dump(dump_dir, withdraw_rates=withdraw_rates, success_rates=success_rates,
                         multi_results_list=multi_results_list,
                         assets_avg_list=assets_avg_list, assets_min_list=assets_min_list,
                         assets_max_list=assets_max_list,
                         assets_med_list=assets_med_list, asset_max_final_list=asset_max_final_list,
                         asset_best_startdate_list=asset_best_startdate_list,
                         asset_min_final_list=asset_min_final_list,
                         asset_worst_startdate_list=asset_worst_startdate_list)

    # ファイルへの出力
    save_results_to_txt(out_dir, withdraw_rates=withdraw_rates, success_rates=success_rates,
                        multi_results_list=multi_results_list,
                        assets_avg_list=assets_avg_list, assets_min_list=assets_min_list,
                        assets_max_list=assets_max_list,
                        assets_med_list=assets_med_list, asset_max_final_list=asset_max_final_list,
                        asset_best_startdate_list=asset_best_startdate_list,
                        asset_min_final_list=asset_min_final_list,
                        asset_worst_startdate_list=asset_worst_startdate_list)

    return multi_results_list, withdraw_rates, success_rates, assets_avg_list, assets_min_list, assets_max_list


def simulate_two_assets_portfolio(ticker1, ticker2):
    def getTuple(ticker):
        match ticker:
            case "SPXL":
                return readCSV(SPXL_Sheets)
            case "SSO":
                return readCSV(SSO_Sheets)
            case "BONDS":
                return readCSV(BONDS_Sheets)
            case "CASH":
                return readCSV(CASH_Sheets)
            case "SPX":
                return readCSV(SPX_Sheets)
            case _:
                print("Ticker not definded!")
                return None

    tuple1 = getTuple(ticker1)
    tuple2 = getTuple(ticker2)
    startdate = tuple1[0][0]
    enddate = tuple1[-1][0]

    for ticker1_ratio in tqdm.tqdm([0, .25, .5, .75, 1], desc=f"{ticker1} & {ticker2}, calculate different ratios: "):
        for years in range(30, 70, 10):
            generate_simulation_datasets_two_assets(tuple1, ticker1_ratio, tuple2, 1 - ticker1_ratio,
                                                    startdate, enddate, years, initial_asset, inflation_rate,
                                                    f"FIRE_Simulation\\two_assets_rebalance_with_dividends\\{ticker1}{ticker1_ratio * 100}_{ticker2}{(1 - ticker1_ratio) * 100}_{years}years_inflation_{inflation_rate * 100}percent_dump\\",
                                                    f"FIRE_Simulation\\two_assets_rebalance_with_dividends\\{ticker1}{ticker1_ratio * 100}_{ticker2}{(1 - ticker1_ratio) * 100}_{years}years_inflation_{inflation_rate * 100}percent_output\\",
                                                    asset_log_dir + f"{ticker1}{ticker1_ratio * 100}_{ticker2}{(1 - ticker1_ratio) * 100}_{years}years_inflation_{inflation_rate * 100}percent_log\\"
                                                    )


if __name__ == '__main__':
    starttime = time.time()
    print("start: {}".format(datetime.datetime.fromtimestamp(starttime).strftime("%H:%M:%S")))

    '''
        dateについて：
        基本：datetime.datetime(yyyy, mm, dd)
        SPXL_tuple[0][0]：CSVファイルの一番最初の日付
        SPXL_tuple[-1][0]：CSVファイルの一番最後の日付
        date + relativedelta(years=n)：dateから数えてn年後
    '''

    simulate_two_assets_portfolio("SPXL", "BONDS")
    simulate_two_assets_portfolio("SPXL", "CASH")
    simulate_two_assets_portfolio("SSO", "BONDS")
    simulate_two_assets_portfolio("SSO", "CASH")
    simulate_two_assets_portfolio("SPX", "BONDS")
    simulate_two_assets_portfolio("SPX", "CASH")
    simulate_two_assets_portfolio("SPXL", "SPX")
    simulate_two_assets_portfolio("SSO", "SPX")

    time1 = time.time()
    print("経過秒数：{}".format(int(time1 - starttime)))
    print("end: {}".format(datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")))
