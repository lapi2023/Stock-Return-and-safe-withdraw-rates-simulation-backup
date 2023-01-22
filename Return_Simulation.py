import codecs
import csv
import datetime
import math
import os
import statistics
import time
import cnum
import joblib
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import tqdm as tqdm
from dateutil.relativedelta import relativedelta


SPXL_Sheets = r"Price Sheet\simulated_SPXL_1886-2023.csv"
SPX_Sheets = r"Price Sheet\simulated_SPX_funds_1886-2023_daily.csv"
SSO_Sheets = r"Price Sheet\simulated_SSO_1886-2023.csv"
initial_asset = 10000
asset_log_dir = "Return_Simulation\\asset_log\\"

def readCSV(path):
    list = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            # print([datetime.datetime.strptime(row['date'], "%Y/%m/%d"), float(row['SPXL'])])
            list.append(tuple([datetime.datetime.strptime(row['date'], "%Y/%m/%d"), float(row['price'])]))
    return tuple(list)
def calculate_return_lump_sum_investment_single_year(sheet_tuple, startdate: datetime, invest_years, initial_asset, inflation_rate=0.02):
    # 条件：最初の一カ月経過時点で初めてwithdraw_rateで資産を取り出す(最初の取り出しは行わない）
    enddate = startdate + relativedelta(years=invest_years)
    if get_index(sheet_tuple, startdate) < 0:
        return None, None
    while get_index(sheet_tuple, enddate) < 0:
        enddate -= relativedelta(days=1)


    start_price = sheet_tuple[get_index(sheet_tuple, startdate)][1]
    end_price = sheet_tuple[get_index(sheet_tuple, enddate)][1]
    growth_rate = (end_price - start_price) / start_price  # リターン=(今年の価格-前年の価格)÷前年の価格

    end_asset = int(initial_asset * (1 + growth_rate) * (1 - inflation_rate))
    return int(end_asset), growth_rate
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
def canbe_simulated(sheet, startdate: datetime, invest_years):
    if startdate + relativedelta(years=invest_years) > sheet[-1][0]:
        return False  # 開始日付+継続年数(invest_years)のレコードがシートにないため-1を返して終了
    else:
        return True
def calculate_return_lump_sum_investment_multi_years(sheet_tuple, startdate: datetime, invest_years, initial_asset, inflation_rate=0.02, asset_log_dir =""):
    # initialize
    if asset_log_dir != "":
        if not os.path.exists(asset_log_dir):
            os.makedirs(asset_log_dir)
        asset_logfile = asset_log_dir + "start_{}_invest_{}years_inflation_{:.1f}percent.txt".format(
            startdate.strftime("%Y%m%d"), invest_years, inflation_rate * 100)
        if (os.path.isfile(asset_logfile)):
            os.remove(asset_logfile)

    current_date = startdate
    day_count = 0
    asset_result_list = [] #何年から始めて資産がどのくらい残ったか
    asset_list = []
    price_growth_rate_list = []
    # end initialization

    while canbe_simulated(sheet_tuple, current_date, invest_years) and (current_date < enddate):
        day_count += 1
        print("case: {}, from:{}, initial asset: {}円, {}".format(day_count, current_date.strftime("%Y/%m/%d"), cnum.jp(int(initial_asset)),
                                                                    datetime.datetime.fromtimestamp(
                time.time()).strftime("%H:%M:%S")), file=codecs.open(asset_logfile, "a", "utf-8"))
        asset, growth_rate = calculate_return_lump_sum_investment_single_year(sheet_tuple, current_date, invest_years, initial_asset, inflation_rate)
        if asset is not None:
            asset_result_list.append([current_date, invest_years, asset])
            asset_list.append(asset)
            price_growth_rate_list.append(growth_rate)
            print("{}年後の資産は{}円({:.1f}倍)になりました)".format(invest_years, cnum.jp(int(asset)), asset / initial_asset),
                  file=codecs.open(asset_logfile, "a", "utf-8"))
        else:
            print("No price data in this day.", file=codecs.open(asset_logfile, "a", "utf-8"))

        current_date += relativedelta(days=1)

    return asset_result_list, asset_list, price_growth_rate_list
def generate_simulation_datasets_lump_sum_investment(sheet_tuple, startdate: datetime, enddate: datetime, invest_years, initial_asset,
                                                     inflation_rate = 0.02, dump_dir = "", out_dir = "", asset_log_dir = ""):

    if dump_dir != "":
        if not os.path.exists(dump_dir):
            os.makedirs(dump_dir)
    if out_dir != "":
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
    if asset_log_dir != "":
        if not os.path.exists(asset_log_dir):
            os.makedirs(asset_log_dir)

    asset_result_list, asset_list, price_growth_rate_list =\
        calculate_return_lump_sum_investment_multi_years(sheet_tuple, startdate, invest_years, initial_asset, 0.02, asset_log_dir)

    if dump_dir != "":
        save_to_dump(dump_dir, asset_result_list=asset_result_list,
                     asset_list=asset_list,
                     price_growth_rate_list=price_growth_rate_list
                     )
    if out_dir != "":
        save_results_to_txt(out_dir, asset_result_list=asset_result_list,
                     asset_list=asset_list,
                     price_growth_rate_list=price_growth_rate_list
                            )
    return asset_result_list, asset_list, price_growth_rate_list
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


    # SPX Simulation
    for years in tqdm.tqdm([1, 5, 10, 20, 30, 40, 50]):
        generate_simulation_datasets_lump_sum_investment(SPX_tuple, startdate, enddate, years, 10000000, 0.02,
                                     "Return_Simulation\\dump\\SPX100_{}years_inflation_2percent_dump\\".format(years),
                                     "Return_Simulation\\output\\SPX100_{}years_inflation_2percent_output\\".format(years),
                                                         asset_log_dir
                                                         )

    # SSO Simulation
    for years in tqdm.tqdm([1, 5, 10, 20, 30, 40, 50]):
        generate_simulation_datasets_lump_sum_investment(SSO_tuple, startdate, enddate, years, 10000000, 0.02,
                                     "Return_Simulation\\dump\\SSO100_{}years_inflation_2percent_dump\\".format(years),
                                     "Return_Simulation\\output\\SSO100_{}years_inflation_2percent_output\\".format(years),
                                                         asset_log_dir
                                                         )

    # SPXL Simulation
    for years in tqdm.tqdm([1, 5, 10, 20, 30, 40, 50]):
        generate_simulation_datasets_lump_sum_investment(SPXL_tuple, startdate, enddate, years, 10000000, 0.02,
                                     "Return_Simulation\\dump\\SPXL100_{}years_inflation_2percent_dump\\".format(years),
                                     "Return_Simulation\\output\\SPXL100_{}years_inflation_2percent_output\\".format(years),
                                                         asset_log_dir
                                                         )
    # データシートtuple, 開始日、終了日、投資年数、初期資産、インフレ率、dump格納先、output格納先、asset log格納先

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



    print("end: {}".format(datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")))

    time1 = time.time()
    print("経過秒数：{}".format(int(time1 - starttime)))
