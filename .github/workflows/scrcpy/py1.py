# -*- coding: utf-8 -*-
import requests
import os,json,time

url='https://zh.stripchat.com/api/front/models?limit=99&offset=0&primaryTag=girls&filterGroupTags=[["tagLanguageChinese"]]&sortBy=stripRanking&parentTag=ethnicityAsian&userRole=guest'
r = requests.get(url)
play = r.json()['models']
play = sorted(play, key=lambda p:p['viewersCount'], reverse=True)
time_stamp = int(time.time())
time_array = time.localtime(time_stamp+8*3600)
str_date = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
#print(len(res))
path = 'wzaz259'
isExists=os.path.exists(path)
if not isExists:
    os.makedirs(path) 
with open("./wzaz259/playlist.json","w", encoding='utf-8') as f:
    json.dump(play,f)

with open('./wzaz259/playlist.dpl', 'w', encoding='utf-8') as w:
        w.write('DAUMPLAYLIST\ntopindex=0\nsaveplaypos=0\n')
        for i in range(0,len(play)):
            w.write(str(i+1)+'*file*'+play[i]["hlsPlaylist"].replace("_240p","")+'\n')
            w.write(str(i+1)+'*title*'+play[i]["username"]+'\n')
tvlive= ""
try:            
    response = requests.get("https://raw.githubusercontent.com/dxawi/0/main/tvlive.txt")
    tvlive = response.text
except Exception as e:
    console.log("tvlive error",e)
    
with open('./wzaz259/playlist.txt', 'w', encoding='utf-8') as w:
        w.write(tvlive)
        w.write("直播,#genre#\n")
        for i in range(0,len(play)):
            print(play[i]["username"]+','+play[i]["hlsPlaylist"].replace("_240p", ""))
            w.write(play[i]["username"]+','+play[i]["hlsPlaylist"].replace("_240p", "")+'\n')
with open('./wzaz259/live.txt', 'w', encoding='utf-8') as w:
        # w.write(tvlive)
        w.write("直播,#genre#\n")
        for i in range(0,len(play)):
            print(play[i]["username"]+','+play[i]["hlsPlaylist"].replace("_240p", ""))
            w.write(play[i]["username"]+','+play[i]["hlsPlaylist"].replace("_240p", "")+'\n')           
with open('./wzaz259/playlist.m3u', 'w', encoding='utf-8') as w:
        w.write('#EXTM3U\n')
        for i in range(0,len(play)):
            w.write('#EXTINF:-1 tvg-name="'+play[i]["username"]+'" tvg-logo="https://img.strpst.com/thumbs/'+str(time_stamp)+'/'+str(play[i]["id"])+'_webp" group-title="'+str_date+'" ,'+play[i]["username"]+'\n')            
            w.write(play[i]["hlsPlaylist"].replace("_240p", "")+'\n')                   
# with open('./wzaz259/playlist2.txt', 'w', encoding='utf-8') as w:
#         for i in range(0,len(play)):
#             w.write(play[i]["username"]+','+play[i]["hlsPlaylist"].replace("_240p", "")+'#')
#             w.write(play[i]["hlsPlaylist"].replace("_240p", "_1080p")+'#')
#             w.write(play[i]["hlsPlaylist"].replace("_240p", "_720p")+'#')
#             w.write(play[i]["hlsPlaylist"].replace("_240p", "_480p")+'#')
#             w.write(play[i]["hlsPlaylist"].replace("_240p", "_240p")+'#')
#             w.write(play[i]["hlsPlaylist"].replace("_240p", "_160p")+'\n')            
print("succeed")
