import kaggle

## Download latest version
#kaggle.api.authenticate()

#kaggle.api.dataset_download_files("yagunnersya/fifa-21-messy-raw-dataset-for-cleaning-exploring", path='.', unzip=True)

## import tools
import numpy as np
import pandas as pd

## Get data into a dataframe, print to check first few rows
fifa = pd.read_csv('Python/SQL/Cleaning_Transforming/fifa21rawdatav2.csv')
##print(fifa.head())



### Now check datatypes in the dataset
# pd.set_option('display.max_rows', None) # Setting this to none displays all rows
# pd.set_option('display.max_columns', None)
# fifa_types = fifa.dtypes
# print(fifa_types)



fifa.Height.unique()
def convert_height(x):
    if x[-1] == '"':
        x = x.replace("\"","")
        inch = int(x[2:]) * 2.54
        foot = int(x[0]) * 30.48
        return round(foot+inch)
    elif x[-1] == "m":
        return int(x[:-2])
    
fifa.Height = fifa.Height.apply(convert_height)
fifa.Height.unique()

fifa = fifa.rename(columns={'Height':'Height_cm'})
fifa.Weight.unique()
def weight_kg(x):
    if 'lbs' in x:
        x = x.replace('lbs','')
        x = float(x) * 0.45359237
        x = int(x)
        return x
    else:
        return int(x[:-2])
    
fifa.Weight = fifa.Weight.apply(weight_kg)
fifa = fifa.rename(columns={'Weight':'Weight_cm'})




## Remove unecessary newline characters from all columns so we do not have to do them individually

for column in fifa.select_dtypes(include=[object]):
    fifa[column] = fifa[column].str.replace('\n', '', regex = False)



## Drop unecessary columns
print(fifa.Name.unique())
#Renaming the column LongName as FullName
fifa = fifa.rename(columns={'LongName':'FullName'})
fifa.drop(fifa.columns [[3,4,18]],axis = 1,inplace = True)
print(fifa)


## Now, check for nulls in the data
print(fifa.isnull().sum())


## The Hits column has some null values so we replace with 0s
fifa.Hits = fifa.Hits.fillna('0')
print(fifa.info())



## Now I want to see what can be done with the 'Joined' column to clean up the format
from datetime import datetime
fifa['Joined']

def month_to_number(x):
    if x== 'Jan':
        return 1
    elif x == 'Feb':
        return 2
    elif x == 'Mar': 
        return 3
    elif x == 'Apr':
        return 4
    elif x == 'May':
        return 5
    elif x == 'Jun': 
        return 6
    elif x == 'Jul': 
        return 7
    elif x == 'Aug': 
        return 8
    elif x == 'Sep': 
        return 9
    elif x == 'Oct': 
        return 10
    elif x == 'Nov':  
        return 11
    elif x == 'Dec':  
        return 12
    
date = []
for x in range(len(fifa['Joined'])):
    d = fifa['Joined'][x]
    c = d.split(" ")
    month = str(month_to_number(c[0]))
    day = str(c[1].replace(',',''))
    year = str(c[2])
    if len(day) == 1:
        day = ('0'+str(day))
    date_long = (str(month)+'/'+str(day)+'/'+str(year))
    date_con = pd.to_datetime(date_long)
    date.append(date_con)
fifa['Joined'] = date
print(fifa['Joined'])



## For overall stats, I want to change to one uniform title
fifa = fifa.rename(columns = {'↓OVA': 'OVA'})

print(fifa.head())



## Now we can clean the 'contract' column
print(fifa.Contract.unique()) #some are on contract while others are on loan!

## define a function to change the values with 'on loan' as an "On loan" category
## define the players with active loans as Active and they can be located easily cause they contain '~'
def contract(a):
    if "On Loan" in a:
        a = 'ON LOAN'
        return a
    elif '~' in a:
        a = 'ACTIVE'
        return a
    elif 'Free' in a:
        a = "FREE"
        return a

fifa.Contract = fifa.Contract.apply(contract)
fifa.Contract = fifa.Contract.astype('category')
# Rename the column to Contract status
fifa = fifa.rename(columns={'Contract':'ContractStatus'})
print(fifa.head())




## Now I will clean up the positions column, from printing we can see that they are not organized
# print(fifa['Positions'].unique())

# Ordering position column leaving them in groups
temp_position = []
for x in range(len(fifa['Positions'])):
    y = sorted(fifa['Positions'][x].split(" "))
    yx = ' '.join(y)
    temp_position.append(yx)

fifa['Positions'] = temp_position
fifa['Positions'] = fifa['Positions'].astype(object)
fifa['Positions'].unique()





## Now let's clean up W/F, SM, and IR columns
# I will define a function to help remove the star
def remove_star(x):
    x = x.replace('★', '')
    return x
fifa.IR = fifa.IR.apply(remove_star)
fifa.SM = fifa.SM.apply(remove_star)
fifa['W/F'] = fifa['W/F'].apply(remove_star)
fifa.head()



## Now I want to clean up the release column and renaming
fifa["Release Clause"].unique()
def release(x):
    if 'M' in x:
        x = x.replace('M', '')
        x = float(x[1:]) * 1000000
        return round(x)
    elif "K" in x:
        x = x.replace('K', '')
        x = float(x[1:]) * 1000
        return round(x)
    else:
        return x
    
fifa["Release Clause"] = fifa["Release Clause"].apply(release)
fifa["Release Clause"].unique()
fifa = fifa.rename(columns={'Release Clause':'Release Clause_€'})
print(fifa)




## Wage will be cleaned up and renamed. To be specific, we add the pounds and remove the 'K'

fifa['Wage'].unique()
def wage(x):
    if 'K' in x:
        x = x.replace('K', '')
        x = int(x[1:]) * 1000
        return round(x)
    else:
        return int(x[1:])
fifa.Wage = fifa.Wage.apply(wage)
fifa.Wage.unique()
fifa = fifa.rename(columns={'Wage':'Wage €'})
print(fifa.iloc[:, 15:25]) #print to check if the changes have worked




## Value column is next 
fifa.Value.unique()
def value(x):
    if 'M' in x:
        x = x.replace('M', '')
        x = float(x[1:]) * 1000000
        return round(x)
    elif "K" in x:
        x = x.replace('K', '')
        x = float(x[1:]) * 1000
        return round(x)
    else:
        return int(x[1:])
    
fifa.Value = fifa.Value.apply(value)
# Rename the value column to value with the Euro sign
fifa = fifa.rename(columns={'Value':'Value €'})






## Hits
fifa.Hits.unique()
# define a function to replace K with an empty string and turn the value to a float so it can be added to 1000
def hitchange(h):
    if "K" in h:
        h = h.replace('K', "")
        h = float(h)* 1000
        return round(h)
    else:
        return h
    
fifa.Hits = fifa.Hits.apply(hitchange)
fifa.Hits.unique()
#converting the datatype from object to integer
fifa['Hits'] = fifa['Hits'].astype('int64')
fifa.head()

fifa.info()