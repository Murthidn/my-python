#String Creation
s='You are amazing!'
print(s)

s1='''You are 
The Creator
Of your destinty'''
print(s1)

print(s[2])
print(s*2)
print(len(s))

#String Slicing - Very easy and Powerful
print(s[0:7])
print(s[0:])
print(s[:8])

print(s[-8:-1])

#Step in Slicing
print(s[0:19:2])
print(s[19:])
print(s[16::-1])
print(s[::-1])  # 3rd value is like like increment or decrement | Pointer dude +ve - Go forward, -ve come backward

#String Strip
s2='  Hey Man!  '
print(s2)
print(s2.strip()) #Skips 1st & last Spacess
print(s2.lstrip()) #left strip
print(s2.rstrip()) #right strip

print(s2.capitalize()) #makes big letters to small
print(s2.find('Man')) #To find a substring in string, gives the index from where it starts
print(s2.find('xxx')) #if value is not there, gives -1
print(s2.find('Man', 0, len(s2))) # we can specify from where to search (2nd value) and where to stop
print(s2.find('Man', 10, len(s2))) # string returns -ve value (-1) if we are accessing out of index but won't error

print(s2.count('M')) #Prints no. of occurances of given sub string
print(s2.replace('Man', 'Buddy')) #replaces given substring

s3='Hello Murthi dN'
print(s3.upper())
print(s3.lower())
print(s3.title()) #makes every word starting letter upper case n followed by lower case
