import re
print('Enter Password')
pw=input()

isMatch=True
if len(pw)<8:
    isMatch=False
elif not re.search('[a-z]',pw):
    isMatch=False
elif not re.search('[A-Z]', pw):
    isMatch=False
elif not re.search('[0-9]', pw):
    isMatch=False
elif not re.search('[_@$]', pw):
    isMatch=False

if isMatch==True:
    print('Yes')
else:
    print('No')