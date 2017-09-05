import pandas as pd
import numpy as np
import datetime
import calendar
import re
import pdb


# Function to get last day of month of a year
def get_datetime(Year, Month):
	return datetime.date(Year,Month,calendar.monthrange(Year,Month)[1])

######### Start of Clean CPI Data ###########

df_cpi = pd.read_excel('Source Data\\Consumer Price Index.xlsx', parse_cols="A:C", skip_rows=3, header=3).iloc[0:439]

# Create Year Column
Year = [int(df_cpi.Year.values[0])]
for i in range(1, len(df_cpi.index)):
	Year.append(Year[i-1] + int((i)%12==0))
df_cpi['Year'] = Year

# Calculate year-to-year rate of change of CPI
df_cpi = df_cpi[df_cpi['Composite Consumer Price Index']!='N.A.']
df_cpi = df_cpi.reset_index(drop=True)
# From % to float
df_cpi['Composite Consumer Price Index'] = df_cpi['Composite Consumer Price Index']/100 + 1
# Prepare array of yearly rate
cpi_monthly = list(df_cpi['Composite Consumer Price Index'].values)
cpi_yearly = []
for i in range(0, len(cpi_monthly)):
	if i <= 10:
		continue
	else:
		cpi_yearly.append(np.product(cpi_monthly[i-11:i+1])-1)
		
# Drop first 11 rows and monthly rate column
df_cpi = df_cpi.iloc[11:len(df_cpi)]
df_cpi = df_cpi.drop('Composite Consumer Price Index',axis=1)
df_cpi = df_cpi.reset_index(drop=True)
# Copy array to dataframe
df_cpi['cpi_yearly'] = cpi_yearly

df_cpi['Month'] = df_cpi['Month'].apply(lambda x : list(calendar.month_abbr).index(x))
df_cpi['Date'] = df_cpi.apply(lambda row: get_datetime(row['Year'],row['Month']), axis=1)

df_cpi = df_cpi.drop(['Month','Year','Composite Consumer Price Index'],axis=1)

######### End of Clean CPI Data ###########




######### Start of Clean Unemployment Data ###########

df_unemployment_rate = pd.read_excel('Source Data\\Unemployment Rate.xlsx', parse_cols="A,F", header=3).iloc[169:465]
df_unemployment_rate = df_unemployment_rate.reset_index(drop=True)
# Remove space and other characters
df_unemployment_rate['Period'] = df_unemployment_rate['Period'].apply(lambda x: re.sub(r"[#@ .*]",r"",x))
# Get DateTime
df_unemployment_rate['Period'] = df_unemployment_rate['Period'].apply(lambda x: get_datetime(int(x.split('-')[1].split('/')[1]),int(x.split('-')[1].split('/')[0])))
# Rename the columns
df_unemployment_rate.columns = ['Date','Unemployment Rate']
# Change percentage to float
df_unemployment_rate['Unemployment Rate'] = df_unemployment_rate['Unemployment Rate'].apply(lambda x : float(x)/100)

######### End of Clean Unemployment Data ###########

######### Start of Merging Data ###########
df_clean = df_cpi.merge(df_unemployment_rate)
df_clean.to_csv('Source Data\\data_cleaned.csv')
######### End of Merging Data ###########

