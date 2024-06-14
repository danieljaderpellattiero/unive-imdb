#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np

import os

os.chdir(os.getcwd()+"/input_tsv/")


# In[2]:


# Function to convert the second field format to the first field format
def transform_field(field):
    return "["+','.join(["\""+s+"\"" for s in field.split(",")])+"]"


# # Name basics

# In[3]:


name_basics=pd.read_csv('name.basics.tsv', encoding='utf-8', sep='\t',index_col='nconst',na_values='\\N')
#name_basics


# In[4]:


#name_basics.isna().sum()


# In[5]:


name_basics["primaryName"]=name_basics["primaryName"].fillna("Unknown")


# In[6]:


name_basics['birthYear']=name_basics['birthYear'].fillna(-1).astype(int)
name_basics['deathYear']=name_basics['deathYear'].fillna(-1).astype(int)


# In[7]:


name_basics['primaryProfession']=name_basics['primaryProfession'].astype(str).apply(transform_field)


# In[8]:


name_basics.drop(['knownForTitles'],axis=1,inplace=True)


# In[9]:


#name_basics.isna().sum()


# In[10]:


#name_basics.info()


# In[11]:


name_basics.rename(columns={'primaryName':'fullName','birthYear':'birth','deathYear':'death','primaryProfession':'professions'},inplace=True)


# In[12]:


name_basics.index.name='id'


# In[13]:


#name_basics


# # Title Basics

# In[14]:


title_basics=pd.read_csv('title.basics.tsv', sep='\t', index_col='tconst', na_values='\\N')
title_basics


# In[15]:


#title_basics.info()


# In[16]:


#title_basics.isna().sum()


# In[17]:


title_basics.dropna(subset=["primaryTitle"],inplace=True)
title_basics


# In[18]:


titles=title_basics.loc["tt13704268"]["primaryTitle"].split("\t")
title_basics.at["tt13704268","primaryTitle"]=titles[0]
title_basics.at["tt13704268","originalTitle"]=titles[1]
title_basics.at["tt13704268","isAdult"]=0


# In[19]:


title_basics.loc["tt13704268"]


# In[20]:


title_basics["startYear"]=title_basics["startYear"].fillna(-1).astype(int)

title_basics["endYear"] = title_basics["endYear"].fillna(title_basics["startYear"]).astype(int)


# In[21]:


#title_basics.isna().sum()


# In[22]:


title_basics["runtimeMinutes"]=title_basics["runtimeMinutes"].fillna(-1)

temp=title_basics[title_basics["runtimeMinutes"].apply(pd.to_numeric, errors='coerce').isna()].index

title_basics.loc[temp,"genres"]=title_basics.loc[temp,"runtimeMinutes"]
title_basics.loc[temp,"runtimeMinutes"]=-1

title_basics["runtimeMinutes"]=title_basics["runtimeMinutes"].astype(int)


# In[23]:


title_basics["genres"]=title_basics["genres"].astype(str)
title_basics["genres"]=title_basics["genres"].apply(transform_field)


# In[24]:


#title_basics["genres"].value_counts()


# In[25]:


#title_basics.isna().sum()


# In[26]:


title_basics.rename(columns={'primaryTitle':'nameEng','originalTitle':'name','isAdult':'isAdult','startYear':'startYear','endYear':'endYear','runtimeMinutes':'runtime','genres':'genres'},inplace=True)
title_basics.index.name='id'

#title_basics


# # Title AKA

# In[27]:


title_aka=pd.read_csv('title.akas.tsv', sep='\t', na_values='\\N')


# In[28]:


#title_aka


# In[29]:


#title_aka.isna().sum()


# In[30]:


title_aka.dropna(subset=["title"],inplace=True)
#title_aka


# In[31]:


title_aka.loc[title_aka["isOriginalTitle"]==1,"region"] = "Original"
title_aka["region"]=title_aka["region"].fillna("Unknown")


# In[32]:


#title_aka.isna().sum()


# In[33]:


title_aka.drop(['language','isOriginalTitle','types','attributes'],axis=1,inplace=True)


# In[34]:


#title_aka


# In[35]:


title_aka.rename(columns={'ordering': 'ordering','title':'name','region':'region','titleid':'titleId'},inplace=True)
title_aka.index.name='id'


# In[36]:


#title_aka


# # Title Ratings

# In[37]:


title_ratings=pd.read_csv('title.ratings.tsv', sep='\t', na_values='\\N', index_col='tconst')


# In[38]:


title_ratings.rename(columns={'averageRating':'rating','numVotes':'votes'},inplace=True)
title_ratings.index.name='titleId'


# In[39]:


#title_ratings


# # JOIN

# In[40]:


title_basics_ratings=title_basics.join(title_ratings)


# In[41]:


title_basics_ratings.dropna(subset=["rating"],inplace=True)


# In[42]:


#title_basics_ratings


# In[43]:


#title_basics_ratings["titleType"].value_counts()


# In[44]:


title_aka=title_aka[title_aka["titleId"].isin(title_basics_ratings.index)]


# In[45]:


title_aka["nameLower"]=title_aka["name"].str.lower()


# In[46]:


title_aka=title_aka.join(title_basics_ratings,
            on='titleId', rsuffix='_r').sort_values(by=['votes','titleId'],ascending=False).drop(['titleType','nameEng','name_r','isAdult','startYear','endYear','runtime','genres','rating','votes'],axis=1)


# In[47]:


#title_aka


# # Split 

# In[48]:


title_basics_ratings_episode=title_basics_ratings[title_basics_ratings["titleType"]=="tvEpisode"]
title_basics_ratings_no_episode=title_basics_ratings[title_basics_ratings["titleType"]!="tvEpisode"]


# In[49]:


#title_basics_ratings_episode


# In[50]:


#title_basics_ratings_no_episode


# ## Title Aka: titleId split

# In[51]:


#title_aka=title_aka.assign(titleId_basic=[x if x in title_basics_ratings_no_episode.index else "-1" for x in title_aka["titleId"]],
#                            titleId_episode=[x if x in title_basics_ratings_episode.index else "-1" for x in title_aka["titleId"]])


# In[52]:


#title_aka.drop(['titleId'], axis=1, inplace=True)


# In[53]:


#title_aka


# # Title Episode

# In[54]:


title_episode=pd.read_csv('title.episode.tsv', sep='\t', na_values='\\N', index_col='tconst')


# In[55]:


#title_episode


# In[56]:


title_episode=title_episode.merge(title_basics_ratings_episode, left_index=True,right_index=True)


# In[57]:


title_episode.drop(['titleType'],axis=1,inplace=True)


# In[58]:


title_episode.rename(columns={'parentTconst':'titleId','seasonNumber':'season','episodeNumber':'episode'},inplace=True)
title_episode.index.name='id'


# In[59]:


#title_episode.isna().sum()


# In[60]:


title_episode["season"]=title_episode["season"].fillna(-1).astype(int)
title_episode["episode"]=title_episode["episode"].fillna(-1).astype(int)


# In[61]:


#title_episode.isna().sum()


# # Title Principal

# In[62]:


title_principal=pd.read_csv('title.principals.tsv', sep='\t', na_values='\\N')


# In[63]:


#title_principal.isna().sum()


# In[64]:


title_principal["job"]=title_principal["job"].fillna(title_principal["category"])


# In[65]:


title_principal.drop(['category'],axis=1,inplace=True)


# In[66]:


#title_principal.isna().sum()


# In[67]:


#title_principal


# In[68]:


title_principal["characters"]=title_principal["characters"].fillna("[]")


# In[69]:


title_principal["characters"]=title_principal["characters"].astype(str)


# In[70]:


#title_principal["characters"].apply(type).unique()


# In[71]:


#title_principal["characters"].unique()


# In[72]:


title_principal.rename(columns={'tconst':'titleId','nconst':'personId'},inplace=True)


# In[73]:


#title_principal


# In[74]:


title_principal=title_principal[title_principal["titleId"].isin(title_basics_ratings.index)]
#title_principal


# # Title Crew

# In[75]:


title_crew=pd.read_csv('title.crew.tsv', sep='\t', na_values='\\N')


# In[76]:


#title_crew


# In[77]:


title_crew.rename(columns={'tconst':'titleId'},inplace=True)


# In[78]:


#title_crew.isna().sum()


# In[79]:


title_crew=title_crew.fillna("")


# In[80]:


title_crew["directors"]=title_crew["directors"].astype(str).apply(transform_field)
title_crew["writers"]=title_crew["writers"].astype(str).apply(transform_field)


# In[81]:


#title_crew


# In[82]:


title_crew=title_crew[title_crew["titleId"].isin(title_basics_ratings.index)]


# In[83]:


title_crew.set_index('titleId',inplace=True)


# In[84]:


#title_crew


# # Finals

# In[85]:


os.chdir(os.getcwd()+"/../parquet/")
print(os.getcwd())


# In[86]:


name_basics.index.name='_id'
#name_basics


# In[87]:


name_basics.to_parquet('name.basics.parquet')


# In[88]:


title_basics=title_basics_ratings_no_episode
title_basics.index.name='_id'
#title_basics


# In[89]:


title_basics.to_parquet('title.basics.parquet')


# In[90]:


title_episode.index.name='_id'
#title_episode


# In[91]:


title_episode.to_parquet('title.episodes.parquet')


# In[92]:


title_aka.reset_index(inplace=True, drop=True)
#title_aka


# In[93]:


title_aka.to_parquet('title.akas.parquet',index=False)


# In[94]:


#title_principal


# In[95]:


title_principal.to_parquet('title.principals.parquet',index=False)


# In[96]:


title_crew.index.name='_id'
#title_crew


# In[97]:


title_crew.to_parquet('title.crew.parquet',index=True)


# # 
