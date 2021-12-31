#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 12:47:13 2019
@author: aswin
"""

import requests
import json, sys, os, shutil, random
from datetime import date
import logging

#Set Logger Object
logger = logging.getLogger('FLICKR')
logging.basicConfig(level=logging.INFO)

sys.path.append('../')
#Set Credentials: 
user_id = "53690459@N04"
api_key = "516be3b1d635419c4311a63155e844be"

#Lets find Thumb Image
identifier = "TH" 

#Set Directory Paths: 
env_top_dir = 'TOP_DIR'
out_dir = os.environ[env_top_dir]+"/scripts/output/"
if env_top_dir in os.environ:
    logger.info(f'{env_top_dir} is {os.environ[env_top_dir]}')
else:
    logger.error(f'{env_top_dir} is not set! Source SourceMe.csh file at root of repository!')
    sys.exit(1)

def get_requestURL(user_id,endpoint="getList"):
    user_id = user_id.replace("@","%40")
    url_upto_apikey = ("https://api.flickr.com/services/rest/?method=flickr.photosets." + 
                       endpoint + 
                       "&api_key=" +  api_key + 
                       "&user_id=" +  user_id + 
                       "&format=json&nojsoncallback=1")
    return(url_upto_apikey)

def get_photo_url(farmId,serverId,Id,secret,title):    
    image_url = ("https://farm" + str(farmId) + 
            ".staticflickr.com/" + serverId + 
            "/" + Id + '_' + secret + "_b.jpg")
    #hugo_synt = ("{{< photo full=\""+ image_url + "\" thumb=\""+ image_url + "\" alt=\"\" phototitle=\"" + title +"\" description=\"\">}}")
    hugo_synt = ("<br /> {{< figure src=\""+ image_url + "\">}}")
    return (hugo_synt)

url = get_requestURL(user_id,endpoint="getList") 
strlist = requests.get(url).content
json_data = json.loads(strlist)
albums = json_data["photosets"]["photoset"]
photosetids, titles, date_mod = [], [], []
URLs = {} 

logger.info("{} albums found for user_id={}".format(len(albums),user_id))

for album in albums:
    logger.debug("___")
    logger.debug("album title={} photoset_id={} date_mod={}".format(album['title']['_content'],album["id"],album["date_update"]))
    photosetids.append(album["id"])
    titles.append(album['title']['_content'])
    date_mod.append(album["date_update"])
zipped = zip(photosetids, date_mod, titles) 
zipped = list(zipped) # Converting to list z 
res = sorted(zipped, key = lambda x: x[1]) # Using sorted and lambda 
photosetids = list(zip(*res)) [0]
titles = list(zip(*res)) [2]
thumbnail=[]

for photoset_id, title in zip(photosetids,titles): ## for each album
    url = get_requestURL(user_id,endpoint="getPhotos") + "&photoset_id=" + photoset_id
    strlist = requests.get(url).content
    json1_data = json.loads(strlist)
    urls = []
    thumb_tmp=""
    for pic in json1_data["photoset"]["photo"]: ## for each picture in an album
        urls.append(get_photo_url(pic["farm"],pic['server'], pic["id"], pic["secret"], pic["title"]))
        #lets find the TH Title
        if identifier in pic["title"]:
            thumb_tmp = get_photo_url(pic["farm"],pic['server'], pic["id"], pic["secret"], pic["title"])
            thumb_tmp = (thumb_tmp.split("\"")[1])
    URLs[photoset_id] = urls
    thumbnail.append(thumb_tmp)
    
            
# Creating a content to store output. Contents will be deleted every time. 
if os.path.isdir(out_dir):
   shutil.rmtree(out_dir)
os.makedirs(out_dir)
os.chdir(out_dir)    
 
count = 1
for i, (photoset_id, urls) in enumerate(URLs.items()):
    logger.debug("______________________")
    logger.debug("{}, photoset_id={}".format(titles[i],photoset_id))
    
    # # Creating a Sub-Folder 
    # try:
    #     os.makedirs(titles[i])
    # except OSError:
    #     logger.debug("Directory Existing %s" %titles[i])
    # else:  
    #     logger.debug("Created directory %s" %titles[i])
    
    # for url in urls:
    #     thumb = random.choice(urls)
    #     thumb = thumb.split("\"")[1]
    #     if identifier in url:
    #         thumb = url.split("\"")[1]
    #         print("FoundFoundFound Found %s \n" %thumb)
    #         break

    thumb = thumbnail[i]
    title_lower = titles[i].lower()
    md_file_name = title_lower.replace(" ","-")
    print(md_file_name)
    
    #f= open("./%s/_index.md" %titles[i],"w+")
    f= open(f"./{md_file_name}.md","w+")
    f.write ("---\n")
    f.write ("title: \"%s\"\n" %titles[i])
    f.write ("date: 2020-04-21T19:12:%02d+00:00 #TODO\n" %count)
    #f.write ("description: Noting here yet! Just a Container #TODO\n")
    

    #Hero cannot be a URL - as it is not supported. 
    f.write ("#hero: %s\n" %thumb)
    url2download = thumb
    output_filename = os.environ[env_top_dir]+ f"/scripts/images/{md_file_name}.png"
    thumb_url = f"/images/sections/posts/{md_file_name}.png"
    os.system(f"curl -o {output_filename} {thumb}")
    f.write ("hero: %s\n" %thumb_url)
    
    f.write ("author:\n  name: Aswin Natesh\n  image: /images/author/aswinnateshv21.png\n")
    f.write ("\n")
    f.write ("\nmenu:")
    f.write ("\n  sidebar:")
    f.write ("\n    name: %s" %titles[i])
    f.write ("\n    #identifier: my-travel")
    f.write ("\n    parent: california-through-my-lens #TODO")
    f.write ("\n    #weight: 1")

    f.write ("\n\n---\n")
    
    for url in urls:
        f.write(url)
        f.write("\n")
    f.close()
#   display(Image(url= url, width=200, height=200))
    count += 1
    if count > 100:
        break
logger.info("Yay! All tasks done!")