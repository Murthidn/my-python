dict={1:'ab',2:'cd',3:'xy'}

print(dict) #returns as it is

print(dict.items()) #returns in set

k=dict.keys()
for i in k:print(i) #need to loop as it returns in set

v=dict.values()
for i in v:print(i)

print(dict[2])

del dict[2]
print(dict)

#Important things
#Strings methods returns new string on modification but list, tuple, set, dict modifies n returns same obj