#Tuple is same as list, but can't be modified
#You can't use methods like append, extend, insert, remove, clear

#important thing in Tuple when you declare a Tuple with single value, you must use comma at end else will be treated as String ex: below
tup=(10,)

#We can do indexing n repetation same as list
tup=(1,'a',440,1)
print(tup[2])
print(tup*2)

print(tup.count(1)) #how many time that value exist
print(tup.index(440)) #to get position/index of a value

#you can use methods which won't modify tuple

#convert list to tuple
lst=[1,2,3]
print(tuple(lst))