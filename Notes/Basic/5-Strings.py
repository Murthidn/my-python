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

#String Methods - Note: All string methods returns new values. They do not change the original string.

#String Strip
s2='  Hey Man!  ' #Skips 1st & last Spacess
print(s2)
print(s2.strip())
print(s2.lstrip()) #left strip
print(s2.rstrip()) #right strip

#Find - #To find a substring in string, gives the index from where it starts
print(s2.find('Man'))
print(s2.find('xxx')) #if value is not there, gives -1
print(s2.find('Man', 0, len(s2))) # we can specify from where to search (2nd value) and where to stop
print(s2.find('Man', 10, len(s2))) # string returns -ve value (-1) if we are accessing out of index but won't error

#Count
print(s2.count('M')) #Prints no. of occurances of given sub string

#Replace
print(s2.replace('Man', 'Buddy')) #replaces given substring

#Upper, Lower, Tittle
s3='Hello Murthi dN'
print(s3.upper())
print(s3.lower())
print(s3.title()) #makes every word starting letter upper case n followed by lower case

#Capitalize - #Capitalize makes 1st letter to big & small to others
string = "a is an operator"
print(string.capitalize()) #

#Center - makes a string middle with given character, by default space is taken
s4="Python is Beautiful!"
print(s4.center(24)) #width to extend string with center
print(s4.center(24, '*')) #2nd arg is fill char, by default space comes else given by user

#Casefold - makes entire string in to lowercase
firstString = "HEY MAN"
print(firstString.casefold())

#Count - returns how many time substring occured
string='Murthi is awesome, isn\'t it?'
subString="is"
print(string.count(subString))

#Endswith - returns true if string ends with substring
print(string.endswith('it?'))
#you can also specify the start & end
print(string.endswith('it?', 4, 10))

#Expandtabs - replaces \t with 8 spaces (tab)
str='Ones\tTwo\tThree'
print(str.expandtabs())

#Encode - encodes Unicoded string to Encoded format (in Python all strings are Unicoded)
str='pythön!'
print(str.encode()) # by default UTF-8 encode

#format - formats given string into a nicer output
print("Hello {}, your balance is {}.".format("Adam", 230.2346))

#index - returns index of substring if found, else error
str="Helo Murthi"
print(str.index('Murthi'))

#isallnum = returns True if all char either alphabets or numerics, else False even if it has single space
str='Murthi1996'
print(str.isalnum())

#isalpha - returns True if all char are alphabets, else False
str='Murthi'
print(str.isalpha())

#isdecimal - returns True if all char are decimals are numbers
str='1996'
print(str.isdecimal())

#isdigit - returns True if all char are digits
str='1996'
print(str.isdigit())

#isidentifier - returns True if string is valid identifier in Python (Py identifiers)
str='96Murthi'
str2='Murthi'
print(str.isidentifier())
print(str2.isidentifier())

#islower - returns True is all char are lower case
str='murthi'
print(str.islower())

#isnumeric - returns True if all char are numbers
str='1996'
print(str.isnumeric())

#isprintable - returns True if that string is printable
str='printable'
str2='\nnew line isnot printable'
print(str2.isprintable())
print(str.isprintable())

#isspace - returns True if there are only spaces or tabs in char
str='   \t'
print(str.isspace())

#istitle - retuns True if string is Title (first letter of word is Upper n ignore special char, num
str1='Hi murthi'
str2='Hi Murthi'
str3='Hi @ Murthi'
str4='96 Hi Murthi'
str5='MURTHI'

print(str1.istitle())
print(str2.istitle())
print(str3.istitle())
print(str4.istitle())
print(str5.istitle())

#isupper - returns True if all are UPPER
str='MURTHI'
print(str.isupper())

#join - returns a string concatenated with the elements of an iterable.
numList = ['1', '2', '3', '4']
seperator = ', '
print(seperator.join(numList))

numTuple = ('1', '2', '3', '4')
print(seperator.join(numTuple))

#ljust - left-justified string of a given minimum width
string = 'cat'
width = 5
fillchar = '*'

print(string.ljust(width))
print(string.ljust(width, fillchar))


#ljust - right-justified string of a given minimum width
string = 'cat'
width = 5
fillchar = '*'

print(string.rjust(width))
print(string.rjust(width, fillchar))

#swapcase - converts all BIG letter to SMALl or SMALL - BIG
str='MurthI'
print(str.swapcase())

#rfind - returns the highest index of the substring (if found). If not found, it returns -1.
str = 'Let it be, let it be, let it be'
print(str.rfind('let it'))

#rindex - returns highest index of the substring inside the string (if found). If the substring is not found, it raises an exception
str = 'Let it be, let it be, let it be'
print(str.rindex('let it'))

#split - breaks up a string at the specified separator and returns a list of strings.
text= 'Love thy neighbor'

# splits at space
print(text.split())

grocery = 'Milk, Chicken, Bread'

# splits at ','
print(grocery.split(', '))

# Splitting at ':'
print(grocery.split(';'))

#splitlines() - splits the string at line breaks and returns a list of lines in the string.
grocery = 'Milk\nChicken\r\nBread\rButter'

print(grocery.splitlines())

#startswith() - returns True if a string starts with the specified prefix(string). If not, it returns False.
str="Hi Murthi"
print(str.startswith('Hi'))