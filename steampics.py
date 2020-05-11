import requests
from bs4 import BeautifulSoup as bs
import json
from PIL import Image
from io import BytesIO
import re

steamId = '76561198077968978' #'76561197987808170' #'76561198048056421' # 

steamkey = ''

#Get all steam games of usr steam id
url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=2B032F9CF0C84A982A07E363DF1B3D2A&steamid=" + steamId + "&format=json&include_appinfo=true"
html = requests.get(url).text

#find number of games for formatting
numOfGames = re.search(r'\"game_count\":(.*?),', html.__str__()).group(1)
print(numOfGames)

#Remove excess intro
html = html.replace("{\"response\":{\"game_count\":"+ numOfGames.__str__() +",\"games\":[{", "").replace("}]}}", "").replace('\'', "")

#seperate game data to array of games each game is a dictonary of datas
items = html.split('},{')
gamesOrg = []
for game in items:
    idsDict = dict()
    for ids in game.split(',\"'): 
        id = ids.split(':')
        #print(len(id))
        idName = id[0].replace("\"", "")
        idsDict.update({idName: id[1]})
    gamesOrg.append(idsDict)
         
#Prints # of games 
print(len(gamesOrg))


#soup = bs(html, 'lxml')

#Makes array of pair datatype game ids and logo url number
pictureIds = []
for dit in gamesOrg:
    #if dit.get("img_logo_url"):
        pictureIds.append((dit.get("appid"), dit.get("img_logo_url").replace("\"","")))

#http://media.steampowered.com/steamcommunity/public/images/apps/400/4184d4c0d915bd3a45210667f7b25361352acd8f.jpg

#Creates array of picture urls based around the steam community format
pictureURLs = []
for pairs in pictureIds:
    if pairs[1] != "":
        pictureURLs.append('http://media.steampowered.com/steamcommunity/public/images/apps/' + pairs[0].__str__() + '/' + pairs[1].__str__() + '.jpg')

images = []
for imgUrl in pictureURLs:
    print(imgUrl)
    response = requests.get(imgUrl)
    img = Image.open(BytesIO(response.content))
    images.append(img) 

#find image size needed based around 16/9 aspect ratio
numOfImages = len(images)
x = int((numOfImages / 144) * 4)
y = int((numOfImages / 144) * 3)
while (x*y) < numOfImages:
    if x < y:
        x = x + 1
    else:
        y = y + 1 
if x<y:
    s = y
    y = x 
    x = s 
print(x.__str__() + " : " + y.__str__())

#concatanated the pictures 
imgsWid = images[0].width
imgsHei = images[0].height
totalImage = Image.new('RGB', ( imgsWid* x, imgsHei*y))
for i in range(numOfImages):
    posY = int(i / x)
    posX = i-(posY*x)
    totalImage.paste(images[i], (posX*imgsWid, posY*imgsHei))

totalImage.show()

#Write urls to JSON file
with open('steam.json', 'w', encoding="utf-8") as outfile:
    #outfile.write(pictures.__str__())
    outfile.write(pictureURLs.__str__())

    