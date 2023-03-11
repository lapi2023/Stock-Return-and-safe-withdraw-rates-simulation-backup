import codecs
import csv
import datetime
import math
import os
import statistics
import time
from concurrent.futures import ProcessPoolExecutor

import cnum
import joblib
import tqdm as tqdm
from dateutil.relativedelta import relativedelta

SPXL_Sheets = r"Price Sheet\simulated_SPX_funds_1886-2023_daily.csv"
SPX_Sheets = r"Price Sheet\simulated_SPX_funds_1886-2023_daily.csv"
SSO_Sheets = r"Price Sheet\simulated_SSO_1886-2023_daily.csv"
initial_asset = 1000 * 10000
asset_log_dir = "FIRE_Simulation\\single_asset\\asset_log\\"


def readCSV(path):
    list = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            # print([datetime.datetime.strptime(row['date'], "%Y/%m/%d"), float(row['SPXL'])])
            list.append(tuple([datetime.datetime.strptime(row['date'], "%Y/%m/%d"), float(row['price'])]))
    return tuple(list)


def simulate_once_a_year_single(sheet, startdate: datetime, withdraw_years, initial_assets, withdraw_rate,
                                inflation_rate=0):
    # 条件：最初の一カ月経過時点で初めてwithdraw_rateで資産を取り出す(最初の取り出しは行わない）
    current_asset = initial_assets
    current_date = startdate
    if get_index(sheet, current_date) < 0:
        return None, None, None, None, None, None
        # current_dateがシート上にない場合(例：1926-01-03)は、次の日付があるまで繰り返す
        # current_date += relativedelta(days=1)

    current_price = sheet[get_index(sheet, current_date)][1]
    withdraw_asset = current_asset * withdraw_rate
    current_years = 0

    asset_min = current_asset
    asset_max = 0

    datasets_years = []
    datasets_assets = []
    datasets_years.append(current_years)
    datasets_assets.append(current_asset)

    while current_date < startdate + relativedelta(years=withdraw_years):

        last_date = current_date
        last_price = current_price

        current_years += 1
        current_date = current_date + relativedelta(years=1)

        while get_index(sheet, current_date) < 0:
            # current_dateがシート上にない場合(例：1926-01-03)は、前の数値がある日付まで繰り返す
            current_date -= relativedelta(days=1)

        current_price = sheet[get_index(sheet, current_date)][1]
        growth_rate = (current_price - last_price) / last_price  # 資産増加率=(今年の価格-前年の価格)÷前年の価格

        current_asset = int((current_asset * (1 + growth_rate) - withdraw_asset) * (1 - inflation_rate))
        # print("{}年後({})の資産額は、{}円。リターンは、{:.1%}".format(current_years, current_date.strftime("%Y/%m/%d"), cnum.jp(int(current_asset)), growth_rate), file=codecs.open(asset_logfile, "a", "utf-8"))
        datasets_years.append(current_years)
        datasets_assets.append(current_asset)

        if current_asset < 0:
            return int(current_asset), int(asset_max), 0, current_years, datasets_years, datasets_assets

        if asset_max < current_asset:
            asset_max = current_asset
        if asset_min > current_asset:
            asset_min = current_asset
    return int(current_asset), int(asset_max), int(asset_min), current_years, datasets_years, datasets_assets


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


def simulate_once_a_year_multi(sheet, startdate: datetime, enddate: datetime, withdraw_years, initial_assets,
                               withdraw_rate, inflation_rate, asset_log_dir):
    # initialize
    if not os.path.exists(asset_log_dir):
        os.makedirs(asset_log_dir)
    asset_logfile = asset_log_dir + "start_{}_withdraw_{}years_withdrawrate_{:.1f}percent.txt".format(
        startdate.strftime("%Y%m%d"), withdraw_years, withdraw_rate * 100)

    if (os.path.isfile(asset_logfile)):
        os.remove(asset_logfile)

    current_date = startdate

    simulated_count = 0
    success_count = 0
    failure_count = 0
    assets = []  # 何年から始めて資産がどのくらい残ったか
    assets_log = []  # 試行毎の資産経過
    asset_maxs = []  # 施行毎に記録した資産最大値（途中経過含む）
    asset_mins = []

    asset_best_startdate = datetime.datetime(1000, 1, 1)  # 最後の資産が残った額が最大値に達した時の運用開始日
    asset_worst_startdate = datetime.datetime(1000, 1, 1)
    asset_max_final = 0
    asset_min_final = math.pow(initial_asset, 2)
    # end initialization

    while canbe_simulated(sheet, current_date, withdraw_years) and (current_date < enddate):
        simulated_count += 1
        print("case: {}, from:{}, initial asset: {}円, withdraw_rate: {:.1%}, {}".format(simulated_count,
                                                                                         current_date.strftime(
                                                                                             "%Y/%m/%d"),
                                                                                         cnum.jp(int(initial_asset)),
                                                                                         withdraw_rate,
                                                                                         datetime.datetime.fromtimestamp(
                                                                                             time.time()).strftime(
                                                                                             "%H:%M:%S")),
              file=codecs.open(asset_logfile, "a", "utf-8"))
        asset, asset_max, asset_min, end_year, years, assets_log = \
            simulate_once_a_year_single(sheet, current_date, withdraw_years, initial_assets, withdraw_rate,
                                        inflation_rate)
        # asset:最後に残った資産額, asset_max:運用期間に記録した最大資産, end_year：最後に終わった年数(成功したら30を返す、失敗の場合は30未満), years & assets:何年経過後の資産額
        if asset is not None:
            assets.append([current_date, withdraw_rate, withdraw_years, asset])
            if asset <= 0:
                print("Failed", file=codecs.open(asset_logfile, "a", "utf-8"))
                if asset_min is not None:
                    asset_min_final = 0
                asset_worst_startdate = current_date
                failure_count += 1
            else:
                success_count += 1
                print("Succeeded! assets: {}円 ({}年後の資産は{:.1f}倍になりました)".format(cnum.jp(int(asset)), withdraw_years,
                                                                                    asset / initial_assets),
                      file=codecs.open(asset_logfile, "a", "utf-8"))
            if asset_max_final < asset:
                asset_max_final = asset
                asset_best_startdate = current_date
            if asset_min_final > asset:
                asset_min_final = asset
                asset_worst_startdate = current_date
        else:
            print("No price in this day.", file=codecs.open(asset_logfile, "a", "utf-8"))
            simulated_count -= 1
        if asset_max is not None:
            asset_maxs.append(asset_max)
        if asset_min is not None:
            asset_mins.append(asset_min)
        current_date += relativedelta(days=1)
    return simulated_count, success_count, failure_count, assets, asset_maxs, asset_mins, asset_max_final, asset_best_startdate, asset_min_final, asset_worst_startdate


def generate_simulation_datasets(sheet_tuple, startdate: datetime, enddate: datetime, withdraw_years, initial_asset,
                                 inflation_rate, dump_dir, out_dir, asset_log_dir):
    if not os.path.exists(dump_dir):
        os.makedirs(dump_dir)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    if not os.path.exists(asset_log_dir):
        os.makedirs(asset_log_dir)

    # load from saved files
    loaded_dic = load_dump(dump_dir, "withdraw_rates", "success_rates", "assets_list",
                           "assets_min_list", "assets_max_list",
                           "assets_avg_list", "assets_med_list", "asset_min_final_list", "asset_max_final_list",
                           "asset_best_startdate_list",
                           "asset_worst_startdate_list"
                           )
    withdraw_rates = loaded_dic["withdraw_rates"]
    success_rates = loaded_dic["success_rates"]
    assets_list = loaded_dic["assets_list"]
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
            iterate_start = int((withdraw_rates[-1] + 0.005) * 1000)

        for i in tqdm.tqdm(range(iterate_start, 65, 5)):
            feature = executor.submit(simulate_once_a_year_multi, SPXL_tuple, startdate, enddate, withdraw_years,
                                      initial_asset, i / 1000, inflation_rate, asset_log_dir)
            simulated_count, success_count, failure_count, assets, asset_maxs, asset_mins, asset_max_final, asset_best_startdate, asset_min_final, asset_worst_startdate = \
                feature.result()
            withdraw_rates.append(i / 1000)
            success_rates.append(success_count / simulated_count)
            assets_list.append(assets)

            # assets: [startdate, withdraw_rate, asset]
            asset_list = []
            for i in assets:
                asset_list.append(i[2])

            assets_avg_list.append(int(sum(asset_list) / len(asset_list)))
            assets_min_list.append(min(asset_list))
            assets_max_list.append(max(asset_list))
            assets_med_list.append(statistics.median(asset_list))
            asset_max_final_list.append(asset_max_final)
            asset_best_startdate_list.append(asset_best_startdate)
            asset_min_final_list.append(asset_min_final)
            asset_worst_startdate_list.append(asset_worst_startdate)

            save_to_dump(dump_dir, withdraw_rates=withdraw_rates, success_rates=success_rates, assets_list=assets_list,
                         assets_avg_list=assets_avg_list, assets_min_list=assets_min_list,
                         assets_max_list=assets_max_list,
                         assets_med_list=assets_med_list, asset_max_final_list=asset_max_final_list,
                         asset_best_startdate_list=asset_best_startdate_list,
                         asset_min_final_list=asset_min_final_list,
                         asset_worst_startdate_list=asset_worst_startdate_list)

    # ファイルへの出力
    save_results_to_txt(out_dir, withdraw_rates=withdraw_rates, success_rates=success_rates, assets_list=assets_list,
                        assets_avg_list=assets_avg_list, assets_min_list=assets_min_list,
                        assets_max_list=assets_max_list,
                        assets_med_list=assets_med_list, asset_max_final_list=asset_max_final_list,
                        asset_best_startdate_list=asset_best_startdate_list,
                        asset_min_final_list=asset_min_final_list,
                        asset_worst_startdate_list=asset_worst_startdate_list)

    return withdraw_rates, success_rates, assets_avg_list, assets_list, assets_min_list, assets_max_list


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


if __name__ == '__main__':
    starttime = time.time()
    print("start: {}".format(datetime.datetime.fromtimestamp(starttime).strftime("%H:%M:%S")))

    SPXL_tuple = readCSV(SPXL_Sheets)
    # SPXL_tuple[i][0]: i番目の日付, SPXL_tuple[i][1]：i番目のSPXL値
    SPX_tuple = readCSV(SPX_Sheets)
    SSO_tuple = readCSV(SSO_Sheets)

    # asset,asset_max,asset_min, end_year, years, assets = simulate_once_a_year_single(SPXL_tuple, datetime.datetime(1920, 1, 3), 10, 60000000, 0.04)
    startdate = SPXL_tuple[0][0]
    enddate = SPXL_tuple[-1][0]
    '''
        dateについて：
        基本：datetime.datetime(yyyy, mm, dd)
        SPXL_tuple[0][0]：CSVファイルの一番最初の日付
        SPXL_tuple[-1][0]：CSVファイルの一番最後の日付
        date + relativedelta(years=n)：dateから数えてn年後
    '''

    # SPXL Simulation
    for years in tqdm.tqdm(range(30, 70, 10)):
        generate_simulation_datasets(SPXL_tuple, startdate, enddate, years, 10000000, 0,
                                     "FIRE_Simulation\\single_asset\\SPXL100_{}years_inflation_2percent_dump\\".format(
                                         years),
                                     "FIRE_Simulation\\single_asset\\SPXL100_{}years_inflation_2percent_output\\".format(
                                         years),
                                     asset_log_dir + "SPXL100_{}years_inflation_2percent_log\\".format(years)
                                     )
    # データシートtuple, 開始日、終了日、運用年数、初期資産、インフレ率、dump格納先、output格納先、asset log格納先

    '''
    # test
    withdraw_rates_SPXL100_2years, success_rates_SPXL100_2years, assets_avg_list_SPXL100_2years, assets_list_SPXL100_2years, assets_min_list_SPXL100_2years, assets_max_list_SPXL100_2years = \
        generate_simulation_datasets(SPXL_tuple, startdate, startdate + relativedelta(years=2), 2, 10000000, 0.02,
                                     "SPXL100_{}years_inflation_2percent_dump\\".format(2),
                                     "SPXL100_{}years_inflation_2percent_output\\".format(2),
                                     asset_log_dir + "SPXL100_{}years_inflation_2percent_log\\".format(2)
                                     )
    # データシートtuple, 開始日、終了日、運用年数、初期資産、インフレ率、dump格納先、output格納先、asset log格納先
    '''

    # SPX Simulation
    for years in tqdm.tqdm(range(30, 70, 10)):
        generate_simulation_datasets(SPX_tuple, startdate, enddate, years, 10000000, 0.02,
                                     "FIRE_Simulation\\single_asset\\SPX100_{}years_inflation_2percent_dump\\".format(
                                         years),
                                     "FIRE_Simulation\\single_asset\\SPX100_{}years_inflation_2percent_output\\".format(
                                         years),
                                     asset_log_dir + "SPX100_{}years_inflation_2percent_log\\".format(years)
                                     )
    # SSO Simulation
    for years in tqdm.tqdm(range(30, 70, 10)):
        generate_simulation_datasets(SSO_tuple, startdate, enddate, years, 10000000, 0,
                                     "FIRE_Simulation\\single_asset\\SSO100_{}years_inflation_2percent_dump\\".format(
                                         years),
                                     "FIRE_Simulation\\single_asset\\SSO100_{}years_inflation_2percent_output\\".format(
                                         years),
                                     asset_log_dir + "SSO100_{}years_inflation_2percent_log\\".format(years)
                                     )

    print("end: {}".format(datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")))

    time1 = time.time()
    print("経過秒数：{}".format(int(time1 - starttime)))
