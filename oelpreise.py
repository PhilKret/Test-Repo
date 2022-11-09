#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests


# In[7]:


# xls files mit pd.read_excel() auslesen
# Excel Tabelle besteht aus mehrere Sheets --> anwählen über sheet_name=
# mit skiprows= überspringen wir Zeilen, die wir nicht brauchen

df = pd.read_excel('https://www.eia.gov/dnav/pet/hist_xls/RBRTEd.xls', sheet_name='Data 1', skiprows=2)


# In[6]:


df


# In[8]:


# Spalten anders benennen

df.columns = ['Datum', 'Dollars pro Barrel']


# In[9]:


df


# In[10]:


df.info() # erkennt er das Datumsformat?


# In[15]:


df = df.set_index('Datum') # Datum als Index


# In[17]:


df_resampled = df.resample('M').mean() # monatlichen Durchschnitt berechnen mit resample().mean()


# In[18]:


df_resampled # unser dataframe ist fertig




# In[20]:


df_resampled.to_csv('oelpreis.csv') #csv export


# In[ ]:




