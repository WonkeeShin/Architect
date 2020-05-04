#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


import json


# In[3]:


import datetime


# In[4]:


# python json 파일 불러오기
with open('./2020_APRIL.json', encoding='utf-8') as t:
    geo = json.load(t)


# In[5]:


# json 파일의 내부를 예쁘게 보기 위해서 pprint 사용
from pprint import pprint


# In[6]:


# json 파일 확인
pprint(geo)


# ## 1. 어떤 장소를 많이 갔는가.

# In[ ]:


# 원하는 정보만 가져와서 DataFrame으로 만들기 위해 뽑아내는 작업.
# 주소 정보와 이동 정보가 랜덤하게 존재해서 그냥 편하게 try로 처리했다.

# 주소 정보 가져오는 작업
place = []
for i in range(len(geo['timelineObjects'])):
    try:
        latitude = geo['timelineObjects'][i]['placeVisit']['location']['latitudeE7']
        longitude = geo['timelineObjects'][i]['placeVisit']['location']['longitudeE7']
        address = geo['timelineObjects'][i]['placeVisit']['location']['address']
        starttime = geo['timelineObjects'][i]['placeVisit']['duration']['startTimestampMs']
        endtime = geo['timelineObjects'][i]['placeVisit']['duration']['endTimestampMs']
        starttime_date = datetime.datetime.fromtimestamp(int(starttime)/1000)
        endtime_date = datetime.datetime.fromtimestamp(int(endtime)/1000)
        during = endtime_date - starttime_date
        place.append([latitude, longitude, address, during.seconds/3600])
    except:
        pass


# In[8]:


# 위도, 경도, 주소, 기간 dataframe 생성
placedata = pd.DataFrame(place, columns=['latitude', 'longitude', 'address', 'during'])


# In[9]:


placedata


# In[10]:


# 위도, 경도 기준으로 합산하여 총 방문 시간 알기.
# 내림차순으로 정렬.
placedata.groupby(['latitude', 'longitude']).sum().sort_values(by=['during'], ascending=False)


# In[186]:


# 각각의 방문 장소를 방문 기간을 기준으로 내림차순
placedata.sort_values(by=['during'], ascending=False)[:15]


# In[11]:


# 지도 위에 표시하기 위한 folium 가져오기
import folium


# In[12]:


# 연습삼아 찍어보기
m = folium.Map(location=[37.3078652, 126.8304404], zoom_start=17)


# In[13]:


m


# In[14]:


# 방문기간이 길었던 상위 5개 장소만 지도위에 마커로 찍어보기

m2 = folium.Map(location=[37.5665, 126.9780])

folium.Marker([37.3202124,126.8331436], popup='<b>Timberline Lodge</b>', icon=folium.Icon(color = 'red')).add_to(m2)
folium.Marker([37.5757637,127.0307465], popup='<b>Timberline Lodge</b>', icon=folium.Icon(color = 'green')).add_to(m2)
folium.Marker([37.5761860,127.0306720], popup='<b>Timberline Lodge</b>', icon=folium.Icon(color = 'black')).add_to(m2)
folium.Marker([37.3078384,126.8304749], popup='<b>Timberline Lodge</b>', icon=folium.Icon(color = 'white')).add_to(m2)
folium.Marker([37.3078822,126.8304859], popup='<b>Timberline Lodge</b>', icon=folium.Icon(color = 'pink')).add_to(m2)


# In[15]:


m2


# In[16]:


# 방문했던 모든 장소 마커로 찍어보기

m3 = folium.Map(location=[37.5665, 126.9780])

for i in range(placedata.latitude.size):
    folium.Marker([placedata.latitude[i]/1e7 ,placedata.longitude[i]/1e7], popup='<b>Timberline Lodge</b>', icon=folium.Icon(color = 'red')).add_to(m3)


# In[17]:


m3


# ## 2. 어떤 방법으로 얼마나 이동했는가

# In[18]:


# 이동 시간 데이터 가져와보기
geo['timelineObjects'][2]['activitySegment']['duration']['startTimestampMs']


# In[19]:


# 원하는 정보만 가져와서 DataFrame으로 만들기 위해 뽑아내는 작업.
# 주소 정보와 이동 정보가 랜덤하게 존재해서 그냥 편하게 try로 처리했다.

# 이동 정보 가져오는 작업

move = []
for i in range(len(geo['timelineObjects'])):
    try:
        activityType = geo['timelineObjects'][i]['activitySegment']['activityType']
        distance = geo['timelineObjects'][i]['activitySegment']['distance']
        starttime = geo['timelineObjects'][i]['activitySegment']['duration']['startTimestampMs']
        endtime = geo['timelineObjects'][i]['activitySegment']['duration']['endTimestampMs']
        starttime_date = datetime.datetime.fromtimestamp(int(starttime)/1000)
        endtime_date = datetime.datetime.fromtimestamp(int(endtime)/1000)
        during = endtime_date - starttime_date
        move.append([activityType, distance, during.seconds/60])
    except:
        pass


# In[20]:


# 이동 형태, 거리, 이동시간 데이터 프레임으로 만들기
move_df = pd.DataFrame(move, columns=['activityType', 'distance', 'during'])


# In[21]:


# 이동거리 km 단위로 보여주기
move_df.distance = move_df.distance/1000


# In[24]:


# 이동시간 min 단위로 보여주기
move_df.during = move_df.during*60


# In[25]:


move_df


# In[26]:


# 칼럼 이름에 단위 포함하도록 칼럼 이름 변경
move_df.rename({'distance' : 'distance(km)', 'during':'during(min)'}, axis=1, inplace=True)


# In[27]:


move_df


# In[28]:


# 이동 형태별 합산
move_df.groupby(['activityType']).sum()

