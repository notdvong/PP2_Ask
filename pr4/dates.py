import datetime

x = datetime.datetime.now() #displays the current time
print(x)
#In order to use date we have to import it

print(x.year)
print(x.strftime("%A"))
#Return the year and name of weekday


y = datetime.datetime(2020, 5, 17)

print(y)
#The datetime() class also takes parameters for time and timezone (hour, minute, second, microsecond, tzone), but they are optional, and has a default value of 0, (None for timezone)


#The method is called strftime(), and takes one parameter, format, to specify the format of the returned string
x = datetime.datetime(2018, 6, 1)

print(x.strftime("%B")) #%B gets us the month name full version

#1:
from datetime import date, timedelta

result = date.today() - timedelta(5)
print(result)

#2:
today = date.today()
yesterday = today - timedelta(1)
tomorrow = today + timedelta(1)

print(yesterday, today, tomorrow)

#3:
now = datetime.now().replace(microsecond=0)
print(now)

#4:
# Example dates (Year, Month, Day, Hour, Minute)
date1 = datetime(2026, 2, 11, 10, 0, 0)
date2 = datetime(2026, 2, 11, 11, 30, 0)
difference = date2 - date1
seconds = difference.total_seconds()

print(f"The difference is {seconds} seconds.")
