# class for reading the dataset from a json file
import json


class Reader():

    def __init__(self, name=""):
        self.name = name

    #Main method of the class
    #returns a list[] of json elements of type:
    # [postID, categories[], indicatorTerms[], priority]
    # []
    def read(self, filename):
        with open(filename, encoding="utf8") as json_data:
            data = json.load(json_data)
            list = []
            final_list = []
            #for i in the range of the events,(here we have 5)
            #we create a size 6 list which its element is a list of json elements, grouped by events
            for i in range(0,len(data['events'])):
                list.append(data["events"][i]["tweets"])
            #append every element to the final list as a simple json elementself.
            # now we have a 1d list with every tweet ready to be inserted to our db.
            for x in list:
                for e in x:
                    if(e is not None):
                        final_list.append(e)
                        
            return final_list
