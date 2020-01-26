lst=[1,'2',3.5] #duplicates, diffrent data types...etc

#We can perform Indexing, Slicing, Repetation on List

#Indexing - starts with 0
print(lst[3])

#Slicing - starts with 0
print((str[1:3])) #very similar to String slicing

#Repetation - same as string
print(lst*2)

#3 Important methods of list
lst.append(60)
lst.remove(3.5)
del(lst[2]) #Py function, delete by index

lst.clear() #clears everything
max(lst) #return max value in integer
min(lst) #returns min

lst.insert(2, 'murthi') #to insert at a specific index/place

lst.sort() #sort int in asc order by default
lst.sort(reverse=True) #sort by desc