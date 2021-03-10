#!/usr/bin/env python
# coding: utf-8

# ## Population and sampling

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
get_ipython().run_line_magic('matplotlib', 'inline')

data = pd.DataFrame()

data['Population']= [47, 48, 85, 20, 19, 13, 72, 16, 50, 60]
a_sample_without_replacement = data['Population'].sample(5, replace=False) # pick up a sample without replacement
a_sample_without_replacement


# ### Parameters
# 
# - mean
# - variance
# - standard deviation
# 
# 
# ### statistics
# 
# - sample mean
# - sample variance
# - sample standard deviation

# In[ ]:


# POpulaçaõ



print('population mean is ', data['Population'].mean())
print('population variance is', data['Population'].var(ddof=0)) # significa que o denominador da variancia da população eh N
print('population standard deviation is', data['Population'].std(ddof=0))
print('population size is', data['Population'].shape[0]) # shape 0 mostgra somente os numeros de linhas


# In[ ]:


# AMOSTRA

a_sample = data['Population'].sample(10, replace=True)
print('population mean is ', a_sample.mean())
print('population variance is', a_sample.var(ddof=1)) # Aqui o ddof eh 1 pq na amostra o denominador eh (n-1)
print('population standard deviation is', a_sample.std(ddof=1))
print('population size is', a_sample.shape[0]) # shape 0 mostgra somente os numeros de linhas


# In[ ]:


sample_length = 500
sample_variance_collection0 = [data['Population'].sample(50, replace=True).var(ddof=0) for i in range(sample_length)]
sample_variance_collection1 = [data['Population'].sample(50, replace=True).var(ddof=1) for i in range(sample_length)]
print('variancia da população eh ', data['Population'].var(ddof=0))

print('media da variancia da amostra com n eh ', pd.DataFrame(sample_variance_collection0)[0].mean())
print('media da variancia da amostra com n-1 eh ', pd.DataFrame(sample_variance_collection1)[0].mean())

# n-1 for sample is better


# # variation of sample

# In[ ]:


fstsample = pd.DataFrame(np.random.normal(10, 5, size=30))
print('a média da amostra eh', fstsample[0].mean())
print('o desvio padrao eh ', fstsample.std(ddof=1))


# In[17]:


# distr da média empiricamente
meanlist=[]
for x in range(1000):
    sample = pd.DataFrame(np.random.normal(10,5, size=30))
    meanlist.append (sample[0].mean())

collection = pd.DataFrame(meanlist) 
collection[0].hist(bins=100, figsize=(15,8))


# In[15]:


# See what central limit theorem tells you...the sample size is larger enough, 
# the distribution of sample mean is approximately normal
# apop is not normal, but try to change the sample size from 100 to a larger number. The distribution of sample mean of apop 
# becomes normal.
sample_size = 100
samplemeanlist = []
apop =  pd.DataFrame([1, 0, 1, 0, 1])
for t in range(10000):
    sample = apop[0].sample(sample_size, replace=True)  # small sample size
    samplemeanlist.append(sample.mean())

acollec = pd.DataFrame()
acollec['meanlist'] = samplemeanlist
acollec.hist(bins=100, figsize=(15,8))


# # Intervalo de confiança

# In[16]:


apple = pd.read_csv('apple.csv')
apple.index = apple['Date']
apple.index = pd.DatetimeIndex(apple.index)
apple['LogReturn'] = np.log(apple['Close']).shift(-1) - np.log(apple['Close'])
apple


# In[ ]:


sample_size = apple['LogReturn'].shape[0]
sample_mean = apple['LogReturn'].mean()
sample_std = apple['LogReturn'].std(ddof=1)/(sample_size**0.5)


# # teste de hipótese
# 

# In[14]:


# como os dados são de 1980 - 2020, vamos reduzi-los para 2017-2019

apple_red = apple.loc['2017-01-01' : '2019-01-01']

apple_red['LogReturn'] = np.log(apple_red['Close']).shift(-1) - np.log(apple_red['Close'])
apple_red['LogReturn'].plot(figsize=(20,8))
plt.axhline(0, color='red')



# $H_0 : \mu = 0$ 
# $H_a : \mu \neq 0$
# 
# H0 significa que a média do retorno da ação é 0
# 
# H1 significa que a média do retorno da ação é 1
# 

# In[ ]:


sample_mean = apple_red['LogReturn'].mean()
sample_mean = apple_red['LogReturn'].std(ddof=1)
n= apple_red['LogReturn'].shape[0]


z_hat =(sample_mean - 0)/(sample_std/n**0.5)

print('o valor de z_chapeu eh', z_hat)

sample_mean


# ### definindo o critério alpha = 0.05

# In[ ]:


alpha = 0.05
z_left = norm.ppf(alpha/2, 0, 1)
z_right = - z_left
print(z_left, z_right)


# ### Fazendo a decisão
# 

# In[ ]:


print ('Para um nível de significância de {}, devemos rejeitar H0: {}'.format(alpha, z_hat>z_right or z_hat<z_left) )


# In[ ]:




