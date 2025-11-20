import person

def unique(s):
    res = ""
    for c in s:
        if c not in res:
            res += c
    return res

print(unique("abcccdddddeeeees"))

piss = person.Name("A","Beee")
pPerson = person.Person(piss,"10.10.2020")

pissDict = {
}

print(pissDict)



diss = person.Name("D","Ceee")
dPerson = person.Person(diss,"12.12.1111")


pissDict.update({diss: dPerson})

pissDict.update({piss: pPerson})


for (x,y) in pissDict.items() :
    print(x,y)

popN = dPerson.name

if popN in list(pissDict.keys()):
    pissDict.pop(popN)
    print("diss gepoppt ----- \n")

for (x,y) in pissDict.items() :
    print(x,y)
