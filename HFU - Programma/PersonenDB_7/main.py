import personDB as persDB
import person as pers

myDB = persDB.PersonDB().laden("Personen.txt")

while (True):

    print("-------------------------------------")
    print("wallah mashallah hier ist dein Menü:")
    print("1: Person hinzufügen ")
    print("2: Person suchen")
    print("3: Person entfernen")
    print("4: Datei speichern")
    print("5: Datei lesen")
    print("???: Person entfernen")
    mode = int(input("Bitte wählen Sie eine Nummer"))

    match mode:

        case 0:
            break

        case 1:
            print("Versuche Person hinzuzufügen...")
            print("Geben Sie PersonenDaten an:")
            vrname = input("Vorname:")
            nachname = input("Nachname:")
            bday = input("Geburtsdatum:")
            myDB.addPerson(pers.Person(pers.Name(vrname, nachname), bday))
            print(f"{vrname} {nachname} wurde erfolgreich hinzugefügt")

        case 2:
            print("Versuche Person zu finden...")
            print("Geben Sie PersonenDaten an:")
            vrname = input("Vorname:")
            nachname = input("Nachname:")
            pers = myDB.findPerson(vrname, nachname)
            if pers == None:
                print(f"Ich kenne {vrname}, {nachname} nicht :(")
            else:
                print(pers)

        case 3:

            print("Versuche Person zu löschen...")
            print("Geben Sie PersonenDaten an:")
            vrname = input("Vorname:")
            nachname = input("Nachname:")
            if myDB.removePerson(vrname, nachname):
                print(f"{vrname} {nachname} wurde erfolgreich gelöscht")
            else:
                print(f"konnte {vrname} {nachname} nicht löschen")

        case 4:

            print("Versuche Personen zu speichern...")
            print("Geben Sie den DateiPfad an:")
            path = input("Path:")
            print(path)
            if myDB.speichern(path):
                print(f"{path} wurde erfolgreich erstellt/gespeichert")
            else:
                print(f"Hat nicht geklappt :((( {path} wurde nicht erstellt")


        case 5:

            print("Versuche Personen zu lesen...")
            print("Geben Sie den DateiPfad an:")
            path = input("Path:")
            myDB= myDB.laden(path)

        case 6:
                print(myDB.persons)

        case 9:
                break

        case _:
            print("ungültiger Input, win32.exe wird gelöscht...")

    print("-------------------------------------")
    print("\n" * 4)