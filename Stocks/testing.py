#!/usr/bin/python3.9
from yahoo_fin import options

i = 0
while i < 100:
    closing_dates = options.get_expiration_dates("MOS")
    print(closing_dates)
    i += 1



# markdict = {"Tom":67, "Tina": 54, "Akbar": 87, "Kane": 43, "Divya":73}
# marklist = sorted(markdict.items(), key=lambda x:x[1], reverse=True)
# sortdict = dict(marklist)
# print(sortdict)

# markdict = {key:val for key, val in markdict.items() if val != 67}
# print(markdict)



# months = 12
# percent = 1.04
# current_portfolio = 23000
# years = 10

# i = 0
# while i < years:
#     j = 0
#     year_starting = current_portfolio
#     while j < months:
#         current_portfolio = percent * current_portfolio
#         j += 1
#     print((current_portfolio - year_starting)/year_starting)
#     i += 1
# print(current_portfolio)