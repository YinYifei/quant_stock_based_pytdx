from pytdx.exhq import *
from pytdx.hq import *
from datetime import datetime, timedelta, date
# from utils.utils_function import stastic_zt_count
from utils.day_k_dataGenerate import *

import os

api_hq = TdxHq_API()
api_hq = api_hq.connect('119.147.212.81', 7709)

def minite_for(start_time, end_time):
  

    start_time = datetime.strptime(start_time, "%H:%M")
    end_time = datetime.strptime(end_time, "%H:%M")

    # 定义时间增量为1分钟
    delta = timedelta(minutes=1)
    res = []
    # 循环遍历时间范围
    current_time = start_time
    while current_time <= end_time:
        # 打印当前时间
        res.append(current_time.strftime("%H:%M"))
        # 增加时间
        current_time += delta

    return res

def get_minte_data(start_date, end_date, stock_code, output_path):
    output_path=out_dir + "\\" + stock_code
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    start_date = datetime.strptime(start_date, "%Y%m%d")
    end_date = datetime.strptime(end_date, "%Y%m%d")

    # 定义日期增量为1天
    delta = timedelta(days=1)
    all = []
    # 循环遍历日期范围
    current_date = start_date
 
    while current_date <= end_date:
        
        temp = []
        cur_date = current_date.strftime("%Y%m%d")
        print(cur_date)
        cur_stock_data = api_hq.get_history_minute_time_data(TDXParams.MARKET_SZ, stock_code, cur_date)
        if len(cur_stock_data) != 0:
            outfile = open(output_path+ "\\" +str(current_date.strftime("%Y%m%d")), "a")
            for i, da in enumerate(cur_stock_data):
                # temp.append(cur_date + " " + str(da["price"]))
                outfile.write(cur_date + " " + all_time_for[i] + " " + str(da["price"]) + "\n")
            outfile.close()
        current_date += delta

def get_day_kLine(start_date, end_date, stock_code, out_dir):
    print("获取k线", start_date, end_date, stock_code, out_dir)
    output_path = out_dir + "\\day_k"
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    data = api_hq.get_k_data(stock_code, start_date, end_date)
    save = []
    save.append("date code open close high low vol amount")
    for da in data.values.tolist():
        save.append(" ".join(list(map(str, da[-2:] + da[:-2]))))

    ff = open(output_path + "\\" + stock_code, "w")
    ff.write("\n".join(save) + "\n")
    ff.close()


def get_history_data(stock_code, out_dir = r"D:\tdx_data\all_stock_code/one_day_k", start_date="20000101", end_date=""):
    today = date.today()
    formatted_date = today.strftime("%Y%m%d")

    if len(end_date) == 0:
        end_date=formatted_date

    all_time_for = []
    time_for_am = minite_for("09:31", "11:30")
    time_for_pa = minite_for("13:01", "15:00")
    all_time_for.extend(time_for_am)
    all_time_for.extend(time_for_pa)
    # get_minte_data(start_date, end_date,stock_code, out_dir)
    get_day_kLine(start_date, end_date, stock_code, out_dir)

def batch_get_stock_data():
    ff = open(r"./all_stock_code/a_stock", "r")
    stock_codes = ff.read().strip().split("\n")
    ff.close()

    for stock_code in stock_codes:
        get_history_data(stock_code, r"./all_stock_code/one_day_k")

def get_all_stock_code():
    all_stocks = []
    # all_stocks = api_hq.get_security_list(1, 100) # 0, 1, 2;
    # 这个api暂时有点问题；因此暂时不通过这种方式获取股票列表；
    # print(len(all_stocks))

    day_K_dir = r"D:\tdx_data\hand_import_dayK"
    day_K_list = os.listdir(day_K_dir)
    all_code = []
    bz = []
    a_stock = []
    kechuang = []
    chuangye = []
    for da in day_K_list:
        all_code.append(da[3:9])
        if "BJ" in da:
            bz.append(da[3:9])
        elif da[3:6] == "688":
            kechuang.append(da[3:9])
        elif da[3:6] == "300" or da[3:6] == "301":
            chuangye.append(da[3:9])
        else:
            a_stock.append(da[3:9])

    return all_code, bz, a_stock, kechuang, chuangye
    

def stastic_zt_stock(start_date="20230101", end_date="20231201", stock_data_save_path=r"D:\tdx_data\one_day_k", type = "a_stock"):
    all_code, bz, a_stock, kechuang, chuangye = get_all_stock_code()

    if type == "all_code":
        all_stock_code = all_code
    elif type == "bz":
        all_stock_code = bz
    elif type == "a_stock":
        all_stock_code = a_stock
    elif type == "kechuang":
        all_stock_code = kechuang
    elif type == "chuangye":
        all_stock_code = chuangye
    else:
        print("not this type")

    start_date = datetime.strptime(start_date, "%Y%m%d")
    end_date = datetime.strptime(end_date, "%Y%m%d")
    zt_count = {}

    # 这里只是统计涨停，因此不写太复杂；
    for cur_stock_code in all_stock_code:
        print(cur_stock_code)

        ff = open(os.path.join(stock_data_save_path, cur_stock_code), "r")
        days_data = ff.read().strip().split("\n")
        ff.close()

        for i, day_data in enumerate(days_data[:]):
            da = day_data.strip().split(" ")
            if i == 0 :
                continue
            elif  i == 1:
                zt_count.setdefault(da[0].replace("-", ""), 0)
                continue
            open_price = float(da[2])
            close_price = float(da[3])
            high_price = float(da[4])
            low_price = float(da[5])
            cur_day = datetime.strptime(da[0], "%Y-%m-%d")

            ref_1_close_price = float(days_data[i - 1].strip().split(" ")[3])
            if (close_price >= ref_1_close_price* 1.09 and close_price <= ref_1_close_price* 1.11 and high_price == close_price) \
                or (close_price >= ref_1_close_price* 1.19 and high_price == close_price):
                zt_count.setdefault(da[0].replace("-", ""), 0)
                zt_count[da[0].replace("-", "")] += 1
            if da[0].replace("-", "") == "20170525":
                print(close_price, ref_1_close_price)
        # get_bar_price = Get_bar_price(cur_stock_code, stock_data_save_path)
        # ref_day_1_close_price = get_bar_price.get_cur_price_ref(cur_day, "close", 1)

        break
    print(zt_count)

if __name__ == "__main__":
    # all_code, bz, a_stock, kechuang, chuangye = get_all_stock_code()
    stastic_zt_stock()