# the following program collates the data of the UN tourism data stored in a csv
# which can be found at https://data.un.org/_Docs/SYB/CSV/SYB66_176_202310_Tourist-Visitors%20Arrival%20and%20Expenditure.csv

import chardet
from urllib.request import urlopen, pathname2url
import pandas as pd

# 1. find the files encoding and use it to open the file with python
csv_path = r"SYB66_176_202310_Tourist-Visitors Arrival and Expenditure(Main).csv"

fileurl=r"file:"+pathname2url(csv_path)

rawfile = urlopen(fileurl, data=None, cafile=None, capath=None, cadefault=False, context=None).read()

fileencoding=chardet.detect(rawfile)["encoding"]

data= pd.read_csv(csv_path, encoding=fileencoding).iloc[:,:7]

data.rename(columns={"Region/Country/Area/Destination": "Country"}, inplace=True)
data["Value"] = data["Value"].str.replace(",","").astype("int")

# 2. to collate data of number of tourists and expenditure done by them we need to select that data seperately 
data_arrivals = data.loc[data.iloc[:,3] == "Tourist/visitor arrivals (thousands)"].iloc[:,:7].reset_index()
data_expenditure = data.loc[~(data.iloc[:,3] == "Tourist/visitor arrivals (thousands)")].iloc[:,:7].reset_index()

# 3. do dynamic variable creation with globals() to get the data of different years in different variables
years = [2005, 2010, 2019]

var_arrivals=[]
var_expenditure=[]
for i in years:
    a = "data_arrivals_"+str(i)
    b = "data_expenditure_"+str(i)
    var_arrivals.append(a)
    var_expenditure.append(b)
    globals()[a] = data_arrivals.loc[data_arrivals.Year == i]
    globals()[b] = data_expenditure.loc[data_expenditure.Year == i]

var_arrivals_ = [globals()[var] for var in var_arrivals]
var_expenditure_ = [globals()[var] for var in var_expenditure]

# 4. find the unique countries whose data for both arrivals and expenditure for years 2005, 2010 and 2019 is available 
countries = data.Country.unique()
var_arrives_countries = [var["Country"] for var in var_arrivals_]
var_expenditure_countries = [var["Country"] for var in var_expenditure_]

# 5. do some python and write the data in the csv
df = pd.DataFrame(columns=["Country","Year","Tourists","TourismRevenue","ExpbyaPerson","IncreaseinTourists","IncreaseinRevenue","IncreaseinExpbyaPerson"])

index = 0
for country in countries:
    three1 = sum([1 for countrylist in var_arrives_countries if country in list(countrylist)])
    three2 = sum([1 for countrylist in var_expenditure_countries if country in list(countrylist)])
    if three1 == 3 and three2 == 3:
        var_country_arrivals = [var.loc[var["Country"]==country] for var in var_arrivals_]
        var_country_expenditure = [var.loc[var["Country"]==country] for var in var_expenditure_]
        a = b = c = 0
        for i in zip(var_country_arrivals, var_country_expenditure):
            Country = country
            Year = int(i[0].Year)
            Tourists = int(i[0]["Value"])
            TourismRevenue = int(i[1]["Value"])
            ExpbyaPerson = (TourismRevenue*1000000)/(Tourists*1000)
            IncreaseinTourists = Tourists - a            
            a = Tourists
            IncreaseinRevenue = TourismRevenue - b
            b = TourismRevenue
            IncreaseinExpbyaPerson = ExpbyaPerson - c
            c = ExpbyaPerson
            df.loc[index] = [Country,Year,Tourists,TourismRevenue,ExpbyaPerson,IncreaseinTourists,IncreaseinRevenue,IncreaseinExpbyaPerson]
            index+=1

df.to_csv("collated_data.csv")