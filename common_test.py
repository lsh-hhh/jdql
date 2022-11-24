import datetime
import calendar
import random
import time


def date_test():
    # current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    current_date = datetime.datetime.now()
    print(current_date)

    week_day, month_count_day = calendar.monthrange(current_date.year, current_date.month)
    print(week_day)
    print(month_count_day)
    last_day = datetime.date(current_date.year, current_date.month, day=month_count_day)
    print(last_day)
    print(month_count_day)

    print(current_date.date() == last_day)


def random_test():
    int_arr = [1, 2, 3, 4, 5]
    random_res = random.randint(0, len(int_arr) - 1)
    print(int_arr[random_res])


def time_test():
    print(datetime.datetime.now())
    print(int(time.time() * 1000))


def main():
    # date_test()
    # for i in range(0, 100):
    #     random_test()
    time_test()


if __name__ == "__main__":
    main()
