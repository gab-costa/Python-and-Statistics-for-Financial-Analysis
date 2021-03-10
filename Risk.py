#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
fb= pd.read_csv('Facebook.csv')
fb.index=fb['Date']
fb.index = pd.DatetimeIndex(fb.index)

ap = pd.read_csv('Apple.csv')
ap.index = ap['Date']
ap.index = pd.DatetimeIndex(ap.index)


# # Distribuição de frequência
# 

# In[7]:



die = pd.DataFrame([1,2,3,4,5,6])

# rolando os dados 50 vezes 
trial=50
result = [die.sample(2, replace=True).sum().loc[0] for x in range(trial)]

np.mean(result)


# In[8]:


freq = pd.DataFrame(result)[0].value_counts()
sort_freq=freq.sort_index()
sort_freq


# In[9]:


sort_freq.plot(kind='bar', color= 'red')


# In[10]:


# relative frequency is frequency divided por number of trial
relative_freq = sort_freq / trial
relative_freq.plot (kind='bar', color='blue')


# In[11]:


trial_2 = 10000
results = [die.sample(2, replace=True).sum().loc[0] for i in range(trial_2)]
freq = pd.DataFrame(results)[0].value_counts()
sort_freq = freq.sort_index()
relative_freq = sort_freq/sort_freq.sum()
relative_freq.plot(kind='bar', color='purple')


# In[12]:


# assume that we have fair dice, which means all faces will be shown with equal probability
# then we can say we know the 'Distribtuion' of the random variable - sum_of_dice

X_distri = pd.DataFrame(index=[2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
X_distri['Prob'] = [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]
X_distri['Prob'] = X_distri['Prob']/36
X_distri


# In[13]:


# there is this formula in the book of statistics

mean = pd.Series(X_distri.index * X_distri['Prob']).sum()
var = pd.Series(((X_distri.index - mean)**2)*X_distri['Prob']).sum()
#Output the mean and variance of the distribution. Mean and variance can be used to describe a distribution
print(mean, var)


# In[14]:


# if we calculate mean and variance of outcomes (with high enough number of trials, eg 20000)...
trial = 200
results = [die.sample(2, replace=True).sum().loc[0] for i in range(trial)]


# In[15]:


#print the mean and variance of the 20000 trials
results = pd.Series(results)
print(results.mean(), results.var())


# # MODELOS DE DISTRIBUIÇÕES
# 
# ### Why is it important to know the distribution or model for stock return?
# 
# it's really crucial in risk management, for example, the stock price of apple drop over 40% 
# 

# In[16]:


ap.loc['2012-08-01':'2013-08-01', 'Close'].plot()


# In[17]:


# what the chance of the yearly return can  be less than 40 % 
ap['LogReturn']= np.log(ap['Close']).shift(-1) - np.log(ap['Close'])
ap['LogReturn'].hist(bins=50)


# In[18]:


from scipy.stats import norm
density = pd.DataFrame()
density['x'] = np.arange(-4, 4 , 0.001)
density['pdf']= norm.pdf(density['x'],0,1)
density['cdf']= norm.cdf(density['x'], 0, 1)
density
plt.plot(density['x'], density['pdf'])


# In[19]:


plt.plot(density['x'], density['cdf'])


# In[20]:


# aproximate mean and varience of the log daily return 
mu = ap['LogReturn'].mean()
sigma = ap['LogReturn'].std(ddof=1)
print(mu, sigma)


# # what is the chance of losing over 5% in a day?

# In[21]:


denApp = pd.DataFrame()
denApp['x']= np.arange(-0.1,0.1, 0.001)
denApp['pdf']=norm.pdf(denApp['x'], mu, sigma) # mu, sigma stands for (mean and standard deviation)


# In[22]:


plt.ylim(0,20)
plt.plot(denApp['x'], denApp['pdf'])
#plt.fill_between(x=np.arange(-0.1, -0.01, 0.0001), y2=0, y1=norm.pdf(np.arange(-0.1, 0.05, 0.0001), mu, sigma),facecolor='pink', alpha=0.5)


# # How about probability of dropping over 40% in a year (220 trading days)? 

# In[23]:


mu220 = 220*mu 
sigma220 = 220** 0.5*sigma
print(mu220, sigma220)

print('the prpobability of dropping over 40% in 220 days is', norm.cdf(-0.4, mu220, sigma220))


# ## Calculate Value at risk (VaR)

# In[24]:


# Value at risk(VaR)
VaR = norm.ppf(0.05, mu, sigma)
print('Single day value at risk ', VaR)

# Quatile 
# 5% quantile
print('5% quantile ', norm.ppf(0.05, mu, sigma))
# 95% quantile
print('95% quantile ', norm.ppf(0.95, mu, sigma))

