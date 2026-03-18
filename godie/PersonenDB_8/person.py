import datetime

def newDate(day, month, year):
     return datetime.date(year = year, month =  month, day =day)

class Name:
    def __init__(self, vorname, nachname):
        self.vorname = vorname.strip()
        self.nachname = nachname.strip()
  
    def __eq__(self, other):

        if not isinstance(other, Name):
            return False
    
        return self.nachname == other.nachname and self.vorname == other.nachname    
    
    def __hash__(self):
        return hash((self.vorname, self.nachname))

    def __str__(self):
        return(f"{self.vorname} {self.nachname}")

    def __repr__(self):
        return self.__str__()


class Person:
    def __init__(self, Name, bday):
        self.name = Name
        self.bday = bday

    def __str__(self):
        return(f"{self.name.vorname} {self.name.nachname} geboren am: {self.bday}")

    def __repr__(self):
        return self.__str__()

    def alter(self):
        bHadBDay = False
        today = datetime.date.today()

        if self.bday.month >= today.month:
            if self.bday.day >= today.day:
                bHadBDay = True

        return today.year - self.bday.year + int(bHadBDay)

    def nächster_geburtstag(self):
        return newDate(day= self.bday.day, month= self.bday.month, year = self.bday.year+self.alter()+1)
