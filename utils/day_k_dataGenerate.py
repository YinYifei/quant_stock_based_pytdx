import os
from datetime import datetime, timedelta



class Get_bar_price():
    def __init__(self, stock_code, files_path):
        self.stock_code = stock_code
        self.files_path = files_path

        self.all_open_price = {}
        self.all_close_price = {}
        self.all_high_price = {}
        self.all_low_price = {}
        self.all_vol = {}
        self.all_amount = {}
        self.all_date = []
        self.deal_cur_k(stock_code, files_path)

    def deal_cur_k(self, stock_code, dir_path):
        file_path = dir_path + "\\" + stock_code
        ff = open(file_path, "r")
        data = ff.read().strip().split("\n")
        ff.close()
        for da in data[1:]:
            temp_da = da.strip().split(" ")
            if type(temp_da[0]) == datetime:
                cur_date = temp_da[0]
            else:
                if "-" in temp_da[0]:
                    cur_date = datetime.strptime(temp_da[0], "%Y-%m-%d")
                else:
                    cur_date = datetime.strptime(temp_da[0], "%Y%m%d")

            self.all_open_price[cur_date] = float(temp_da[2])
            self.all_close_price[cur_date] = float(temp_da[3])
            self.all_high_price[cur_date] = float(temp_da[4])
            self.all_low_price[cur_date] = float(temp_da[5])
            self.all_vol[cur_date] = float(temp_da[6])
            self.all_amount[cur_date] = float(temp_da[7])
            self.all_date.append(cur_date)

    def get_cur_price(self, date, type_=None):
        if type(date) == datetime:
            cur_date = date
        else:
            if "-" in date:
                cur_date = datetime.strptime(date, "%Y-%m-%d")
            else:
                cur_date = datetime.strptime(date, "%Y%m%d")
        if type_ == None or type_ == "close":
            return self.all_close_price[cur_date]
        elif type_ == "open":
            return self.all_open_price[cur_date]
        elif type_ == "high":
            return self.all_high_price[cur_date]
        elif type_ == "low":
            return self.all_low_price[cur_date]
        elif type_ == "vol":
            return self.all_vol[cur_date]
        elif type_ == "amount":
            return self.all_amount[cur_date]
        else:
            return None

    def get_cur_price_ref(self, date, type_=None, days=0):
        # date  均线日期
        # type_ "open" "close" "high" "low"
        # days 向前多少天

        if type(date) == datetime:
            cur_date = date
        else:
            if "-" in date:
                cur_date = datetime.strptime(date, "%Y-%m-%d")
            else:
                cur_date = datetime.strptime(date, "%Y%m%d")

        cur_index = self.all_date.index(cur_date)
        before_date = self.all_date[int(cur_index) - int(days)]

        return self.get_cur_price(before_date, type_)