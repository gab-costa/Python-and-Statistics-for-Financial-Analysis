#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
fb = pd.read_csv('facebook.csv')
fb=pd.DataFrame(fb)

fb.index=fb['Date']
x = pd.DatetimeIndex(fb.index)
#mpl.style.use('classic')
fb.index = x

fb


# In[ ]:


fb.loc['2015-01-02':'2015-12-31', 'Close']


# In[ ]:


plt.figure(figsize=(10, 8))
fb['Close'].plot()
plt.show()


# In[ ]:


fb[['Open', 'Close']] # select the two columns

fb['Price1']=fb['Close'].shift(-1)
fb


# In[ ]:


fb['PriceDiff']=fb['Price1']-fb['Close']
fb


# In[ ]:


fb['Daly_return']=fb['PriceDiff']/fb['Close']
fb


# In[ ]:


fb['Direction'] = [1 if fb.loc[x, 'PriceDiff']>0 else -1 for x in fb.index] # list comprehension
fb


# In[7]:


#fb['Average3']= (fb['Close'] + fb['Close'].shift[1] + fb['Close'].shift(2))/3

fb['MA40'] = fb['Close'].rolling(40).mean()
fb['MA200'] = fb['Close'].rolling(200).mean()


fb['Close'].plot()
fb['MA40'].plot()
fb['MA200'].plot()


# In[8]:


plt.figure(figsize=(10, 8))

fb['MA40'].loc['2015-01-01':'2015-12-31'].plot(label='MA40')
fb['Close'].loc['2015-01-01':'2015-12-31'].plot(label='Close')
plt.legend()
plt.show()


# ## STRATEGY - fast signal and slow signal

# In[6]:


fb['MA10']= fb['Close'].rolling(10).mean() #fast signal
fb['MA50']= fb['Close'].rolling(50).mean()


fb['MA10'].loc['2015-01-01':'2015-12-31'].plot(label='MA10')
fb['Close'].loc['2015-01-01':'2015-12-31'].plot(label='Close')
fb['MA50'].loc['2015-01-01':'2015-12-31'].plot(label='MA50')
plt.legend()
plt.show()


# In[ ]:


fb['Shares']=[1  if fb.loc[x, 'MA10']> fb.loc[x,'MA50'] else 0 for x in fb.index]
fb


# In[ ]:


fb['Profit']=[fb.loc[x,'Price1']-fb.loc[x, 'Close'] if fb.loc[x, 'Shares']==1 else 0 for x in fb.index]
fb


# In[ ]:


fb['Profit'].plot()
plt.axhline(y=0, color='red')


# In[ ]:


fb['Wealth']=fb['Profit'].cumsum()
fb.tail()


# In[ ]:




