import datetime
import time

import click

from zhdate import ZhDate as lunar_date


def get_week_day(date):
    week_day_dict = {
        0: '星期一',
        1: '星期二',
        2: '星期三',
        3: '星期四',
        4: '星期五',
        5: '星期六',
        6: '星期天',
    }
    day = date.weekday()
    return week_day_dict[day]

def time_parse(today):
    distance_big_year = (lunar_date(today.year, 1, 1).to_datetime().date() - today).days
    distance_big_year = distance_big_year if distance_big_year > 0 else (
            lunar_date(today.year + 1, 1, 1).to_datetime().date() - today).days

    distance_5_5 = (lunar_date(today.year, 5, 5).to_datetime().date() - today).days
    distance_5_5 = distance_5_5 if distance_5_5 > 0 else (
            lunar_date(today.year + 1, 5, 5).to_datetime().date() - today).days

    distance_8_15 = (lunar_date(today.year, 8, 15).to_datetime().date() - today).days
    distance_8_15 = distance_8_15 if distance_8_15 > 0 else (
            lunar_date(today.year + 1, 8, 15).to_datetime().date() - today).days

    distance_year = (datetime.datetime.strptime(f"{today.year}-01-01", "%Y-%m-%d").date() - today).days
    distance_year = distance_year if distance_year > 0 else (
            datetime.datetime.strptime(f"{today.year + 1}-01-01", "%Y-%m-%d").date() - today).days

    distance_4_5 = (datetime.datetime.strptime(f"{today.year}-04-05", "%Y-%m-%d").date() - today).days
    distance_4_5 = distance_4_5 if distance_4_5 > 0 else (
            datetime.datetime.strptime(f"{today.year + 1}-04-05", "%Y-%m-%d").date() - today).days

    distance_5_1 = (datetime.datetime.strptime(f"{today.year}-05-01", "%Y-%m-%d").date() - today).days
    distance_5_1 = distance_5_1 if distance_5_1 > 0 else (
            datetime.datetime.strptime(f"{today.year + 1}-05-01", "%Y-%m-%d").date() - today).days

    distance_10_1 = (datetime.datetime.strptime(f"{today.year}-10-01", "%Y-%m-%d").date() - today).days
    distance_10_1 = distance_10_1 if distance_10_1 > 0 else (
            datetime.datetime.strptime(f"{today.year + 1}-10-01", "%Y-%m-%d").date() - today).days

    distance_7_21 = (datetime.datetime.strptime(f"{today.year}-07-21", "%Y-%m-%d").date() - today).days
    distance_7_21 = distance_7_21 if distance_7_21 > 0 else (
            datetime.datetime.strptime(f"{today.year + 1}-07-21", "%Y-%m-%d").date() - today).days

    distance_11_26 = (datetime.datetime.strptime(f"{today.year}-11-26", "%Y-%m-%d").date() - today).days
    distance_11_26 = distance_11_26 if distance_11_26 > 0 else (
            datetime.datetime.strptime(f"{today.year + 1}-11-26", "%Y-%m-%d").date() - today).days

    distance_12_15 = (datetime.datetime.strptime(f"{today.year}-12-15", "%Y-%m-%d").date() - today).days
    distance_12_15 = distance_12_15 if distance_12_15 > 0 else (
            datetime.datetime.strptime(f"{today.year + 1}-12-15", "%Y-%m-%d").date() - today).days

    #计算下在一起多久了
    love_now = datetime.datetime.today()
  #  print(love_now)
    love_one_day = datetime.datetime(2021,12,15,0,00,0)
    love_time = (love_now - love_one_day).days


 #   print(f"最后时间为{love_time}")




    time_ = [
        {"v_": 5 - 1 - today.weekday(), "title": "周末"},  # 距离周末
        #{"v_": distance_year, "title": "元旦"},  # 距离元旦
        #{"v_": distance_big_year, "title": "过年"},  # 距离过年
        #{"v_": distance_4_5, "title": "清明节"},  # 距离清明
        #{"v_": distance_5_1, "title": "劳动节"},  # 距离劳动
        #{"v_": distance_5_5, "title": "端午节"},  # 距离端午
        #{"v_": distance_8_15, "title": "中秋节"},  # 距离中秋
        #{"v_": distance_10_1, "title": "国庆节"},  # 距离国庆
        {"v_": distance_7_21,"title":"宝宝生日"}, #距离宝宝生日
        {"v_": distance_11_26, "title": "认识一周年"},
        {"v_": distance_12_15, "title": "一周年纪念日"},
        {"v_": love_time,"title":"在一起"}
    ]

    time_ = sorted(time_, key=lambda x: x['v_'], reverse=False)
    return time_


@click.command()
def cli():
    """你好，摸鱼人，工作再累，一定不要忘记摸鱼哦 !"""
    from colorama import init, Fore
    init(autoreset=True)  # 初始化，并且设置颜色设置自动恢复
    print()
    today = datetime.date.today()
    now_ = f"{today.year}年{today.month}月{today.day}日"
    week_day_ = get_week_day(today)
    print(f'\t\t {Fore.GREEN}{now_} {week_day_}')
    str_ = '''
    \t\t😘 ❤ 
    '''
    print(f'{Fore.RED}{str_}')

    time_ = time_parse(today)
    for t_ in time_:
        if t_.get("title")=="在一起":
            print(f'\t\t {Fore.RED}已经{t_.get("title")} {t_.get("v_")}天啦，😘')
        else:
            print(f'\t\t {Fore.GREEN}距离{t_.get("title")}还有: {t_.get("v_")}天')
    tips_ = '''
    [友情提示] 大哥说的永远都是对的，跟着大华走吃香的喝辣的！！！！！！！！！！\n
    '''
    print(f'{Fore.RED}{tips_}')
    print(f'\t\t\t\t\t\t\t{Fore.YELLOW} 大华')


if __name__ == '__main__':
    cli()