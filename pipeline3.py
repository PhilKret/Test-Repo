#!/usr/bin/env python
# coding: utf-8

# In[145]:


import pandas as pd
import requests
import json
import os


# In[146]:


token = os.environ['MSTEAMS']


# In[94]:


url = 'https://coast.hhla.de/api/execute-report/Standard-Report-Segelliste'


# In[95]:


r = requests.get(url)


# In[96]:


# mit json Modul den textabruf wieder als json

data = json.loads(r.text) 


# In[97]:


# mit json_normalize den richtigen Pfad der json ansteuern, mit T transponieren/um 90 Grad drehen

einzel_df = pd.json_normalize(data['resultTables'][0]['rows'][0]).T 


# In[98]:


einzel_df


# In[99]:


# erste Zeile zu Spaltennamen

einzel_df.columns = einzel_df.iloc[0]


# In[100]:


einzel_df = einzel_df[1:]


# In[101]:


einzel_df


# In[102]:


# wie viele Zeilen haben wir?

zeilen = data['resultTables'][0]['totalNumberOfRows']
zeilen


# In[103]:


# Schleife für alle rows in der Liste

dfliste = [] #wie erstellen eine leere liste in die wir die dfs  packen

for id in range(0,zeilen):   # hinter dem for wird immer eine temporäre Variable eingefügt die dann die range enthält und im Loop eingesetzt werden kann
    einzel_df = pd.json_normalize(data['resultTables'][0]['rows'][id]).T 
    einzel_df.columns = einzel_df.iloc[0]
    einzel_df = einzel_df[1:]
    dfliste.append(einzel_df)
    
 


# In[110]:


df_komplett = pd.concat(dfliste)


# In[111]:


df_komplett = df_komplett.sort_values(by='schiffabfertigung.ankunftsollzeitpunkt')
df_komplett = df_komplett.reset_index()
df_komplett


# In[112]:


df_komplett['schiffabfertigung.ankunftsollzeitpunkt'] = pd.to_datetime(df_komplett['schiffabfertigung.ankunftsollzeitpunkt'])


# In[113]:


# nur deepsea Shciffe rausfiltern

df_deepsea = df_komplett[df_komplett['schiffabfertigung.schiffstyp'] == 'DEEPSEA']


# In[114]:


df_deepsea


# In[115]:


# nur die schiffe die nächste Woche ankommen

import datetime


# In[116]:


# timezonenkompatibilität herstellen

import pytz


# In[117]:


utc=pytz.UTC


# In[118]:


heute = utc.localize(datetime.datetime.now()) # was ist heute?


# In[122]:


df_deepsea_abheute = df_deepsea[df_deepsea['schiffabfertigung.ankunftsollzeitpunkt'] > heute]


# In[123]:


df_deepsea_abheute15 = df_deepsea_abheute.iloc[:15]
df_deepsea_abheute15


# In[124]:


df_deepsea_abheute15['schiffabfertigung.schiffsname']


# In[136]:


new_str = [str(x) for x in df_deepsea_abheute15['schiffabfertigung.schiffsname']]
text = ','.join(new_str)
text


# In[126]:


# Über Teams Webhooks schicken

get_ipython().system('pip install pymsteams')


# In[132]:


import pymsteams


# In[143]:


# You must create the connectorcard object with the Microsoft Webhook URL
myTeamsMessage = pymsteams.connectorcard(token)

# Add text to the message.
myTeamsMessage.text(f"Die nächsten Schiffe sind: {text}")


# In[144]:


# send the message.
myTeamsMessage.send()


# In[ ]:




