import requests
from bs4 import BeautifulSoup
import re
import urllib
import sys

downloadpath = sys.argv[1]

#specify the url
weblink = "http://getcomics.info/?s=the+walking+dead"
webpage = requests.get(weblink)
# webpage.content

list = []
downloadurl = ""
soup = BeautifulSoup(webpage.content,'html.parser')
# print(soup.prettify().encode("utf-8"))
# soup.find_all(class_ = "post-header-image")
for link in soup.findAll('a', attrs={'href': re.compile("^http://getcomics.info/other-comics/")}):
   list.append(link.get('href'))


weblink2 = list[0].encode("UTF-8")
webpage2 = requests.get(weblink2)
webpage2.content

link = list[0].encode("UTF-8").split("/")
for items in link:
    if items == "":
       link.remove(items)

filename = link[-1]

soup2 = BeautifulSoup(webpage2.content,'html.parser')

for link in soup2.findAll('a', attrs={'href': re.compile("^http://"),'title' : re.compile("Download Now")}):
    downloadurl = link.get('href')

#Can be done using requests but urllib is one liner
urllib.urlretrieve(downloadurl,"{0}/{1}.cbr".format(downloadpath, filename))

#Upload downloaded file to gdrive comics folder using google drive api and pydrive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

file = drive.CreateFile({'title':'{0}.cbr'.format(filename), 'mimeType':'application/cbr',
        "parents": [{"id": "<Your folder id goes here>"}]})

file.SetContentFile("{0}/{1}.cbr".format(downloadpath, filename))
file.Upload()

print('Uploaded file %s with mimeType %s' % (file['title'],
file2['mimeType']))
# Created file hello.png with mimeType image/png

