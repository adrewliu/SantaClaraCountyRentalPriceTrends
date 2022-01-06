'''
Names: Andrew Liu, Andrew Yee

rent.py: This file contains three main functions: meanPrice, priceTrend, and
currentRentBarChart. meanPrice calculates the means of each months rent in all the
zipcodes. priceTrent is a function that  plots the price trend of rents
for a all the cities in Santa Clara county or just for one city. currentRentBarChart
creates a bar chart that plots the most current rent for each zip code helping the user
see the price difference easier.

Extra Credit:
If my friend wants to list in a city with low rental prices I would suggest Campbell
in the graph with all the cities average rent, it was the lowest. It was also one of
the cities with a lower current rent in the bar chart.

'''
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import datetime



def printNums(func):
    '''
    decorator that helps functions print outputs
    :param func: The function that it will be applied to
    :return: returns the outputs of functions its called on
    '''
    def wrapper(*args, **kwargs):
        results = func(*args, **kwargs)
        print(results)
        return results
    return wrapper


class Rent:
    startMonth = 5
    startYear = 2018
    endMonth = 8
    endYear = 2019

    def __init__(self):
        self.rent = []
        self.arrRent = np.array(self.rent)
        self.cities = {}
        self.zipCodes = {}
        self.rowLength = 0
        self.cityList = []
        with open('zipCity.csv') as fh:
            reader = csv.reader(fh)
            for row in reader:
                citiesTemp = {row[1]: row[0]} #dictionary with city: zipcodes
                self.zipCodes[row[0]] = row[1]  #zipcode: city
                for city, zipCode in citiesTemp.items():
                    if city in self.cities.keys():
                        self.cities[city].append(row[0])
                    else:
                        self.cities[city] = [row[0]]

        print(citiesTemp)
        print(self.cities)
        print(self.zipCodes)

        f = open('rent.csv')
        reader = csv.reader(open('rent.csv'))
        data = [row for row in csv.reader(f)]
        f.close()
        
        fc = open('zipCity.csv')
        reader = csv.reader(open('zipCity.csv'))
        new_column = [row[0] for row in csv.reader(fc)]

        fc.close()
        new_data = []

        #create numpy array
        for i, item in enumerate(data):
            try:
                item.insert(0, new_column[i])
            except IndexError as e:
                item.extendleft(0, "placeholder")
            new_data.append(item)
        
        f = open('rentCombined.csv', 'w', newline='')
        csv.writer(f).writerows(new_data)
        f.close()

        with open('rentCombined.csv') as fh:
            reader = csv.reader(fh)
            for row in reader:
                self.rent.append(row)
            self.rowLength = len(row)
            self.arrRent = np.array(self.rent)

        for city in self.cities.keys():
            self.cityList.append(city)

    @printNums
    def meanPrice(self):
        '''
        finds the mean of each months rent for all zipcodes of a city
        :return: combinedMeanArr: a numpy array with all the averages
        '''

        self.combinedMeanArr = []
        tempArray = []
        self.arrRent = self.arrRent.astype(float)
        zipList = []
        zipTotal = 0

        for city in self.cities.keys():

            zipCount = len(self.cities[city])
            zipTotal = sum(zipList)
            zipList.append(zipCount)

            if zipTotal == 0:
                newArr = self.arrRent[0:(len(self.cities[city])), 1:self.rowLength]
            else:
                newArr = self.arrRent[zipTotal: (zipTotal + len(self.cities[city])), 1:self.rowLength]
            tempArray.append(newArr.mean(0))
        combinedMeanArr = np.array(tempArray)
        #print(combinedMeanArr)
        return combinedMeanArr

    def priceTrend(self, cityNum):
        '''

        :param cityNum: The value of the city the user chooses
        :return: Plots the mean prices of all the zipcodes of a city for each month
        '''

        fontP = FontProperties()
        fontP.set_size('small')

        plt.title("Rental Prices Across Time")
        plt.xlabel("Month")
        plt.ylabel("Cost of Rent (dollars)")
        plt.style.use('fivethirtyeight')
        plt.grid(True)
        plt.tight_layout()
        plt.xticks(rotation='vertical')
        plt.rcParams['figure.figsize'] = (8, 9)

        xval = []

        count = 0           #count to build the list of city numbers

        combinedMeanList = self.meanPrice()
        combinedMeanList = combinedMeanList.tolist() #turn the mean array into a list so it can be used for plotting

        _startMonth = Rent().startMonth
        _startYear = Rent().startYear
        _endMonth = Rent().endMonth
        _endYear = Rent().endYear

        dates = datetime.date(_startYear, _startMonth, 1) # this create a datetime date using the class attributes

        # this chunk of code stores the dates in xval
        temp = 0
        for month in range(_startMonth, _startMonth + self.rowLength-1):
            if _startMonth == 12:
                xval.append(str('{}/{}'.format(_startMonth, _startYear)))
                _startMonth = 1
                _startYear += 1
            else:
                xval.append(str('{}/{}'.format(_startMonth, _startYear)))
                _startMonth += 1

        if cityNum == -1:
            for i in range(len(combinedMeanList)):
                yval = combinedMeanList[i]
                plt.plot(xval, yval, marker='.', linewidth=2)
                plt.tick_params(labelsize=6)
                plt.xticks(rotation=45)
                plt.legend([self.cityList[i] for i in range(len(combinedMeanList))], loc='best', prop={'size': 6})

        else:
            for count in range(len(self.cityList)):
                if count == cityNum:
                    yval = combinedMeanList[count]
                    plt.plot(xval, yval, marker='.', linewidth=2)
                    plt.tick_params(labelsize=6)
                    plt.xticks(rotation=45)
                    plt.legend([self.cityList[cityNum]], loc='best', prop={'size': 6})
            #print(len(self.cityList))
           #print(self.cityList)
        #plt.show()

    @printNums
    def currentRentBarChart(self):
        '''
        Plots a bar chart that includes the current price for every zipcode
        :return: sortedDataPoints: the current prices of zipcodes
        '''
        plt.title("Current Rents per Zipcode")
        plt.xlabel("Zipcode")
        plt.ylabel("Cost of Rent (dollars)")
        # plt.style.use('fivethirtyeight')
        plt.xticks(rotation=45)
        xvalues = []
        yvalues = []
        bottom, top = plt.ylim()  # return the current ylim
        plt.ylim((2000, 4700))  # set the ylim to bottom, top

        flatRentList = self.arrRent.tolist()
        dataPoints = []

        for i in range(len(flatRentList)):
            dataPoints.append([flatRentList[i][-1], flatRentList[i][0]])
        sortedDataPoints = sorted(dataPoints, key=lambda x: x[1])
        for i in range(len(sortedDataPoints)):
            yvalues.append((sortedDataPoints[i][0]))

        for key, values in self.zipCodes.items():
            xvalues.append((values, key))

        yList = []
        for i in yvalues:
            #print("this is i", i)
            yList.append(float(i))
        #print("this is ylist", yList)
        pos = np.arange(len(xvalues))
        #print("yvalue length, xvalue length", len(yvalues), xvalues)
        plt.bar(pos, yList, color='blue', align='center', edgecolor='black')
        labelList = [str(xvalue) for xvalue in xvalues]
        plt.xticks(pos, labelList, fontsize=6)
        #plt.show()

        return sortedDataPoints


if __name__ == "__main__":
    #num = int(input("enter city number"))
    ren = Rent()
    #ren.meanPrice()
    #ren.priceTrend(num)
    #ren.currentRentBarChart()
