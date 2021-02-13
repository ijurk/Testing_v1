# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 11:51:38 2020

@author: ijurkovic
"""

name = "Iva"

greeting = "Hello, {}"

with_name = greeting.format(name)

print( f"Hello, {name}")

longer_phrase = "Hello, {}. Today is {}."

formatted = longer_phrase.format("Iva","Friday")

print(formatted)


name = input("Enter your name: ")
print(name)


size_input = input("How big is your house (in sq feet): ")
sq_feet = int(size_input)

sq_meters = sq_feet / 10.8

print(f"{sq_feet} sq feet is {sq_meters:.2f} sq meters")


user_age = int(input("Enter your age: "))
months = user_age * 12
print(f"Your age, {user_age} is equal to {months} months")


day_of_week = input("what day of teh week is it today?").lower()

# =============================================================================
# List, Tuplets, sets
# =============================================================================


l = ["Iva","Juan","Max"] #mutable, keeps order, add and remove
t = ("Iva","Juan","Max") #notmutable, keeps order
s = {"Iva","Iva", "Juan","Max"} #removes duplicate, does not keep order, add and remove

l[0]
t[0]

l[0] = "John"

l.append("Iva")
s.add("Smith")

grades = [3,5,7,8]

total = sum(grades)
amount = len(grades)

print(total/amount)


# =============================================================================
# Set Operations
# =============================================================================


friends = {"Bob","Rolf","Anne"}
abroad = {"Bob","Anne"}

local = friends.difference(abroad)
print(local_friends)

s = set() #empty set

friends = local.union(abroad)
friends

art = {"Bob","Jen","Rolf","Charlie"}
science = {"Bob","Jen","Adam", "Anne"}


both = art.intersection(science)
both


# =============================================================================
# Booleans
# =============================================================================


5 == 5
5 > 5
10 != 10

#Comparisons: ==,!=, <, >, >=, <=

friends = ["Rolf","Bob"]
abroad = ["Rolf","Bob"]

print(friends == abroad)
print(friends is abroad) 

abroad = friends
print(friends is abroad)

# =============================================================================
# in key word
# =============================================================================


friends = ["Bob","Rolf","Jen"]

print("Jen" in friends)


number = (7,5)

user_input = input("Enter 'y' if you would like to play: ").lower()

if user_input == "y":
    user_num = int(input("Guess our number: "))
    if user_num in number:
        print("Correct!")
    elif abs(number - user_num) == 1:
        print("You are off by 1")
    else:
        print("Sorry, wrong!")

# =============================================================================
# Loops in Python
# =============================================================================




while True:
    user_input = input("Would you like to play? (Y/n) ").lower()
    
    if user_input == 'n':
        break
    
    user_num = int(input("Guess our number: "))
    if user_num in number:
        print("Correct!")
    elif abs(number - user_num) == 1:
        print("You are off by 1")
    else:
        print("Sorry, wrong!")




friends = ["Bob","Rolf","Jen"]

for friend in friends:
    print(f"{friend} is my friend")
    
    
    
# =============================================================================
# List comprehantion
# =============================================================================


numbers = [1,3,5]
doubled = [num * 2 for num in numbers]

friends = ["Sam","Samantha","Bob","Rolf","Jen"]
start_s = [friend for friend in friends if friend.startswith("S")] 
        
print(start_s)


# =============================================================================
# Dictionaries
# =============================================================================

friend_age = {'Juan': 38, 'Iva': 25}


friend_age['Iva'] #access
friend_age['Ian'] = 55 #add
friend_age['Juan'] = 35 #change
friend_age


#list of dictionaries

friends = [
    {'name': 'Iva', 'age': 25},
    {'name': 'Juan', 'age': 35},
    {'name': 'Ian', 'age': 55},
    ]


friends
friends[0]['name']


for friend in friend_age:
    print(f'{friend} is {friend_age[friend]} years old')
    
 

for friend, age in friend_age.items():
    print(f'{friend} is {age} years old')
    
    
if 'Iva' in friend_age:
    print(f"{friend_age['Iva']} years old")
    
    
#get the values only

age = friend_age.values()

avg_age = sum(age)/len(age)
avg_age    


student_at = {'Iva' : 96, 'Juan': 80, 'Anne': 100}

for student, atten in student_at.items():
    print(f"{student}: {atten}")

print(list(student_at.items()))


person = ('Bob',42,'Mechanic')

name, _, profession = person

name
_
profession


head, *tail = [1,2,3,4,5]
head
tail
*head, tail = [1,2,3,4,5]

# =============================================================================
# Functions
# =============================================================================


def user_age_in_sec():
    user_age = int(input("enter your age in years: "))
    age_seconds = user_age * 365 *24*60*60
    print(f"Your age in seconds is {age_seconds}.")
    

user_age_in_sec()


def add(x,y):
    pass #do nothing 
    

# =============================================================================
# default parameters in functions
# =============================================================================


def add_two(x,y=8):
    print(x+y)

add_two(5)
add_two(6,4)



default_y = 3

def add_two_two(x, y=default_y):
    print(x+y)
    
add_two_two(5)

default_y = 5 #does not change the default of the add_two_two function
add_two_two(5)


# =============================================================================
# Lambda function
# =============================================================================

def add_two(x,y):
    return x+y

print(add(5,7))


add = lambda x,y: x+y
print(add(5,7))


def double(x):
    return x*2

sequence = [1,3,5,9]
doubled = [double(x) for x in sequence]
doubled 

doubled = list(map(double,sequence)) #map returns map object
doubled

doubled = [(lambda x: x*2)(x) for x in sequence]
doubled

doubled = list(map(lambda x: x*2,sequence))
doubled


# =============================================================================
# Dictionaries comprehantion
# =============================================================================

#list of tuplets 
users = [
        (0, 'Iva', 'pass'),
        (1, 'Juan','test'),
        (2, 'Max', 'passw')
        ]

#creating a dictionary
username_mapping = {user[1]: user for user in users}

username_input = input("enter your username: ")
password_input = input("enter your password: ")

_, username, password = username_mapping[username_input]

if password_input == password:
    print("successful login")
else:
    print("incorect username or/and password")



# =============================================================================
# Unpacking Arguments
# =============================================================================

#creates a tuplet - args is a tuplet 
def multiply(*args):
    print(args)
    total = 1
    for arg in args:
        total = total * arg
    return total
    
    
    
print(multiply(1,3,5))
    

def add(x, y):
    return x + y

nums = [3,5]
add(*nums) #deconstructing the variable into single values


def add(x, y, z):
    return x + y + z

nums = {"x": 3, "y": 5, "z": 2}
print(add(**nums))


def apply(*args, operator): #operator is a compulsory or required named argument
    if operator == "*":
        return multiply(*args)
    elif operator == "+":
        return sum(args)
    else:
        return "No valid operator provided to apply()"
    


print(apply(1,3,6,7, operator = "*"))


# =============================================================================
# Unpacking keyword arguments
# =============================================================================

#collects keyword arguments - outputs/creates a dictionary, 
#collecting named arguments into a dictionary
def named(**kwargs): #pack into dictionary 
    print(kwargs)
    
named(name='Iva', age=25)


def named(name,age):
    print(name,age)
    
details = {'name': 'Iva', 'age': 25}


named(**details) #unpacks the dictionary into single values

def print_nicely(**kwargs):
    named(**kwargs)
    for arg, value in kwargs.items():
        print(f"{arg}: {value}")

print_nicely(name='Iva', age=25)

def both(*args, **kwargs):
    print(args)
    print(kwargs)

both(1,2,3,4, name="Iva", age = 25)

#used when we don't know how many arguments will pass to the function

def post(url, data=None, json=None, **kwargs):
    return request('post', url, data=data, json=json, **kwargs)

# =============================================================================
# Object oriented programming
# =============================================================================


student = {'name': 'Iva', 'grades': (89,90,93,78,90)}

def average(sequence):
    return sum(sequence) / len(sequence)


print(average(student['grades']))

#rewritten as object oriented prog
class Student:
    def __init__(self):
        self.name = 'Iva'
        self.grades = (89,90,93,78,90)
        
    def average(self):
        return sum(self.grades) / len(self.grades)
        
        
student = Student()
print(Student.average(student))
print(student.average())
print(student.name)
print(student.grades)


#all methods inside a class need to have a parameter

class Student:
    def __init__(self,name, grades):
        self.name = name
        self.grades = grades
        
    def average(self):
        return sum(self.grades) / len(self.grades)
        
student = Student('Juan', (89,90,93,78,95))
print(student.average())
print(student.name)


# =============================================================================
# Magic methods _str_ and _repr_ - used for representing an object and recreating it 
# =============================================================================

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def __str__(self):
        return f"{self.name} is {self.age} years old."
    
    def __repr__(self):
        return f"<Person('{self.name}', {self.age})>"
        
bob = Person('Bob', 35)
print(bob)

# =============================================================================
# @classmethod and @ststicmethod
# =============================================================================
# =============================================================================
# instance_method - is used when you want to produce an action that uses the data inside the object
# created on initalization
# class method - is like a factory
# static method - used to place a method inside a class because it belongs there 
# =============================================================================

class ClassTest:
    def instance_method(self):
        print(f"Called instance_method of {self}")
    
    @classmethod
    def class_method(cls):
        print(f"Called class_method of {cls}")
        
    @staticmethod
    def static_method(): #seperate function that lives inside the class
        print("Called static method.")


test = ClassTest()
test.instance_method()
ClassTest.instance_method(test)


ClassTest.class_method()
ClassTest.static_method()


class Book:
    types = ('hardcover','paperback')
    
    def __init__(self, name, book_type, weight):
        self.name = name
        self.book_type = book_type
        self.weight = weight
        
        
    def __repr__(self):
        return f"<Book {self.name}, {self.book_type}, weighing {self.weight}g>"
    
    @classmethod
    def hardcover(cls, name, page_weight):
        return Book(name, Book.types[0], page_weight + 100)
    
    @classmethod
    def paperback(cls, name, page_weight):
        return Book(name, Book.types[1], page_weight)

print(Book.types)


book = Book('Harry Potter', 'hardcover', 1500)
print(book.name)
print(book.book_type)
print(book)

light = Book.paperback('Python 101', 600)
book = Book.hardcover('Harry Potter', 1500)
print(book)
print(light)

# =============================================================================
# Class Inheritance
# =============================================================================


class Device:
    def __init__(self, name, connected_by):
        self.name = name
        self.connected_by = connected_by
        self.connected = True
        
    def __str__(self):
        return(f"Device {self.name!r} ({self.connected_by})") #!r calls repr method od self.name and adds quotes
    
    def disconnect(self):
        self.connected = False
        print("Disconnected.")
        
printer = Device("Printer","USB")

print(printer.name) #Printer
print(printer.connected) #True
print(printer.connected_by) #USB
print(printer) #Device 'Printer' (USB)

printer.disconnect()
print(printer.connected)



class Printer(Device):
    def __init__(self, name, connected_by, capacity):
        super().__init__(name, connected_by) #call parent class Device init method, super class 
        self.capacity = capacity
        self.remaining_pages = capacity
        
    def __str__(self):
        return f"{super().__str__()} ({self.remaining_pages} pages remaining)"
    
    def print(self, pages):
        if not self.connected:
            print("Your printer is not connected")
            return 
        print(f"Printing {pages} pages. ")
        self.remaining_pages -= pages


printer = Printer("Printer", "USB", 500)
printer.print(20)
print(printer)
print(printer)


printer.disconnect()
printer.print(30)


# =============================================================================
# Class composition
# =============================================================================

class BookShelf:
    def __init__(self, *books):
        self.books = books
        
    def __str__(self):
        return f"Bookshelf with {len(self.books)} books."
      


class Book:
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return f"Book {self.name}"


book = Book("Harry Potter")
book2 = Book("Python 101")
shelf = BookShelf(book, book2)
print(shelf)
print(shelf.books)


# =============================================================================
# Type hiniting
# =============================================================================

def list_avg(sequence: list) -> float: #define it takes in a list and returns a float
    return sum(sequence)/len(sequence)


list_avg(123)


# =============================================================================
# Imports 
# =============================================================================

from mymodule import divide

print(divide(6,2))


import sys

print(sys.path)

import mymodule


# =============================================================================
# Errors
# =============================================================================

def divide(dividend, divisor):
    if divisor == 0:
        raise ZeroDivisionError("Divisor cannot be 0.")
        
    return dividend/divisor


grades = [2,5]

print("Welcome to the average grade program.")
try:
    average = divide(sum(grades),len(grades))
except ZeroDivisionError as e:
    print(e)
    print("There are no grades yet in your list.")  
except ValueError:
    print("Another error.")
else:
    print(f"The average grade is {average}")
finally:
    print("Thank you!")



students = [
    {"name": "Iva", "grades": [2,5,4]},
    {"name": "Bob", "grades": []},
    {"name": "Juan", "grades": [5,6,7]},
    ]


try:
    for student in students:
        name = student["name"]
        grades = student['grades']
        average = divide(sum(grades), len(grades))
        print(f"{name} average grade is {average}")
except ZeroDivisionError as e:
    print(f"ERROR: {name} has no grades yet.")
    print(e)
else:
    print("-- All student averages calculated --")
finally:
    print("-- End of student average calculation --")
    