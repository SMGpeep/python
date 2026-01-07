import os
import person as pers

class PersonDB:
    def __init__(self):
        self.persons = {}

    def addPerson(self, person):
        if self.persons.get(person.name):
            raise ValueError(f"{person} existiert bereits !!")
        self.persons.update({person.name : person})

    def clear(self):
        self.persons = {}

    def findPerson(self, name):
           return self.persons.get(name)

    def removePerson(self, name):
        try:
            return self.persons.pop(name)
        except KeyError:
            return None

    def laden(self,path):
        self.clear()

        if  False == os.path.exists(path):
            print(f"die angegebene Datei existiert nicht:{path} ")
            return self

        file = open(path, "r")
        personLines = file.readlines()
        file.close()

        for line in personLines:
            splits = line.split(",")
            if splits.__len__() <= 1:
                continue

            pName = pers.Name(splits[0],splits[1])
            peter = pers.Person(pName, splits[2])
            self.addPerson(peter)

        print(f"found following persons in file: {personLines} - path: {path}")
        print(f"=> dict: {self.persons}")
        return self

    def speichern(self, path):

        if  False == os.path.exists(path):
            print(f"creating new File: {path} ")

        file = open(path, "w")

        for (key,value) in self.persons.items():
            file.write(f"{key.vorname.strip()}, {key.nachname.strip()}, {value.bday} \n")


        file.close()
        print(f"wrote persons into file: {self.persons} - file: {path}")

        return True