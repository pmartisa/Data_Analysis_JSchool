#!/usr/bin/env python
# coding: utf-8

# ### Do your imports!

# In[701]:


import pandas as pd
import numpy as np
pd.set_option("display.max_columns", None)


# In[823]:


df = pd.read_csv("subset.csv", encoding='utf-8', nrows= 7000000, na_values=['UNKNOWN'])


# # 311 data analysis
# 
# ## Read in `subset.csv` and review the first few rows
# 
# Even though it's a giant file – gigs and gigs! – it's a subset of the [entire dataset](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9). It covers plenty of years, but not all of the columns.
# 
# If your computer is struggling (which it will!) or you are impatient, feel free to use `nrows=` when reading it in to speed up the process by only reading in a subset of columns. Pull in at least a few million, or a couple years back.

# In[703]:


df.head(15)


# ### Where the subset came from
# 
# If you're curious, I took the [original data](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9/data) and clipped out a subset by using the command-line tool [csvkit](https://csvkit.readthedocs.io/en/latest/).
# 
# First I inspected the column headers:
# 
# ```bash
# $ csvcut -n 311_Service_Requests_from_2010_to_Present.csv 
# ```
# 
# Then I selected the columns I was interested in and saved it to a file.
# 
# ```bash
# $ csvcut -c 1,2,3,4,5,6,7,8,9,10,16,17,20,26,29 311_Service_Requests_from_2010_to_Present.csv > subset.csv
# ```
# 
# This was much much much much faster than doing it in Python.

# ## We want more columns!
# 
# **Right now we don't see all of the columns.** For example, mine has `...` between the **Incident Address** column and the **City** column. Go up to the top where you imported pandas, and add a `pd.set_option` line that will allow you to view all of the columns of the dataset.

# In[ ]:





# ## We hate those column names!
# 
# Change the column names to be tab- and period-friendly, like `df.created_date` instead of `df['Created Date']`

# In[825]:


df.columns = df.columns.str.lower().str.replace(" ", "_")
df.head(15)


# # Dates and times
# 
# ## Are the datetimes actually datetimes?
# 
# We're going to be doing some datetime-y things, so let's see if the columns that look like dates are actually dates.

# In[705]:


df.dtypes
# datetimes are strings


# ## In they aren't datetimes, convert them
# 
# The ones we're interested in are as follows:
# 
# * Created Date
# * Closed Date
# 
# You have two options to convert them:
# 
# 1. Do it like we did in class, but **overwrite the existing string columns with the new datetime versions**
# 2. Find an option with `read_csv` to automatically read certain columns as dates! Use the shift+tab trick to read the `read_csv` docs to uncover it. Once you find it, you'll set it to be the **list of date-y columns**.
# 
# They're both going to take forever if you do them wrong, but can be faster with a few tricks. For example, using `pd.to_datetime` can be sped up significantly be specifying the format of the datestring.
# 
# For example, if your datetime was formatted as `YYYY-MM-DD HH:MM:SS AM`, you could use the following:
# 
# ```
# df.my_datetime = pd.to_datetime(df.my_datetime, format="%Y-%m-%d %I:%M:%S %p")
# ```
# 
# It's unfortunately much much much faster than the `read_csv` technique. And yes, [that's `%I` and not `%H`](https://strftime.org/).
# 
# > *Tip: What should happen if it encounters an error or missing data?*

# In[834]:


df.created_date = pd.to_datetime(df.created_date, format="%m/%d/%Y %I:%M:%S %p")


# In[835]:


df.closed_date = pd.to_datetime(df.closed_date, format="%m/%d/%Y %I:%M:%S %p")
#df.dtypes


# ## According to the dataset, which month of the year has the most 311 calls?
# 
# The kind of answer we're looking for is "January," not "January 2021"

# In[708]:


# there are two big techniques for date stuff: .dt or .resample
# if you use one of those, explain why you picked that one and not the other


# In[709]:


df.created_date.dt.month.value_counts()
# it seems overall that March has the highest number of calls


# ## According to the dataset, which month has had the most 311 calls?
# 
# The kind of answer we're looking for is "January 2021," not "January" (although _techniucally_ it will say `2021-01-31`, not `January 2021`)

# In[710]:


# there are two big techniques for date stuff: .dt or .resample
# if you use one of those, explain why you picked that one and not the other


# In[711]:


df.resample('M', on='created_date').size().sort_values(ascending=False)

# May 2019 had the most 311 calls


# ## Plot the 311 call frequency over our dataset on a _weekly_ basis
# 
# To make your y axis start at zero, use `ylim=(0,100000)` when doing `.plot`. But replace the `1000` with a large enough value to actually see your data nicely!

# In[712]:


# there are two big techniques for date stuff: .dt or .resample
# if you use one of those, explain why you picked that one and not the other


# In[867]:


df.resample('W', on='created_date').size().sort_index().plot(ylim=(0,70000))


# ## What time of day (by hour) is the least common for 311 complains? The most common?
# 

# In[714]:


# there are two big techniques for date stuff: .dt or .resample
# if you use one of those, explain why you picked that one and not the other


# In[715]:


df.created_date.dt.hour.value_counts()

# the most common hour is midnight
# the less common hour is 4 am


# ### Make a graph of the results
# 
# * Make sure the hours are in the correct order
# * Be sure to set the y-axis to start at 0
# * Give your plot a descriptive title

# In[866]:



df.created_date.dt.hour.value_counts().sort_index().plot(ylim=(0,3000000), title="Most 311 complains are made at midnight")


# # Agencies
# 
# ## What agencies field the most complaints in the dataset? Get the top 5.
# 
# Use the `agency` column for this one.

# In[717]:


df.agency.value_counts().head(5)


# ## What are each of those agencies?
# 
# Define the following five acronyms:
# 
# * NYPD
# * HPD
# * DOT
# * DSNY
# * DEP

# In[718]:


# NYPD: New York Police Department 
# HPD: Housing Preservation and Development
# DOT: Department of Transportation
# DSNY: NYC Department of Sanitation
# DEP: Department of Environmental Protection
df.agency_name.value_counts().head(15)


# ## What is the most common complaint to HPD?

# In[719]:


# Why did you pick these columns to calculate the answer?
# Because there is one column with all the different kinds of complaints
# so I just filtered to just show ONLY the kind of complaints issued to HPD


# In[720]:


df.complaint_type[df.agency == "HPD"].value_counts().head(5)


# ## What are the top 3 complaints to each agency?
# 
# You'll want to use the weird confusing `.groupby(level=...` thing we learned when reviewing the homework.

# In[785]:


df.groupby('agency').complaint_type.value_counts().groupby(level=0, group_keys=False).nlargest(3)


# ## What is the most common kind of residential noise complaint?
# 
# The NYPD seems to deal with a lot of noise complaints at homes. What is the most common subtype?

# In[722]:


# Why did you pick these columns to calculate the answer?
# Because I wanted to know what was the most common value within the type 'noise-residential'


# In[723]:


df.descriptor[df.complaint_type == "Noise - Residential"].value_counts().head(5)


# ## What time of day do "Loud Music/Party" complaints come in? Make it a chart!

# In[724]:


# there are two big techniques for date stuff: .dt or .resample
# if you use one of those, explain why you picked that one and not the other


# In[784]:


df[df.complaint_type == "Noise - Residential"].created_date.dt.hour.value_counts().sort_index().plot(ylim=(0,40000))


# ## When do people party hard?
# 
# Make a monthly chart of Loud Music/Party complaints since the beginning of the dataset. Make it count them on a biweekly basis (every two weeks).

# In[726]:


# there are two big techniques for date stuff: .dt or .resample
# if you use one of those, explain why you picked that one and not the other


# In[727]:


df[df.complaint_type == "Noise - Residential"].resample('2W', on='created_date').size().plot()


# ## People and their bees
# 
# Sometimes people complain about bees! Why they'd do that, I have no idea. It's somewhere in "complaint_type" – can you find all of the bee-related complaints?

# In[728]:


df[df.complaint_type.str.contains("bee", case=False)]


# ### What month do most of the complaints happen in? I'd like to see a graph.

# In[729]:


# most complaints happen in May
df[df.complaint_type == "Harboring Bees/Wasps"].created_date.dt.month.value_counts().sort_index().plot(kind='barh')


# ### Are the people getting in trouble usually beekeepers or not beekeepers?

# In[832]:


df.descriptor[df.complaint_type == "Harboring Bees/Wasps"].value_counts()
# The are more not beekepers complaining


# # Math with datetimes
# 
# ## How long does it normally take to resolve a 311 complaint?
# 
# Even if we didn't cover this in class, I have faith that you can guess how to calculate it.

# In[836]:


df['time_to_fix'] = df['closed_date'] - df['created_date']


# Save it as a new column called `time_to_fix`

# ## Which agency has the best time-to-fix time?

# In[837]:


df.groupby('agency').time_to_fix.median().sort_values().head()


# ## Maybe we need some more information...
# 
# I might want to know how big our sample size is for each of those, maybe the high performers only have one or two instances of having requests filed!
# 
# ### First, try using `.describe()` on the time to fix column after your `groupby`.

# In[733]:


df.groupby('agency').time_to_fix.describe()


# ### Now, an alternative
# 
# Seems a little busy, yeah? **You can also do smaller, custom aggregations.**
# 
# Try something like this:
# 
# ```python
# # Multiple aggregations of one column
# df.groupby('agency').time_to_fix.agg(['median', 'size'])
# 
# # You can also do something like this to reach multiple columns
# df.groupby('agency').agg({
#     'time_to_fix': ['median', 'size']
# })
# ```

# In[734]:


df.groupby('agency').time_to_fix.agg(['median', 'size'])


# In[735]:


df.groupby('agency').agg({
    'time_to_fix': ['median', 'size']
})


# ## Seems weird that NYPD time-to-close is so fast. Can we break that down by complaint type?
# 
# Remember the order: 
# 
# 1. Filter
# 2. Group
# 3. Grab a column
# 4. Do something with it
# 5. Sort

# In[869]:


df[df.agency == "NYPD"].groupby('complaint_type').time_to_fix.median().sort_values()


# ## Back to median fix time for all agencies: do these values change based on the borough?
# 
# First, use `groupby` to get the median time to fix per agency in each borough. You can use something like `pd.set_option("display.max_rows", 200)` if you can't see all of the results by default!

# In[737]:


df.groupby(['agency', 'borough']).time_to_fix.agg(['median', 'size'])


# ### Or, use another technique!

# We talked about pivot table for a hot second in class, but it's (potentially) a good fit for this situation:
# 
# ```python
# df.pivot_table(
#     columns='what will show up as your columns',
#     index='what will show up as your rows',
#     values='the column that will show up in each cell',
#     aggfunc='the calculation(s) you want dont'
# )
# ```

# In[874]:


df.pivot_table(
    columns='borough',
    index='agency',
    values='time_to_fix',
    aggfunc= 'median'
)


# ### Use the pivot table result to find the worst-performing agency in the Bronx, then compare with Staten Island
# 
# Since it's a dataframe, you can use the power of `.sort_values` (twice!). Do any of the agencies have a large difference between the two?

# In[875]:


df.pivot_table(
    columns='borough',
    index='agency',
    values='time_to_fix',
).sort_values(by ='STATEN ISLAND', ascending=False).sort_values(by = 'BRONX', ascending=False)
# The worst performing agency in the Bronx is the Deparment of Buildings (DOB)
# We can see a large difference in how that same agency operates, in Staten Island, where is more efficient
# The opposite happens with EDC, which is much faster in the Bronx in comparison


# ## What were the top ten 311 types of complaints on Thanksgiving 2020? Are they different than the day before Thanksgiving?
# 
# **Finding exact dates is awful, honestly.** While you can do something like this to ask for rows after a specific date:
# 
# ```python
# df[df.date_column >= '2020-01-01']
# ```
# 
# You, for some reason, can't ask for an **exact match** unless you're really looking for exactly at midnight. For example, this won't give you what you want:
# 
# ```python
# df[df.date_column == '2020-01-01']
# ```
# 
# Instead, the thing you need to do is this:
# 
# ```python
# df[(df.date_column >= '2020-01-01') & (df.date_column < '2020-01-02']
# ```
# 
# Everything that starts at midnight on the 1st but *is still less than midnight on the 2nd**.

# In[871]:


df.complaint_type[(df.created_date >= '2020-11-26') & (df.created_date < '2020-11-27')].value_counts().head(10)


# In[872]:


# Day before Thanksgiving
df.complaint_type[(df.created_date >= '2020-11-25') & (df.created_date < '2020-11-26')].value_counts().head(10)


# ## What is the most common 311 complaint types on Christmas day?
# 
# And I mean *all Christmas days*, not just in certain years)
# 
# * Tip: `dt.` and `&` are going to be your friend here
# * Tip: If you want to get fancy you can look up `strftime`
# * Tip: One of those is much much faster than the other

# In[742]:


df.complaint_type[(df['created_date'].dt.day==25) & (df['created_date'].dt.month==12)].value_counts().head(10)
# The most common one by far is complaints related to heating


# # Stories
# 
# Let's approach this from the idea of **having stories and wanting to investigate them.** Fun facts:
# 
# * Not all of these are reasonably answered with what our data is
# * We only have certain skills about how to analyzing the data
# * There are about six hundred approaches for each question
# 
# But: **for most of these prompts there are at least a few ways you can get something interesting out of the dataset.**

# ## Fireworks and BLM
# 
# You're writing a story about the anecdotal idea that the summer of the BLM protests there were an incredible number of fireworks being set off. Does the data support this?
# 
# What assumptions is your analysis making? What could make your analysis fall apart?

# In[844]:


df['create_month'] = df.created_date.dt.strftime('%B')


# In[854]:


fireworks = df[df.complaint_type.str.contains("illegal firework", case=False)]
summer = fireworks[fireworks.create_month.isin(['June', 'July', 'August'])]
summer['year'] = summer.created_date.dt.strftime('%Y')
summer['monthyear'] = summer['year'] + summer['create_month']
summer.monthyear.value_counts().sort_index().plot(xlim=(0,12))


# In[800]:


## Even when the data is showing an exponential increase, these cases don't necessarily need to be related to BLM protests


# ## Sanitation and work slowdowns
# 
# The Dept of Sanitation recently had a work slowdown to protest the vaccine mandate. You'd like to write about past work slowdowns that have caused garbage to pile up in the street, streets to not be swept, etc, and compare them to the current slowdown. You've also heard rumors that it was worse in Staten Island and a few Brooklyn neighborhoods - Marine Park and Canarsie - than everywhere else.
# 
# Use the data to find timeframes worth researching, and note how this slowdown might compare. Also, is there anything behind the geographic issue?
# 
# What assumptions is your analysis making? What could make your analysis fall apart?

# In[ ]:





# ## Gentrification and whining to the government
# 
# It's said that when a neighborhood gentrifies, the people who move in are quick to report things to authorities that would previously have been ignored or dealt with on a personal basis. Use the data to investigate the concept (two techniques for finding gentrifying area are using census data and using Google).
# 
# What assumptions is your analysis making? What could make your analysis fall apart? Be sure to cite your sources. 

# In[ ]:





# ## 311 quirks
# 
# Our editor tried to submit a 311 request using the app the other day, but it didn't go through. As we all know, news is what happens to your editor! Has the 311 mobile app ever actually stopped working?
# 
# If that's a dead end, maybe you can talk about the differences between the different submission avenues: could a mobile outage disproportionately impact a certain kind of complaint or agency? How about if the phone lines stopped working?
# 
# What assumptions is your analysis making? What could make your analysis fall apart?

# In[841]:


df.groupby('agency').open_data_channel_type.value_counts() .groupby(level=0, group_keys=False).nlargest(3).sort_values(ascending=False)
# Some agencies like HPD or DSNY seem to depend completely on phone complaints
# so a phone lines cut could be really harmful
# Other like NYPD are much more diversified btw phone, online and mobile app complaints


# ## NYCHA and public funds
# 
# NYC's public housing infrastructure is failing, and one reason is lack of federal funds. While the recent spending bills passed through Congress might be able to help, the feeling is that things have really fallen apart in the past however-many years – as time goes on it gets more and more difficult for the agency in control of things to address issues in a timely manner.
# 
# If you were tasked with finding information to help a reporter writing on this topic, you will **not** reasonably be able to find much in the dataset to support or refute this. Why not? 
# 
# If you wanted to squeeze something out of this dataset anyway, what could an option be? (You might need to bring in another dataset.)

# In[ ]:




