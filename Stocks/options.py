#!/usr/bin/python3.9
from yahoo_fin import options
from yahoo_fin import stock_info

# pip install yahoo_fin
# pip install html5lib
# pip install requests-html

class BestOptions:
    # Protected
    _PATH = "C:\\Users\\Zach\\Documents\\My Programs\\Stocks\\Tickers\\"
    _SPATH = "C:\\Users\\Zach\\Documents\\My Programs\\Stocks\\sectors.txt"
    # Public
    sectors_txt = []
    basic_materials = []
    comm_services = []
    con_cyclical = []
    con_defensive = []
    energy = []
    fin_services = []
    healthcare = []
    industrials = []
    real_estate = []
    technology = []
    utilities = []
    zmisc = []

    def getTickerList(self): # Gets a list of all the txt file sectors
        with open(self._SPATH, "r") as StockTickers:
            self.sectors_txt = [line.rstrip() for line in StockTickers]
        return
            
    def populateSectors(self): # Populates all tickers for each sector
        i = 0
        temp_list = []
        while i < len(self.sectors_txt):
            with open(self._PATH + self.sectors_txt[i], "r") as SectorTickers:
                temp_list = [line.rstrip() for line in SectorTickers]
            if i == 0:
                self.basic_materials = temp_list
            elif i == 1:
                self.comm_services = temp_list
            elif i == 2:
                self.con_cyclical = temp_list
            elif i == 3:
                self.con_defensive = temp_list
            elif i == 4:
                self.energy = temp_list
            elif i == 5:
                self.fin_services = temp_list
            elif i == 6:
                self.healthcare = temp_list
            elif i == 7:
                self.industrials = temp_list
            elif i == 8:
                self.real_estate = temp_list
            elif i == 9:
                self.technology = temp_list
            elif i == 10:
                self.utilities = temp_list
            else:
                self.zmisc = temp_list
            i += 1
            temp_list = []
        del temp_list
        return

    def closestCallStrike(self, ticker, cur_stock_price, closing_date): # Gets the option price of the closest strike price
        chain = options.get_options_chain(ticker, closing_date) # Gets all option information
        closest_call = min(range(len(chain["calls"]["Strike"])), key=lambda i: abs(chain["calls"]["Strike"][i]-cur_stock_price)) # Finds closest strike price index

        if chain["calls"]["Strike"][closest_call] < cur_stock_price: # If price is lower we need to raise it by one
            closest_call += 1
        
        # print("Closest strike is %f" % (cur_stock_price))
        # print(chain["calls"]["Strike"][closest_call])
        # print(chain["calls"]["Last Price"][closest_call])
        result = (float(chain["calls"]["Bid"][closest_call]) + float(chain["calls"]["Ask"][closest_call])) / 2.00
        # print("Result is:")
        # print(result)
        return result # Returns option price

    def closestPutStrike(self, ticker, cur_stock_price, closing_date): # Gets the option price of the closest strike price
        chain = options.get_options_chain(ticker, closing_date) # Gets all option information
        closest_put = min(range(len(chain["puts"]["Strike"])), key=lambda i: abs(chain["puts"]["Strike"][i]-cur_stock_price)) # Finds closest strike price index
        
        if chain["puts"]["Strike"][closest_put] > cur_stock_price: # If price is lower we need to raise it by one
            closest_put -= 1

        # print("Closest strike is %f" % (cur_stock_price))
        # print(chain["puts"]["Strike"][closest_put])
        # print(chain["puts"]["Last Price"][closest_put])
        result = (float(chain["puts"]["Bid"][closest_put]) + float(chain["puts"]["Ask"][closest_put])) / 2.00 # Returns option price
        # print("Result is:")
        # print(result)
        return result

    def topFive(self, sector):
        top_five_calls = {}
        top_five_puts = {}
        # max_call = 0
        # min_call = 10000
        # max_put = 0
        # min_put = 10000
        i = 0
        print("Sector len is:")
        print(len(sector))
        while i < len(sector):
            print(i)
            print(sector[i])
            closing_dates = options.get_expiration_dates(sector[i]) # Closing dates of the stock
            print(closing_dates)
            cur_stock_price = stock_info.get_live_price(sector[i]) # Get current ticker price
            # print("in while what is stock price %f" % (cur_stock_price))
            
            call = self.closestCallStrike(sector[i], cur_stock_price, closing_dates[0])
            # print(sector[i])
            # print(call)
            # if call > max_call: # Keeps track of the lowest and highest option prices
            #     max_call = call
            # if call < min_call:
            #     min_call = call
            
            put = self.closestPutStrike(sector[i], cur_stock_price, closing_dates[0])
            # print(sector[i])
            # print(put)
            # if put > max_put:
            #     max_put = put
            # if put < min_put:
            #     min_put = put
            
            # top_five_calls[sector[i]] = call
            # top_five_puts[sector[i]] = put
            top_five_calls[sector[i]] = [round(cur_stock_price, 2), closing_dates[0], round(call, 2)]
            top_five_puts[sector[i]] = [round(cur_stock_price, 2), closing_dates[0], round(put, 2)]
            
            print(top_five_calls)
            print(top_five_puts)
            # print("LEN OF CALLS")
            # print(len(top_five_calls))
            # print("LEN OF PUTS")
            # print(len(top_five_puts))
            if len(top_five_calls) > 5: # Populates call dict
                # Pop lowest
                print(top_five_calls)
                del top_five_calls[min(top_five_calls, key=top_five_calls.get)]
                print(top_five_calls)
                # min_call = min(top_five_calls.items())
                # min_call = int(min_call)
                # print("MINCALL %i" % (min_call))
                # print(top_five_calls)
                # top_five_calls = {key:val for key, val in top_five_calls.items() if val != min_call}
            # else:
            #     # if top_five_calls == 10: # Sorts the current dict
            #     #     top_five_calls = sorted(top_five_calls.items(), key=lambda x:x[1], reverse=True)

            #     if call > max_call:
            #         max_call = call
            #         # top_five_calls.insert(0, {sector[i] : call})
            #         top_five_calls[sector[i]] = call

            if len(top_five_puts) > 5: # Populates put dict
                # Pop lowest
                print(top_five_puts)
                del top_five_puts[min(top_five_puts, key=top_five_puts.get)]
                print(top_five_puts)
                # min_put = min(top_five_puts.items())
                # min_put = int(min_put)
                # print("MINPUT %i" % (min_put))
                # print(top_five_puts)
                # top_five_puts = {key:val for key, val in top_five_puts.items() if val != min_put}
            # else:
            #     # if top_five_puts == 10: # Sorts the current dict
            #     #     top_five_puts = sorted(top_five_puts.items(), key=lambda x:x[1], reverse=True)
            #     if put > max_put:
            #         max_put = put
            #         top_five_puts.insert(0, {sector[i] : put})
            i += 1
        
        self.printTopFive(top_five_calls, top_five_puts)
        return

    def allSectors(self):
        return (self.basic_materials + self.comm_services + self.con_cyclical + self.con_defensive + 
                self.energy + self.fin_services + self.healthcare + self.industrials +
                self.real_estate + self.technology + self.utilities + self.zmisc)

    def basicMaterials(self):
        return self.basic_materials
    
    def commServices(self):
        return self.comm_services
    
    def conCyclical(self):
        return self.con_cyclical

    def conDefensive(self):
        return self.con_defensive

    def energySector(self):
        return self.energy
    
    def finServices(self):
        return self.fin_services
    
    def healthcareSector(self):
        return self.healthcare

    def industSector(self):
        return self.industrials
    
    def realEstate(self):
        return self.real_estate
    
    def techSector(self):
        return self.technology

    def utilSector(self):
        return self.utilities
    
    def miscSector(self):
        return self.zmisc
    
    def getSector(self, choice):
        choice = int(choice)
        descision = ""
        if choice == 1:
            descision = self.allSectors()
        elif choice == 2:
            descision = self.basicMaterials()
        elif choice == 3:
            descision = self.commServices()
        elif choice == 4:
            descision = self.conCyclical()
        elif choice == 5:
            descision = self.conDefensive()
        elif choice == 6:
            descision = self.energySector()
        elif choice == 7:
            descision =self.finServices()
        elif choice == 8:
            descision = self.healthcareSector()
        elif choice == 9:
            descision = self.industSector()
        elif choice == 10:
            descision = self.realEstate()
        elif choice == 11:
            descision = self.techSector()
        elif choice == 12:
            descision = self.utilSector()
        else:
            descision = self.miscSector()
        return descision

    def printSectors(self):
        print(self.basic_materials)
        print(self.comm_services)
        print(self.con_cyclical)
        print(self.con_defensive)
        print(self.energy)
        print(self.fin_services)
        print(self.healthcare)
        print(self.industrials)
        print(self.real_estate)
        print(self.technology)
        print(self.utilities)
        print(self.zmisc)
        return

    def printTopFive(self, dict_calls, dict_puts):
        print("Calls")
        print(dict_calls)
        lcalls = sorted(dict_calls.items(), key=lambda x:x[1][2], reverse=True)
        sorted_dcalls = dict(lcalls)
        print(sorted_dcalls)
        print("Puts")
        print(dict_puts)
        lputs = sorted(dict_puts.items(), key=lambda x:x[1][2], reverse=True)
        sorted_dputs = dict(lputs)
        print(sorted_dputs)
        return

    def printCallsAndPuts(self, tick): # For testing a certain stock
        date = options.get_expiration_dates(tick)
        chain = options.get_options_chain(tick, date[0])
        print(chain)
        return


bo = BestOptions()
print("Which sector would you like to view?")
print("1. All\n2. Basic Materials\n3. Communication Services\n4. Consumer Cyclical\n5. Consumer Defensive")
print("6. Energy\n7. Financial Services\n8. Healthcare\n9. Industrials\n10. Real Estate")
choice = int(input("11. Technology\n12. Utilities\n13. Miscellaneous\n"))

bo.getTickerList()
bo.populateSectors()
# temp = bo.basicMaterials()
chosen_sector = bo.getSector(choice)
bo.topFive(chosen_sector)
# stock = "cf"
# bo.printCallsAndPuts(stock)


# closestc = bo.closestCallStrike(stock, cur_stock_price, closing_dates[0])
# closestp = bo.closestPutStrike(stock, cur_stock_price, closing_dates[0])
# print(closestc)
# print(closestp)
