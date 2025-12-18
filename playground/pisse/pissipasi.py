piss = {
    "Alice": 3.7,
    "Bob": 4.2,
    "Charlie": 2.9,
    "Diana": 3.5,
    "Edward": 4.0,
    "Fiona": 4.8,
    "George": 1.8,
    "Helen": 2.5,
    "Isaac": 3.9,
    "Julia": 2.2,
    "Kevin": 4.5,
    "Laura": 3.0
}


# Create a list called 'pisslist' that contains the names (keys) from 
# the 'piss' dictionary
# Only include names where the associated value 
# (e.g., score or rating) is less than or equal to 4.0
pisslist = [k for k, v in piss.items() if v <= 4.0]


print(pisslist)


