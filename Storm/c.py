a=[{'a': 'aa', 'b': 'bb', 'c': 'cc', 'd':'dd'}]
l=[{'a': 'aa', 'b': 'bb', 'c': 'ccc'}]

for l in a:
  if l in a:
      print('Yes')
  else:
      print('No')
