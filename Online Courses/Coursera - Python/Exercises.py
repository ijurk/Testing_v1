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

