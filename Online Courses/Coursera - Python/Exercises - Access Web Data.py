# -*- coding: utf-8 -*-
"""
Created on Wed May 13 21:31:13 2020

@author: ijurkovic
"""

# -*- coding: utf-8 -*-
"""
Created on Sat May  9 21:26:30 2020

@author: ijurkovic
"""
"""
tuples
- cannot be changed
- dir(tuple) - count and index
- can be compared
- itmes() method returns tuples 
"""

d = dict()
for (k,v) in d.items():
    print(k,v)
    
    
d = {'a' :10,'b' : 1,'c': 22}
d.items()
sorted(d.items())

#sort by key
for k,v in sorted(d.items()):
    print(k,v)


#sort by value
tmp = list() #list of tuples
for k,v c.items():
    tmp.append((v,k))
    
tm = sorted(tmp, reverse=True)

##get top 10 most common words
fhand = open('romeo.txt')
counts = dict()
for line in fhand:
    words = line.split()
    for word in words:
        counts[word] = counts.get(word,0) + 1
        
lst = list()
for key, val in counts.items():
    newtup = (val, key)
    lst.append(newtup)
    
    
lst = sorted(lst, reverse=True)

for val, key in lst[:10] :
    print(key, val)
    
##line 44 through 53 done in one line - LIST COMPREHENSION
c = {'a' :10,'b' : 1,'c': 22}
print(sorted([(v,k) for k,v in c.items()]))
"""
9.4 Write a program to read through the mbox-short.txt and figure out who has sent 
the greatest number of mail messages. The program looks for 'From ' lines and 
takes the second word of those lines as the person who sent the mail. The program 
creates a Python dictionary that maps the sender's mail address to a count of the 
number of times they appear in the file. After the dictionary is produced, the 
program reads through the dictionary using a maximum loop to find the most prolific 
committer.
"""

name = input("Enter file:")
if len(name) < 1 : name = "mbox-short.txt"
fh = open(name)
senders = dict()

for line in fh:
    if not line.startswith('From '): continue
    words = line.split()
    senders[words[1]] = senders.get(words[1],0) + 1
        
bigsender = None
bigcount = None

for sender,count in senders.items():
    if bigcount is None or count > bigcount:
        bigsender = sender
        bigcount = count

print(bigsender,bigcount)

"""
10.2 Write a program to read through the mbox-short.txt and figure out 
the distribution by hour of the day for each of the messages. 
You can pull the hour out from the 'From ' line by finding the time and 
then splitting the string a second time using a colon.
From stephen.marquard@uct.ac.za Sat Jan  5 09:14:16 2008
Once you have accumulated the counts for each hour, print out the counts, 
sorted by hour as shown below.
"""

name = input("Enter file:")
if len(name) < 1 : name = "mbox-short.txt"
handle = open(name)

hours = dict()

for line in handle:
    if not line.startswith('From '): continue
    words = line.split()
    hour = words[5]
    hour = hour.split(':')
    hours[hour[0]] = hours.get(hour[0],0) + 1
    
 
tlist = sorted([(k,v) for k,v in hours.items()])

for k,v in tlist:
    print(k,v)

"""
8.5 Open the file mbox-short.txt and read it line by line. When you 
find a line that starts with 'From ' like the following line:
From stephen.marquard@uct.ac.za Sat Jan  5 09:14:16 2008
You will parse the From line using split() and print out the second 
word in the line (i.e. the entire address of the person who sent the message). 
Then print out a count at the end.
Hint: make sure not to include the lines that start with 'From:'.

You can download the sample data at http://www.py4e.com/code3/mbox-short.txt
"""

fname = input("Enter file name: ")
if len(fname) < 1 : fname = "mbox-short.txt"
fh = open(fname)
count = 0

for line in fh:
    if not line.startswith('From '): continue
    words = line.split()
    print(words[1])
    count = count + 1

print("There were", count, "lines in the file with From as the first word")


#######################################
############Regular Expresion##########
#######################################


## re.search() - returns true/false
## re.findall() - extracting the matching string - list of strings

"""
* zero or more
. any
^ beg of line
\s non white space character
[0-9] - one character
[0-9.] decimal numbers
+ one or more
[^ ] give me everything not white space -- [^] not
"""
import os
import re

parent_dir = 'C:\\Users\\ijurkovic\\Desktop\\Coursera - Python'

os.chdir(parent_dir)
os.getcwd()

fn = input("Enter file name:")
fh = open(fn)
numlist = list()
for line in fh:
    line = line.rstrip()
    numbers = re.findall('[0-9]+',line)
    if len(numbers) == 0: continue
    numlist = numlist + numbers
  
total = 0    
for i in range(len(numlist)):
    num = float(numlist[i])
    total = total + num

print(total)   



############################################
#############Sockets########################
############################################


import socket

mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mysock.connect(('data.pr4e.org', 80))
cmd = 'GET http://data.pr4e.org/intro-short.txt HTTP/1.0\r\n\r\n'.encode()
mysock.send(cmd)

while True:
    data = mysock.recv(512)
    if len(data) < 1:
        break
    print(data.decode(),end='')

mysock.close()


############################################
#############Retriving Web Pages############
############################################

import urllib.request, urllib.parse, urllib.error

fhand = urllib.request.urlopen('http://data.pr4e.org/romeo.txt')
for line in fhand:
    print(line.decode().strip())


fhand = urllib.request.urlopen('http://data.pr4e.org/romeo.txt')

counts = dict()
for line in fhand:
    words = line.decode().split()
    for word in words:
        counts[word] = counts.get(word, 0) + 1
print(counts)

####Parsing Web Page


from bs4 import BeautifulSoup

url = input('Enter - ')
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html,'html.parser')

# Retrive all of the anchor tags
tags = soup('a')
for tag in tags:
    print(tag.get('href',None))
    


import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter - ')
html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

# Retrieve all of the anchor tags
tags = soup('a')
for tag in tags:
    print(tag.get('href', None))
    
    
    
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter - ')
html = urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, "html.parser")

# Retrieve all of the anchor tags
tags = soup('span')

total = 0

for tag in tags:
    # Look at the parts of a tag
    total = total + float(tag.contents[0])

print(total)




import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter URL - ')
cnt = input('Enter count - ')
cnt = float(cnt)
pos = input('Enter position - ')
pos = float(pos)
cnt = cnt + 1

while cnt > 0:
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    print('Retriving: ', url)
    tags = soup('a')
    pos_cnt = 0
    
    for tag in tags:
        pos_cnt = pos_cnt + 1
        if pos_cnt < pos : continue
        if pos_cnt == pos:
            url = tag.get('href', None)
            cnt = cnt - 1
            break
            
 ####Parsing XML
 
 import xml.etree.ElementTree as ET
 
data = '''
<person>
  <name>Chuck</name>
  <phone type="intl">
    +1 734 303 4456
  </phone>
  <email hide="yes" />
</person>''' #xml string
 
 tree = ET.formstring(data)
 print('Name:', tree.find('name').text)
 print('Attr:',tree.find('email').get('hide'))
 
 
 
 input_d = input = '''
<stuff>
  <users>
    <user x="2">
      <id>001</id>
      <name>Chuck</name>
    </user>
    <user x="7">
      <id>009</id>
      <name>Brent</name>
    </user>
  </users>
</stuff>'''##multi child nodes
 
 stuff = ET.formstring(input_d)
 lst = stuff.findall('users/user')
 print('User count:',len(lst))
 for item in lst:
     print('Name',item.find('name').text)
     print('Id', item.find('id').text)
     print('Attribute', item.get('x'))
     
     
     
     
import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET


while True:
    url = input('Enter location: ')
    if len(url) < 1: break

    
    print('Retrieving', url)
    uh = urllib.request.urlopen(url, context=ctx)

    data = uh.read()
    print('Retrieved', len(data), 'characters')
    tree = ET.fromstring(data)

    results = tree.findall('comments/comment')
    print('Count:',len(results))
    total = 0 
    for result in results:
        num = result.find('count').text
        total = total + float(num)
    print('Sum:', total)

  
###or instead of comments/comment you use .//count to directly access count

import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET


while True:
    url = input('Enter location: ')
    if len(url) < 1: break

    
    print('Retrieving', url)
    uh = urllib.request.urlopen(url, context=ctx)

    data = uh.read()
    print('Retrieved', len(data), 'characters')
    tree = ET.fromstring(data)

    results = tree.findall('.//count')
    print('Count:',len(results))
    total = 0
    for result in results:
        num = result.text
        total = total + float(num)
    print('Sum:', total)
        
    
 ####Parsing JSON
 
import json

data = '''
{
  "name" : "Chuck",
  "phone" : {
    "type" : "intl",
    "number" : "+1 734 303 4456"
   },
   "email" : {
     "hide" : "yes"
   }
}'''

info = json.loads(data)
print('Name:', info["name"])
print('Hide:', info["email"]["hide"])


import json

data = '''
[
  { "id" : "001",
    "x" : "2",
    "name" : "Chuck"
  } ,
  { "id" : "009",
    "x" : "7",
    "name" : "Brent"
  }
]'''

info = json.loads(data)
print('User count:', len(info))
for item in info:
    print('Name:', item['name'])
    print('Id:', item['id'])
    print('Attr:', item['x'])

 

import urllib.request, urllib.parse, urllib.error
import json

while True:
    url = input('Enter location: ')
    if len(url) < 1: break

    
    print('Retrieving', url)
    uh = urllib.request.urlopen(url, context=ctx)

    data = uh.read().decode()
    print('Retrieved', len(data), 'characters')
    info = json.loads(data)
    info = info['comments']
    print('Count:',len(info))
    total = 0
    for item in info:
        num = item['count']
        total = total + float(num)
    print('Sum:', total)



import urllib.request, urllib.parse, urllib.error
import json

serviceurl = 'http://maps.googleapis.com/maps/api/geocode/json?'

while True:
    address = input('Enter location: ')
    if len(address) < 1: break
    
    url = serviceurl + urllib.parse.urlencode({'address' : address})
    
    print('Retriving', url)
    uh = urllib.request.urlopen(url)
    data = uh.read().decode()
    print('Retrived', len(data), 'character')
    
    try:
        js = json.loads(data)
    except:
        js = None
        
    if not js or 'status' not in js or js['status'] != 'OK':
        print('========= Failur to retrive ========')
        print(data)
        continue
    
print(json.dumps(js, indent=4))  
    
lat = js['results'][0]['geometry']['location']['lat']
lng = js['results'][0]['geometry']['location']['lng']

print('lat', lat, 'lng', lng)
location = js['results'][0]['formatted_address']
print(location)


##geo json code

import urllib.request, urllib.parse, urllib.error
import json
import ssl

api_key = False
# If you have a Google Places API key, enter it here
# api_key = 'AIzaSy___IDByT70'
# https://developers.google.com/maps/documentation/geocoding/intro

if api_key is False:
    api_key = 42
    serviceurl = 'http://py4e-data.dr-chuck.net/json?'
else :
    serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json?'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

while True:
    address = input('Enter location: ')
    if len(address) < 1: break

    parms = dict()
    parms['address'] = address
    if api_key is not False: parms['key'] = api_key
    url = serviceurl + urllib.parse.urlencode(parms)

    print('Retrieving', url)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters')

    try:
        js = json.loads(data)
    except:
        js = None

    if not js or 'status' not in js or js['status'] != 'OK':
        print('==== Failure To Retrieve ====')
        print(data)
        continue

    placeid = js['results'][0]['place_id']
    print('Place id', placeid)
    
    
############################################
#############Using databases############
############################################       


import sqlite3
conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

cur.execute('''drop table if exists Counts''')

cur.execute('''create table Counts (email TEXT, count INTEGER)''')

fname = input('Enter file name: ')
if len(fname) < 1: fname = 'mbox-short.txt'
fh = open(fname)
for line in fh:
    if not line.startswith('From: '): continue
    pieces = line.split()
    email = pieces[1]
    cur.execute('select count from Counts where email = ?',(email,))
    row = cur.fetchone()
    if row is None:
        cur.execute('''insert into Counts (email, count) values(?,1)''', (email,))
    else:
        cur.execute('update Counts set count = count + 1 where email = ?',(email,))
    conn.commit()
    
sqlstr = 'select email, count from Counts order by count desc limit 10'

for row in cur.execute(sqlstr):
    print(str(row[0]),row[1])
    
cur.close()
    


import sqlite3
conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()


cur.execute('''CREATE TABLE Ages ( 
  name VARCHAR(128), 
  age INTEGER
)''')

cur.execute('''DELETE FROM Ages''')
cur.execute('''INSERT INTO Ages (name, age) VALUES ('Rio', 35)''')
cur.execute('''INSERT INTO Ages (name, age) VALUES ('Ahtasham', 31);''')
cur.execute('''INSERT INTO Ages (name, age) VALUES ('Lauren', 40);''')
cur.execute('''INSERT INTO Ages (name, age) VALUES ('Ailise', 21);''')
cur.execute('''INSERT INTO Ages (name, age) VALUES ('Alphonsina', 22);''')
cur.execute('''INSERT INTO Ages (name, age) VALUES ('Clio', 21);''')
sqlstr = 'SELECT hex(name || age) AS X FROM Ages ORDER BY X'

for row in cur.execute(sqlstr):
    print(row[0])
    






import os
import sqlite3
import urllib.request, urllib.parse, urllib.error
import re


os.getcwd()
os.chdir('C:/Users/ijurkovic/Desktop/Coursera - Python')


conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')

cur.execute('''
CREATE TABLE Counts (email TEXT, count INTEGER)''')

url = input('Enter file location: ')
fhand = urllib.request.urlopen(url)


emailcount = dict()
for line in fhand:
    line = line.decode().strip()
    if not line.startswith('From: '): continue
    pieces = line.split()
    email = pieces[1]
    org = re.findall('@(.+)[.]', email)
    org = org[0]
    emailcount[org] = emailcount.get(org, 0) + 1
    
for k,v in emailcount.items():
    cur.execute('''INSERT INTO Counts (email, count)
                VALUES (?, ?)''', (k,v))
  
                 
conn.commit()

sqlstr = 'SELECT email, count FROM Counts ORDER BY count DESC'

for row in cur.execute(sqlstr):
    print(row)

cur.close()


#### worked example tracked

import xml.etree.ElementTree as ET
import sqlite3
import os

os.getcwd()
os.chdir('C:/Users/ijurkovic/Desktop/Coursera - Python/tracks')

conn = sqlite3.connect('trackdb.sqlite')
cur = conn.cursor()

cur.executescript('''
            drop table if exists Artist;
            drop table if exists Album;
            drop table if exists Track;
            
            
            create table Artist (
                id integer not null primary key autoincrement unique,
                name text unique
            );
            
            CREATE TABLE Genre (
                id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                name    TEXT UNIQUE
            );
            
            create table Album (
                id integer not null primary key autoincrement unique,
                artist_id integer,
                title text unique
            );
            
            create table Track (
                id integer not null primary key autoincrement unique,
                title text unique,
                album_id integer,
                genre_id integer,
                len integer, rating integer, count integer
            );
            ''')
            
            
fname = input('Enter file name: ')
if len(fname) < 1 : fname = 'Library.xml'
            
def lookup(d,key):
    found = False
    for child in d:
        if found : return child.text
        if child.tag == 'key' and child.text == key :
            found = True
    return None
            
            
stuff = ET.parse(fname)
all = stuff.findall('dict/dict/dict') 
print('Dict count:', len(all))
for entry in all:
    if ( lookup(entry, 'Track ID') is None) : continue

    name = lookup(entry, 'Name')
    artist = lookup(entry, 'Artist')
    genre = lookup(entry, 'Genre')
    album = lookup(entry, 'Album')
    count = lookup(entry, 'Play Count')
    rating = lookup(entry, 'Rating')
    length = lookup(entry, 'Total Time')
    
    if name is None or artist is None or album is None or genre is None:
        continue
         
    print(name, artist,genre, album, count, rating, length)

    cur.execute('''insert or ignore into Artist (name)
                values (?)''', (artist, ))
    cur.execute('select id from Artist where name = ?', (artist,))
    artist_id = cur.fetchone()[0]
    
    cur.execute('''insert or ignore into Genre (name)
                values (?)''', (genre, ))
    cur.execute('select id from Genre where name = ?', (genre,))
    genre_id = cur.fetchone()[0]
    
    
    cur.execute('''insert or ignore into Album (title, artist_id)
                values (?, ?)''', (album, artist_id ))
    cur.execute('select id from Album where title = ?', (album,))
    album_id = cur.fetchone()[0]
            
    
    cur.execute('''insert or replace into Track (title, album_id,genre_id, len, rating, count)
                values (?, ?, ?, ?, ?, ?)''', (name, album_id, genre_id, length, rating, count ))
    
  
    conn.commit()        


sqlstr = '''SELECT Track.title, Artist.name, Album.title, Genre.name 
            FROM Track JOIN Genre JOIN Album JOIN Artist 
            ON Track.genre_id = Genre.ID and Track.album_id = Album.id 
                AND Album.artist_id = Artist.id
            ORDER BY Artist.name LIMIT 3'''
    
    
    
for row in cur.execute(sqlstr):
    print(row)

cur.close()



import json
import sqlite3
import os

os.getcwd()
os.chdir('C:/Users/ijurkovic/Desktop/Coursera - Python')
os.getcwd()


conn = sqlite3.connect('rosterdb.sqlite')
cur = conn.cursor()

# Do some setup
cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);

CREATE TABLE Course (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
)
''')

fname = input('Enter file name: ')
if len(fname) < 1:
    fname = 'roster_data.json'

# [
#   [ "Charley", "si110", 1 ],
#   [ "Mea", "si110", 0 ],

str_data = open(fname).read()
json_data = json.loads(str_data)

for entry in json_data:

    name = entry[0];
    title = entry[1];
    role = entry[2];

    print((name, title, role))

    cur.execute('''INSERT OR IGNORE INTO User (name)
        VALUES ( ? )''', ( name, ) )
    cur.execute('SELECT id FROM User WHERE name = ? ', (name, ))
    user_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Course (title)
        VALUES ( ? )''', ( title, ) )
    cur.execute('SELECT id FROM Course WHERE title = ? ', (title, ))
    course_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Member
        (user_id, course_id, role) VALUES ( ?, ?, ? )''',
        ( user_id, course_id, role ) )

    conn.commit()


sqlstr = '''SELECT hex(User.name || Course.title || Member.role ) AS X FROM 
            User JOIN Member JOIN Course 
            ON User.id = Member.user_id AND Member.course_id = Course.id
            ORDER BY X'''
            
for row in cur.execute(sqlstr):
    print(row)

cur.close()