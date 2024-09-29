import pandas as pd
import glob, pytz, re
import numpy as np
from datetime import datetime as dt 

#EXCTRACTION
#define file path
path = 'D:\data_sources\data_reqruitment'

#get csv file within path
getFile = glob.glob(path + '/*.csv')

#extract csv file within path and make dataframe for it
df = pd.read_csv(getFile[0])

#drop unnecessary columm with no meaning that appear after reading from csv file
df.drop(columns={'Unnamed: 0'}, inplace=True)


# ================================================================================================================================================ #

#TRANSFORMATION
#specify timezone for transformation dates purpose
localTz = pytz.timezone('Asia/Jakarta')

#function for cleansing company value, there's regex logic inside of it
def cleansingCompany(company):
    return re.search(r'[A-Za-z\s]+', company).group()

#function for cleansing salary estimate in year
def cleansingSalary(salary):
    try:
        if '/hr' in salary:
            return float(re.search(r'[\d\.\,]+', salary).group().replace(',','')) * 2080
        elif '/mon' in salary:
            return float(re.search(r'[\d\.\,]+', salary).group().replace(',','')) * 12
        else:
            return float(re.search(r'[\d\.\,]+', salary).group().replace(',',''))
    except AttributeError:
        return re.search(r'[\d\.\,]+', salary)

#apply cleansingCompany method
df['company'] = df['company'].apply(lambda x: cleansingCompany(str(x)).replace('\n',''))

#replace 'unknown' values with null/nan
df['company_revenue'] = df['company_revenue'].apply(lambda x: np.nan if x == 'Unknown / Non-Applicable' else x)
df['company_type'] = df['company_type'].apply(lambda x: np.nan if x == 'Unknown' else x)
df['company_size'] = df['company_size'].apply(lambda x: np.nan if x == 'Unknown' else x)

#converting datetime with local timezone Jakarta
df['dates'] = df['dates'].apply(lambda x: dt.strptime(x,'%Y-%m-%d %H:%M:%S%z').astimezone(localTz))

#cleansing salary estimate in year
df['salary_estimate'] = df['salary_estimate'].apply(lambda x: cleansingSalary(str(x)))

# ================================================================================================================================================ #

#DEMOGRAPHY

print('1. How many Data Engineer job in market')
print(60 * '=')
print(len(df.loc[df['job_title'].str.contains('DATA ENGINEER', na=False, case=False)]))
print('')
print('2. 5 industries that need Data Engineer the most')
print(60 * '=')
print(df.loc[df['job_title'].str.contains('DATA ENGINEER', na=False, case=False), 'company_industry'].value_counts().head(5))
print('')
print('3. 5 job that has highest salary')
print(60 * '=')
print(df[['job_title','salary_estimate']].sort_values( by=['salary_estimate'], ascending=False).head(5))
print('')
print('4. How many companies that have no ratings')
print(60 * '=')
print(df['company_rating'].isna().sum())
print('')
print('5. Average Salary in every industries')
print(60 * '=')
grp_by = df.groupby(['company_industry'])
print(grp_by['salary_estimate'].mean().sort_values(ascending=False))
