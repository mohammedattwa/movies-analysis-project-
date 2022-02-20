#!/usr/bin/env python
# coding: utf-8

# 
# 
# # Project: TMDb movie data analysis
# 
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# ### Dataset Description 
# 
# >in this project, i will analyze the data associated with the development of the movies over 90 years. I’m interested to find the trends among the top movies and describe the effect of technology on the budget of production. This data set contains information about 10,000 movies collected from The Movie Database (TMDb), including user ratings and revenue.it also contains cast, director, runtime, release year, production company. the data set provide the information about genres of each movie and overview. this data not only provide the information about real revenue and budget but also offer the information about the effect of inflation on this budget and revenue.
# The final two columns ending with “_adj” show the budget and revenue of the associated movie in terms of 2010 dollars, accounting for inflation over time.
# 
# 
# ### Question(s) for Analysis
# > we can analyze the data provided by data set to answer some question 
# ### Q1 progress in number of movies by time? what are top 5 years according to number of released movies?
# ### Q2 progress in production companies’ number? top 5 companies in movies production according to movies number?
# ### Q3 How the profit change with time? and compare with the data taking inflation in our consideration?
# ### Q4 Top 5 year with highest profit? Top 5 production companies according to profit?
# ###  Q5 Number of movies by month? Which month has largest number of released movies? 
# ### Q6 Which month is most profitable?
# ### Q7 which is the dominant genre?
# ### Q8 progress of run time?
# ### Q9 what's longest movie and shortest movie?
# ### Q10 How the vote-average change with time?
# ### Q11 what's the top 5 movies due to rating? and what's the worst movies?
# 
# 
# 

# In[1]:


# Use this cell to set up import statements for all of the packages that you
#   plan to use.
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
import datetime

# Remember to include a 'magic word' so that your visualizations are plotted
#   inline with the notebook. See this page for more:
#   http://ipython.readthedocs.io/en/stable/interactive/magics.html


# In[2]:


# Upgrade pandas to use dataframe.explode() function. 
get_ipython().system('pip install --upgrade pandas==0.25.0')


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# 
# 
# ### General Properties

# In[3]:


df=pd.read_csv("tmdb-movies.csv")
df.head(1)
# Load your data and print out a few lines. Perform operations to inspect data
#types and look for instances of missing or possibly errant data.


# In[4]:


df.info()
#display information about the data set


# In[5]:


sum(df.duplicated())
df.drop_duplicates(inplace=True)
#check the duplication 
#remove duplicated rows


# In[6]:


df.isnull().sum()
#check the null values


# 
# ### Data Cleaning
# 

# In[7]:


# After discussing the structure of the data and any problems that need to be
# cleaned, perform those cleaning steps in the second part of this section.
df.drop(["imdb_id","homepage","tagline","keywords","overview"],axis=1,inplace=True)
#remove unnesseray column that will be not used in analysis 
df['budget_adj']=df['budget_adj']/1000000
df['revenue_adj']=df['revenue_adj']/1000000
df['budget']=df['budget']/1000000
df['revenue']=df['revenue']/1000000
df['release_date'] = pd.to_datetime(df['release_date'])
df['Month'] = df['release_date'].dt.month
df["profit"]=df["revenue"]-df["budget"]
df["inflation profit"]=df["revenue_adj"]-df["budget_adj"]
#make month column
df.head(2)
#check the data set 


# In[8]:


df_genres=df[df['genres'].notna()]
df_genres.info()
#form the data new data set that has non nane values for generes to make analysis easier on genres
#check the information about new data set  


# In[9]:


df_production_companies=df[df['production_companies'].notna()]
df_production_companies.info()
#form the data new data set that has non nane values for production_companies to make analysis easier on genres
#check the information about new data set  


# In[10]:


df_money=df.query("revenue_adj > 0& budget_adj > 0 & budget>0 & revenue>0")
df_money.head(1)
#form the data new data set that has non zero values for money to make analysis easier on genres
#check the information about new data set  


# In[11]:


df_time=df.query("runtime > 0")
df_time.head(1)
#form the data new data set that has non zero values for runtime to make analysis easier on genres
#check the information about new data set  


# In[12]:


df.describe()


# In[13]:


df.hist(figsize=(20,10));


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# > *
# 
# ### Q1 progress in number of movies by time? what are top 5 years according to number of released movies?
# 

# In[14]:


df.groupby("release_year")["id"].count().plot(kind="bar",figsize=(30,8),width=0.8,fontsize=20);
plt.xlabel("year",fontsize=20)
plt.ylabel("movies number",fontsize=20)
plt.title("number of movies per year",fontsize=20)
#Classification of movies by year and count the number of movies have been released in each year 


# graph comment : there's a remarkable increase in movie production. movies number increase exponentially by time

# In[15]:


df.groupby("release_year")["id"].count().nlargest(5)
# the top 5 year according to number of movies 


# ### Q2 progress in production companies’ number? top 5 companies in movies production according to movies number?

# In[16]:


df_production_companies.groupby("release_year")["production_companies"].nunique().plot(kind="bar",figsize=(30,8),width=0.8,fontsize=20);
plt.xlabel("year",fontsize=20)
plt.ylabel("number of companies",fontsize=20)
plt.title("number of production companies per year",fontsize=20)
#Classification of production companies by year and count the number of companies that released movies in each year


# In[17]:


df_production_companies.groupby("release_year")["production_companies"].nunique().iloc[-1]/df_production_companies.groupby("release_year")["production_companies"].nunique().iloc[0]


# graph comment :the number of production company increase by time , it reach to mor than 18 times over 55 year.

# In[18]:


df_production_companies["production_companies"].value_counts().nlargest(5)
# the top 5 production companies according to number of movies 


# In[19]:


df_production_companies.groupby("release_year")["production_companies"].value_counts().nlargest(1)


# ### Q3 How the profit change with time? and compare with the data taking inflation in our consideration?

# In[20]:


fig, ax = plt.subplots()
df_money.groupby("release_year")["profit"].mean().plot(figsize=(30,8),fontsize=20,color="green");
df_money.groupby("release_year")["inflation profit"].mean().plot(figsize=(30,8),fontsize=20,color="blue");
plt.ylabel("million $",fontsize=20)
plt.legend(["inflation profit","profit"],fontsize=25,loc=2)
ax2 = ax.twinx()
df_money.groupby("release_year")["id"].count().plot(secondary_y = True,color="red",fontsize=20);
plt.ylabel("number of movies",fontsize=20)
plt.legend(["number of movies"],fontsize=25,loc=9)
ax.set_xlabel("Year",fontsize=20)
plt.title("profit, inflation profit and number of movies Vs year",fontsize=30)
# Classification of profit and inflation profit with year


# In[21]:


df_money.groupby("release_year")["inflation profit"].mean().iloc[:31].mean()


# In[22]:


df_money.groupby("release_year")["inflation profit"].mean().iloc[31:].mean()


# ### Q4 Top 5 year with highest profit? Top 5 production companies according to profit?

# In[23]:


df_money.groupby("release_year")["inflation profit"].mean().nlargest(5)
# top 5 profitable year per movie , with inflation 


# In[24]:


df_money.groupby("release_year")["profit"].mean().nlargest(5)
#top 5 profitable year per movie , without inflation 


# In[25]:


df_money.groupby("production_companies")["inflation profit"].sum().nlargest(5)
#top 5 profitable production_compaies , with inflation


# In[26]:


df_money.groupby("production_companies")["profit"].sum().nlargest(5)
#top 5 profitable production_compaies , without inflation


# ###  Q5 Number of movies by month? Which month has largest number of released movies? 

# In[27]:


df.groupby("Month")["id"].count().plot(kind="bar",figsize=(20,8),width=0.2,fontsize=20);
plt.xlabel("month",fontsize=20)
plt.ylabel("movies number",fontsize=20)
plt.title("number of movies per month",fontsize=20)
#Classification of movies by month of release


# In[28]:


df.groupby("Month")["id"].count().nlargest(2)
#the top 2 month crowded with movies


# In[29]:


(df.query("Month==9")["id"].count()+df.query("Month==10")["id"].count())/df["id"].count()


# graph comment : september followed by october are the most two crowded monthes with movies

# ### Q6 Which month is most profitable?

# In[30]:


df_money.groupby("Month")["profit"].mean().plot(figsize=(30,8),fontsize=20,color="blue");
plt.ylabel("million $",fontsize=20)
plt.legend(["profit"],fontsize=25,loc=2)
plt.xlabel("month",fontsize=20)
plt.title("profit Vs month",fontsize=20)
#Classification of mean profit gained per month


# In[31]:


df_money.groupby("Month")["profit"].mean().nlargest(2)


# comment graph : june and May are most profitable months 

# ### Q7 which is the dominant genre?

# In[32]:


fig = plt.figure(figsize=(15,15), dpi=200)
ax = plt.subplot(111)
df_genres['genres'].str.get_dummies(sep='|').sum().sort_values(ascending=False).plot(kind="barh");
#separte the genres of each movie and count the each genre.
plt.xlabel("number of movies")
plt.ylabel("genre")
plt.title("genre Vs number of movies")


# In[33]:


df_genres['genres'].str.get_dummies(sep='|').sum()["Drama"]/10842


# comment graph : Drama , comedy are the most common genre .only the Drama represted about 43% of all movies released over 55 year 

# In[34]:


dfy_genres=df_genres['genres'].str.get_dummies(sep='|')
dfy_genres["year"]=df_genres["release_year"]
dfy_genres.head(2)


# In[35]:


dfy_genres.groupby("year").sum().agg(['idxmax','max'], axis=1).tail(5)


# ### Q8 progress of run time ?

# In[36]:


df_time.groupby("release_year")['runtime'].mean().plot();
plt.ylabel("average runtime")
plt.xlabel("year")
plt.title("average runtime Vs year")
# the mean runtime change by year


# In[37]:


df_time["release_year"].corr(df_time["runtime"]) 


# comment graph : the mean of runtime of movies decrease by time 

# In[38]:


df_time.plot.scatter("runtime","popularity");
plt.title("runetime Vs popularity")


# ## Q9 what's longest movie and shortest movie?

# In[39]:


x=df_time["runtime"].max()
df_time.query("runtime=={}".format(x))[["original_title","runtime"]]
#longest movie released over 55 year


# In[40]:


y=df_time["runtime"].min()
df_time.query("runtime=={}".format(y))[["original_title","runtime"]]
# the list of shortest movies released over 55 year


# ## Q10 How the vote-average change with time?

# In[41]:


df.groupby("release_year")["vote_average"].mean().plot()
plt.ylabel("mean vote_average")
plt.title("mean vote_average per year")
# mean of movie rating over time 


# In[42]:


df.query("vote_average>7")['vote_average'].count()/df['vote_average'].count()
# percentage of movies that have rating more than 7


# ### Q11 what's the top 5 movies due to rating? and what's the worst movies?

# In[43]:


df.sort_values("vote_average")[["original_title","vote_average"]].tail(5)
#top 5 movies due to rating


# In[44]:


df.sort_values("vote_average")[["original_title","vote_average"]].head(5)
# the list of 5 worst movie due to raring


# In[53]:


df_money.sort_values("profit")[["original_title","profit"]].tail(1)


# In[54]:


df_money.sort_values("inflation profit")[["original_title","inflation profit"]].tail(1)


# <a id='conclusions'></a>
# ## Conclusions
# 
# > from this analysis, we conclude that the production of movies is in progress since about 25% of movies were produced in last 5 year (2011:2015). Only in 2014, about 700 movies were released and this year is considered as the most crowded month since 1960 until 2015.  It’s not only the number of movies increased but also the number of production companies increased about 18 times over 55 years. the paramount pictures company comes in the first place in the movies production with 156 movies followed by universal pictures with 133 movies. In only 1991, paramount pictures company produced 11 movies. Since 1990, there’s exponential increase in number of movies released .in contrast, profit is seeming constant over the range 1990: 2015.taking inflation in our consideration, the mean profit before 1990 is larger than twice of that after 1990. In 1965, the highest mean profit recorded (552.65 million dollars)with implementation of inflation. But if inflation is neglected ,2015 come in the first place. Paramount Pictures company is the
#  largest company making profit (9.3 billion dollars).
# September followed by October are the most crowed months. about 22% of movies released since 1960 to 2015 were released in September and October. Although, the most profitable month was June 
# followed by May.
#  Drama and comedy movies are the most dominant genres. drama genre is appeared in about 43.9% of 
# Movies released. Since 2011 to 2015, all movies come in dramatic scenario.   
# average time length of movies produced are 102 min. by time, we noticed that mean of time-length of movies decreased.so we can conclude that the audience nowadays prefer the short movies. The Story of Film: An Odyssey is the longest movie, it lasts 900 min. on the other hand, Fresh Guacamole, Cousin Ben Troop Screening, The Adventures of AndrÃ© and Wally B.,Luxo Jr. and Bambi Meets Godzilla last only 2 min.
# mean the average rate of movies is 5.975012. with time the mean of average vote decreases also it's noticed that less than 12% of movies produced over 55 years take rate higher than 7. The Story of Film: An Odyssey take highest rate about 9.2 followed by The Mask You Live In movie. Manos: The Hands of Fate and Transmorphers movies had been get the least rate about 1.5 .
# 
# 
# ### Limitations
# > i think some of data are missing which leads to not accurate analysis process.some of movies has revenue and budget eaual to zero.there is 6016 movies have zero as value of revenue and about 5696 movies have zero budget and about 4701 movies have both as zero value. Also , there are large number of missing data in production company.also there are 31 values of runtime have 0 as values
# 
# 
# 

# In[ ]:





# In[ ]:





# In[46]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])

