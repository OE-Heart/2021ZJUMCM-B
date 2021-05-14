import numpy as np 
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
data = pd.read_excel("ini.xlsx")

NumOfPeople = data.shape[0]
if NumOfPeople >= 5 and NumOfPeople <= 7:
    NumOfClasses = 1
elif NumOfPeople >= 8 and NumOfPeople <= 10:
    NumOfClasses = 2
elif NumOfPeople >= 11 and NumOfPeople <= 12:
    NumOfClasses = 3
elif NumOfPeople >= 13 and NumOfPeople <= 15:
    NumOfClasses = 4

totalWorkDays = 0
totalWorkClasses = 0
for i in range(data.shape[0]):
    totalWorkDays += data.loc[:,"已工作天数"][i]
    totalWorkClasses += data.loc[:,"已安排A"][i]
    totalWorkClasses += data.loc[:,"已安排B"][i]
    totalWorkClasses += data.loc[:,"已安排C"][i]
    totalWorkClasses += data.loc[:,"已安排D"][i]
ratio = totalWorkClasses/totalWorkDays

