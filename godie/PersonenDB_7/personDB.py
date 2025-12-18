import os
import person as pers

class PersonDB:
    def __init__(self):
        self.persons = {}

    def addPerson(self, person):
        self.persons.update({person.name : person})

    def clear(self):
        self.persons = {}

    def findPerson(self, name):
        for (key,value) in self.persons.items():
            if (key.vorname.strip().lower() == name.vorname.strip().lower()
                            and key.nachname.strip().lower() == name.nachname.strip().lower())  :
                return value
        return None

    def removePerson(self,  name):

        person = self.findPerson(name)
        if(person is None):
            return False
        print(f"removing person ({person}) in file: {self.persons}")
        del self.persons[person.name]
        return True

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