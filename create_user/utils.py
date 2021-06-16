import datetime
import time


def getDate(day_increment=0):
    per_day_time_microseconds = 24 * 60 * 60 * 1000 * 1000
    now_time = time.time() * 1000 * 1000
    target_time = now_time + (per_day_time_microseconds * day_increment)
    final_date = datetime.date.fromtimestamp(target_time/1000000)
    return final_date.strftime("%Y-%m-%d")


# #def getDate(day_increment=0,month_increment=0,year_increment=0):
# #    today_date = datetime.datetime.now()
#     day = today_date.day + day_increment
#     day = 1 if day > 30 else day
#     month = today_date.month + month_increment
#     month = 1 if month > 12 else month
#     year = today_date.year + year_increment
#     return f"{year}-{month if month>9 else f'0{month}'}-{day if day>9 else f'0{day}'}"
