#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 12:47:13 2019
@author: aswin
"""

import requests
import json, sys, os, shutil, random
from datetime import date
sys.path.append('../')

api_key = "516be3b1d635419c4311a63155e844be"



def get_requestURL(user_id,endpoint="getList"):
    user_id = user_id.replace("@","%40")
    url_upto_apikey = ("https://api.flickr.com/services/rest/?method=flickr.photosets." + 
                       endpoint + 
                       "&api_key=" +  api_key + 
                       "&user_id=" +  user_id + 
                       "&format=json&nojsoncallback=1")
    return(url_upto_apikey)

user_id = "53690459@N04"
url = get_requestURL(user_id,endpoint="getList") 
strlist = requests.get(url).content
json_data = json.loads(strlist)
albums = json_data["photosets"]["photoset"]

print("{} albums found for user_id={}".format(len(albums),user_id))

photosetids, titles, date_mod = [], [], []
for album in albums:
    print("___")
    print("album title={} photoset_id={} date_mod={}".format(album['title']['_content'],album["id"],album["date_update"]))
    photosetids.append(album["id"])
    titles.append(album['title']['_content'])
    date_mod.append(album["date_update"])

zipped = zip(photosetids, date_mod, titles) 
# Converting to list z
zipped = list(zipped) 
# Using sorted and lambda 
res = sorted(zipped, key = lambda x: x[1]) 
photosetids = list(zip(*res)) [0]
titles = list(zip(*res)) [2]
      

def get_photo_url(farmId,serverId,Id,secret,title):
    
    image_url = ("https://farm" + str(farmId) + 
            ".staticflickr.com/" + serverId + 
            "/" + Id + '_' + secret + "_b.jpg")
    
    #hugo_synt = ("{{< photo full=\""+ image_url + "\" thumb=\""+ image_url + "\" alt=\"\" phototitle=\"" + title +"\" description=\"\">}}")
    hugo_synt = ("<br /> {{< figure src=\""+ image_url + "\">}}")
    return (hugo_synt)

URLs = {} 
for photoset_id, title in zip(photosetids,titles): ## for each album
    url = get_requestURL(user_id,endpoint="getPhotos") + "&photoset_id=" + photoset_id
#    print (url)
    strlist = requests.get(url).content
    json1_data = json.loads(strlist)
    
    urls = []
    for pic in json1_data["photoset"]["photo"]: ## for each picture in an album
        urls.append(get_photo_url(pic["farm"],pic['server'], pic["id"], pic["secret"], pic["title"]))
    URLs[photoset_id] = urls
        
    
#from IPython.display import Image, display
    
# Creating a content to store output. Contents will be deleted every time. 
out_dir = "./content"
if os.path.isdir(out_dir):
   shutil.rmtree(out_dir)
os.makedirs(out_dir)
os.chdir('./content')    
 
count = 1
for i, (photoset_id, urls) in enumerate(URLs.items()):
    print("______________________")
    print("{}, photoset_id={}".format(titles[i],photoset_id))
    
    # Creating a Sub-Folder 
    try:
        os.makedirs(titles[i])
    except OSError:
        print ("Directory Existing %s" %titles[i])
    else:  
        print ("Created directory %s" %titles[i])

    #Lets find Thumb Image
    identifier = "TH" 
    flag=0
    
    for url in urls:
        thumb = random.choice(urls)
        thumb = thumb.split("\"")[1]
        if identifier in url:
            thumb = url.split("\"")[1]
#            print("found %s \n" %thumb)
            break
           
    
    f= open("./%s/_index.md" %titles[i],"w+")
    f.write ("+++ \n")
    f.write ("albumthumb = \"%s\"\n" %thumb)
    f.write ("date = \"2016-04-21T19:12:%02d+00:00\"\n" %count)
    f.write ("title = \"%s\"\n\n" %titles[i])
    f.write ("+++ \n\n")
    
    for url in urls:
#        print(url)
#        print()
        f.write(url)
        f.write("\n")
        
    f.close()
#        display(Image(url= url, width=200, height=200))
    count += 1
    if count > 100:
        break
print("Yay! All tasks done!")