#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from pandas import DataFrame
import numpy as np
import matplotlib as plt
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


#importing the HIV.xlsx file with estimated HIV prevalance % data (ages 15-49)
HIV = pd.read_excel("/Users/shristidhakal/Documents/Grad School/INFO5502/HIV.xlsx")
#renaming the countries column to "Country" in HIV.xlsx
HIV = HIV.rename(columns={'Estimated HIV Prevalence% - (Ages 15-49)': 'Country'})
HIV.head(3)


# In[3]:


#importing countries_by_continent file. This is a separate new file.. 
#..that has a list of countries separated by their respective continent.
continent = pd.read_excel("/Users/shristidhakal/Documents/Grad School/INFO5502/countries_by_continent.xlsx")
continent.head(3)


# In[4]:


#performing a left inner join to join HIV data and countries_by_continent data
merged_HIV = pd.merge(left=continent, right=HIV, how='left', on=['Country', 'Country'])
merged_HIV.head(3)


# In[5]:


#locating columns: years 2000-2011
years=merged_HIV.loc[:,['2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011']]
years.head(5)


# In[6]:


#calculating average of each country from 2000-2011
merged_HIV['average_2000to2011'] = years.mean(axis=1, skipna = 'True')
merged_HIV.head(5)


# In[7]:


#grouping countries by continent
highest_hiv = merged_HIV.groupby(['Continent', 'Country', 'average_2000to2011']).idxmax(axis=1, skipna=True)
highest_hiv.head(5)


# In[8]:


#countries in each continent with highest HIV from 2000 to 2011
#highest averages at the end..
highest_hiv = merged_HIV.loc[merged_HIV.groupby('Continent')['average_2000to2011'].idxmax()]
highest_hiv.head(6)


# In[9]:


#country in each continent with lowest HIV from 2000 to 2011
#lowest averages at the end..
lowest_hiv = merged_HIV.loc[merged_HIV.groupby('Continent')['average_2000to2011'].idxmin()]
lowest_hiv.head(6)


# In[10]:


#bar chart showing highest avg. HIV in each continent 2000-2011 ages 15-49
highest_hiv.plot.bar(x='Continent', y='average_2000to2011', rot=0)
plt.xticks(rotation=45)


# In[11]:


#bar chart showing lowest avg. HIV in each continent 2000-2011 ages 15-49
lowest_hiv.plot.bar(x='Continent', y='average_2000to2011', rot=0, 
                    color='olive')
plt.xticks(rotation=45)


# In[12]:


#assigning binary values to help differentiate the highs and lows, and
#putting the high and low values together for plotting
average = merged_HIV.groupby(['Continent']).mean()
average.head(10)
highest_hiv['binary'] = 'high'
lowest_hiv['binary'] = 'low'
highest_lowest = pd.concat([highest_hiv, lowest_hiv, average], axis=0)
highest_lowest.head(8)


# In[13]:


#plot: high and low average HIV by continent
highest_lowest.plot.bar(x='Continent', y='average_2000to2011', rot=0)
plt.xticks(rotation='vertical')


# In[14]:


#countries without the highest and lowest HIV values selected
other_countries = merged_HIV.loc[(merged_HIV['Country'] == "Brazil") | 
                                 (merged_HIV['Country'] == "United States") | 
                                 (merged_HIV['Country'] == "Nepal") | 
                                 (merged_HIV['Country'] == "South Africa") | 
                                 (merged_HIV['Country'] == "China") | 
                                 (merged_HIV['Country'] == "Australia") |
                                 (merged_HIV['Country'] == "India") | 
                                 (merged_HIV['Country'] == "Uganda") |
                                 (merged_HIV['Country'] == "Haiti") | 
                                 (merged_HIV['Country'] == "Jamaica") |
                                 (merged_HIV['Country'] == "Finland")]
other_countries.head(10)


# In[15]:


#Average HIV prevalence ages 15-49, years 2000-2011, plot by Country
#Of countries that lie between the highest or the lowest HIV prevalence
plt.plot( 'Country', 'average_2000to2011', data=other_countries, 
         marker='o', markerfacecolor='blue', markersize=12, 
         color='skyblue', linewidth=2)
plt.xticks(rotation='vertical')
plt.legend(["Avg. HIV Prevalence by Country"]);


# In[16]:


#Average HIV prevalence ages 15-49, years 2000-2011, plot by Continent
#Of selected countries that lie between the highest or the lowest HIV prevalence
plt.plot( 'Continent', 'average_2000to2011', data=other_countries, 
         marker='o', markerfacecolor='blue', markersize=12, 
         color='green', linewidth=2)
plt.xticks(rotation='vertical')
plt.legend(["Avg. HIV Prevalence by Continent"]);


# In[17]:


#average HIV estimated prvalence of each country from 1979 to 2011 
merged_HIV['average_1979to2011'] = merged_HIV.mean(axis=1, skipna = 'True')
merged_HIV.head(5)


# In[18]:


#grouping average HIV from 1970-2011 by continent
#averages at the end
averages_new = merged_HIV.groupby(['Continent']).mean()
averages_new.head(5)


# In[19]:


#creating a new table with a more simplified indexing to plot line charts
new_table = pd.DataFrame(columns=['Years', 'Africa', 'Asia', 'Europe', 
                                  'North America', 'South America','Oceania'])

new_table['Years'] = averages_new.columns
new_table['Africa'] = pd.DataFrame(averages_new.loc['Africa'].values)
new_table['Asia'] = pd.DataFrame(averages_new.loc['Asia'].values)
new_table['Europe'] = pd.DataFrame(averages_new.loc['Europe'].values)
new_table['North America'] = pd.DataFrame(averages_new.loc['North America'].values)
new_table['South America'] = pd.DataFrame(averages_new.loc['South America'].values)
new_table['Oceania'] = pd.DataFrame(averages_new.loc['Oceania'].values)

new_table.head(5)


# In[20]:


#Line chart for each continent showing changes in the average HIV estimated..
#..prevalence from 1979 to 2011.

africa_plot = new_table[['Years', 'Africa']].plot('Years')
africa_plot.set_ylabel('Estimated HIV Prevalence')
africa_plot.title.set_text('Average HIV Changes: years 1979-2011, Africa')

asia_plot = new_table[['Years', 'Asia']].plot('Years')
asia_plot.set_ylabel('Estimated HIV Prevalence')
asia_plot.title.set_text('Average HIV Changes: years 1979-2011, Asia')

europe_plot = new_table[['Years', 'Europe']].plot('Years')
europe_plot.set_ylabel('Estimated HIV Prevalence')
europe_plot.title.set_text('Average HIV Changes: years 1979-2011, Europe')

north_america_plot = new_table[['Years', 'North America']].plot('Years')
north_america_plot.set_ylabel('Estimated HIV Prevalence')
north_america_plot.title.set_text('Average HIV Changes: years 1979-2011, North America')

south_america_plot = new_table[['Years', 'South America']].plot('Years')
south_america_plot.set_ylabel('Estimated HIV Prevalence')
south_america_plot.title.set_text('Average HIV Changes: years 1979-2011, South America')

oceania_plot = new_table[['Years', 'Oceania']].plot('Years')
oceania_plot.set_ylabel('Estimated HIV Prevalence')
oceania_plot.title.set_text('Average HIV Changes: years 1979-2011, Oceania')


# In[21]:


#overlaid line chart of estimated HIV prevalence (1979-2011) by continent
plot = new_table.plot('Years')
plot.set_ylabel('Estimated HIV Prevalence')
plot.title.set_text('Estimated HIV Prevalence (1979-2011) By Continent')


# In[26]:


#scatter plot showing HIV data of 1990 by continent 
#scatter plot looks empty because most of the values were missing for 1990
avg_1990 = merged_HIV.loc[:, ['Country', 'Continent', '1990']]

avg_1990_1 = avg_1990.groupby('Continent').mean().iloc[0]['1990']
avg_1990_2 = avg_1990.groupby('Continent').mean().iloc[1]['1990']
avg_1990_3 = avg_1990.groupby('Continent').mean().iloc[2]['1990']
avg_1990_4 = avg_1990.groupby('Continent').mean().iloc[3]['1990']
avg_1990_5 = avg_1990.groupby('Continent').mean().iloc[4]['1990']

avg_1990.loc[avg_1990.Continent == 'Africa', '1990a'] = avg_1990_1 
avg_1990.loc[avg_1990.Continent == 'Africa', 'continent'] = 1
avg_1990.loc[avg_1990.Continent == 'Asia', '1990a'] = avg_1990_2 
avg_1990.loc[avg_1990.Continent == 'Asia', 'continent'] = 2
avg_1990.loc[avg_1990.Continent == 'Europe', '1990a'] = avg_1990_3
avg_1990.loc[avg_1990.Continent == 'Europe', 'continent'] = 3
avg_1990.loc[avg_1990.Continent == 'North America', '1990a'] = avg_1990_4
avg_1990.loc[avg_1990.Continent == 'North America', 'continent'] = 4
avg_1990.loc[avg_1990.Continent == 'South America', '1990a'] = avg_1990_5
avg_1990.loc[avg_1990.Continent == 'South America', 'continent'] = 5


plot_1990 = avg_1990.plot.scatter('1990a', '1990', c='continent', cmap='viridis')
plot_1990.set_xlabel('Average HIV Prevalence by Continent in 1990')
plot_1990.set_ylabel('HIV Est. Prevalence in 1990')


# In[25]:


#scatter plot showing HIV data of 2010 by continent 

avg_2010 = merged_HIV.loc[:, ['Country', 'Continent', '2010']]

avg_2010_1 = avg_2010.groupby('Continent').mean().iloc[0]['2010']
avg_2010_2 = avg_2010.groupby('Continent').mean().iloc[1]['2010']
avg_2010_3 = avg_2010.groupby('Continent').mean().iloc[2]['2010']
avg_2010_4 = avg_2010.groupby('Continent').mean().iloc[3]['2010']
avg_2010_5 = avg_2010.groupby('Continent').mean().iloc[4]['2010']

avg_2010.loc[avg_2010.Continent == 'Africa', '2010a'] = avg_2010_1 
avg_2010.loc[avg_2010.Continent == 'Africa', 'continent'] = 1
avg_2010.loc[avg_2010.Continent == 'Asia', '2010a'] = avg_2010_2 
avg_2010.loc[avg_2010.Continent == 'Asia', 'continent'] = 2
avg_2010.loc[avg_2010.Continent == 'Europe', '2010a'] = avg_2010_3
avg_2010.loc[avg_2010.Continent == 'Europe', 'continent'] = 3
avg_2010.loc[avg_2010.Continent == 'North America', '2010a'] = avg_2010_4
avg_2010.loc[avg_2010.Continent == 'North America', 'continent'] = 4
avg_2010.loc[avg_2010.Continent == 'South America', '2010a'] = avg_2010_5
avg_2010.loc[avg_2010.Continent == 'South America', 'continent'] = 5


plot_2010 = avg_2010.plot.scatter('2010a', '2010', c='continent', cmap='viridis')
plot_2010.set_xlabel('Average HIV Prevalence by Continent in 2010')
plot_2010.set_ylabel('HIV Est. Prevalence in 2010')


# In[ ]:




