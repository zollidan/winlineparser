from meinsrc.config import change_date

class_date = "29 мар 11:00"

day = change_date(class_date)[0]
month = change_date(class_date)[1]
year = change_date(class_date)[2]
time = change_date(class_date)[3]

print(day, month, year, time)
