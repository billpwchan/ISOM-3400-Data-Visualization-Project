#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 14:02:05 2018

@author: ivan
"""

# Loading Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Specify MatPlot Style
plt.style.use('ggplot')

# LoadibreadBasketdataset to variable breadBasket
breadBasket = pd.read_csv('BreadBasket.csv', na_values="NONE")

# Remove Nan Values
breadBasket.dropna(inplace=True)

# Mask date and time column as datatime
breadBasket['Date'] = pd.DatetimeIndex(breadBasket['Date'])

# Creating Summary Statistics dataframe
dataSetStats = pd.DataFrame()

# Number of Transactions
dataSetStats.loc[0, 'Num_Trans'] = breadBasket['Transaction'].unique().size

# Numer of Distinct Items Purchased
dataSetStats.loc[0, 'Num_Distinct_Items'] = breadBasket['Item'].unique().size

# Average Size of Purchase
dataSetStats.loc[0, 'Avg_Size_of_Purchase'] = breadBasket['Transaction'].size / \
    breadBasket['Transaction'].unique().size

# Weekday Distribution
weekDay = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
dayMap = {day: str(weekDay.index(day) + 1) for day in weekDay}

# Time Period Distribution
timePeriod = ['0900-1000', '1000-1100', '1100-1200', '1200-1300',
              '1300-1400', '1400-1500', '1500-1600', '1600-1700', '1700-1800']
timeMap = {time: time[:2] for time in timePeriod}

itemList = breadBasket['Item'].unique()


# Functions for extracting Time Period Indicator
def extractTime(inputStr):
    return inputStr[:2]

# Functions for extracting DayofWeek of DateTimeIndex
def extractDayOfWeek(inputDate):
    return str(inputDate.dayofweek)

# Functions for extracting item
def extractItem(inputStr):
    return str(inputStr)


# Item Sold by Time of Day
Item_Sold_Time = pd.DataFrame(columns=timePeriod, index=weekDay)
for time in timePeriod:
    for day in weekDay:
        Item_Sold_Time.loc[day, time] = breadBasket[(breadBasket['Time'].apply(extractTime) == timeMap[time])
                                                    & (breadBasket['Date'].apply(extractDayOfWeek) == dayMap[day])]['Item'].count()
del time, day

# Best Seller by Time & weekDay
Best_Seller_Time = pd.DataFrame(columns=weekDay, index=timePeriod)
for day in weekDay:
    for time in timePeriod:
        Best_Seller_Time.loc[time, day] = breadBasket[(breadBasket['Time'].apply(extractTime) == timeMap[time])
                                                 & (breadBasket['Date'].apply(extractDayOfWeek) == dayMap[day])]['Item'].mode().values
del day, time

# Item Sold by Category
Item_Sold_Category = pd.DataFrame(columns=breadBasket['Item'].unique())
for item in itemList:
    Item_Sold_Category[item] = breadBasket[breadBasket['Item'].apply(
        extractItem) == item].count()

# Remove Unnecessary Rows retrieved from Count()
Item_Sold_Category.drop(Item_Sold_Category.index[[0, 1, 3]], inplace=True)


def plot_chart(option):
    xAxis = timePeriod
    targetDataFrame = Item_Sold_Time
    yLabel = 'Item Sold'
    chartTitle = 'Item Sold by Time of Day'
    if (option == '1'):
        xAxis = breadBasket['Item'].unique()
        targetDataFrame = Item_Sold_Category
        chartTitle = 'Items Sold by Category'
    if (option == '2'):
        # String-based DataFrame. Not suitable for plotting.
        print(Best_Seller_Time)
        return
    if (option == '4'):
        print(dataSetStats)
        return
    # To place the xTicks evenly on the x-Axis
    plt.bar(np.arange(len(tuple(xAxis))),
            targetDataFrame.sum(), align='center', alpha=0.5)
    plt.xticks(np.arange(len(tuple(xAxis))), tuple(xAxis))

    # Chart Property Setup
    plt.ylabel(yLabel)
    plt.title(chartTitle)

    # Chart Display
    plt.show()

def init():
    displayMsg = "Please select the chart to display: \n 0) Quit the Program. \n 1) Item Sold by Category \n 2) Best Seller \n 3) Item Sold by Time of Day\n 4) Display Statistics \n"
    # Asking User Input for displaying chart accodingly
    option = input(displayMsg)
    while (option != '0'):
        plot_chart(option)
        option = input("Please select the chart to display:")


init()






