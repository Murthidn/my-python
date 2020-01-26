#Only Unique values

st={1,2,3,4}
st.update([6,7]) #doen't gurantee order while adding new elem, use sqaure bracket while adding
print(st)

#So only we can't perform indexing, slicing, repeation

#can perform update and remove
st.remove(7)
print(st)

#FROZEN SET - once we convert to frozenset, we can't modify set
frozenset(st)

#when frozen, we can only navigate/loop/print