a = [
{'id':1,'name':'john', 'age':34},
{'id':1,'name':'john', 'age':34},
{'id':1,'name':'johns', 'age':34},
{'id':2,'name':'hanna', 'age':30},
]

#b=list({d['id']: d for d in a}.values())

d = list()
for l in a:
    if l in d:
        pass
    else:
        d.append(l)

# c = list(set(a))
print(d)