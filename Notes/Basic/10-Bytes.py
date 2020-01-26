lst=[1,2,3,4,5] #upto 255 as it's gonna be byte
b=bytes(lst)
print(type(b))

#b[2]=9 # can't assign values

ba=bytearray(lst)
print(type(ba))
ba[2]=10
print(ba)

#so only assign allowed in Bytearray but no slicing/repetation in both bytes n bytearray