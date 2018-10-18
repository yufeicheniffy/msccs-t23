from DB import DB
from Reader import Reader

database = DB("mongodb://localhost:27017/", "mscdb", "msc")
read = Reader("name of the reader")
l = read.read("TRECIS-CTIT-H-Training.json")
#first parameter is the collection.
database.insert("test", l)
database.print_all("test")
