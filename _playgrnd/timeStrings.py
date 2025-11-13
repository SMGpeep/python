import datetime as dt
import re
import string


def containsTimeString(string):
    # is there any time representation in this thing?
    return False

def justYoloIt(string):

    for char in string:
        if char.isdigit():
            print("go fuck")
        elif char.isalpha():
            print("about to fuck")

    # parse for day, month and year respectively
    # day: 1-31  -> ppl are gonna be re and not respect the 0 ?
    # month: 1-12
    # year:
    # for the 2ks: 00 - 37~ ? -> 20xx
    # for the 1ks: 60~ - 99 -> 19xx
    # 'b.c.' -> take the prior numbers
    # 'a.c.' ? -> take the prior numbers + '-' (are negative times even supported?)
        # if u take anything else, go fk lol

    # idk

    day = 12
    month = 10
    year = 2020

    return dt.datetime(year, month, day)

def parseStringFormat(string):
    # do some random parsing sht
    # string needs to be timeString
    # returns the time Format
    return string.replace(" ", "")

def getDateTimeFromString(string):
    format = parseStringFormat(string)
    return dt.datetime.strptime(string, format)

piss = dt.datetime.today()
pissStr = "2025-12-11 20:39:16"
sqrtStr = "aa-sss-bvv-as-d-asd-as"
kek = justYoloIt(sqrtStr+pissStr)
print(kek)


