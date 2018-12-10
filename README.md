# msccs-t23
Identify &amp; categorize tweets during emergencies, visualize &amp; analyze data produced by system.

Part of the University of Glasgow Master's Team Project for Data Science students.

### Hierarchy of this project:

- app #Store flask based web application code.

    -- for

    -- static #store static resource
 
    -- templates #Store html templates

 - classifier #store the classfier code
 
    -- data_files_scripts #store database code

 - flask #virtual environment of this project

### To run this project
#### Use the virtual enviroment built in this project.
    in windows, enter msccs-t23 folder by cmd, type following command.
    >> flask\Scripts\activate
    >> python helpme.py
    
    in Linux/Macos, enter msccs-t23 folder by cd, type following command.
    >> source flask/Scripts/activate
    >> python helpme.py

#### Use your own enviroment.
Sometimes the virtual enviroment can not be used in some machines. In this case, please use your python enviroment and run this project after you intalled these dependences:

- Flask:
    >>python -m pip install Flask

- Pymongo:
    >>python -m pip install pymongo

- flask_wtf:
    >>python -m pip install flask_wtf

- numpy:
    >>python -m pip install numpy

- sklearn:
    >>python -m pip install sklearn

- nltk:
    >>python -m pip install nltk

- nltk data:
    >>python 
    >>import nltk
    >>nltk.download('stopwords')
    >>exit()
           
- Tweepy:
    >>python -m pip install tweepy

- dateutil:
    >>python -m pip install python-dateutil

### Database

**This project is based on a could database and will connect to it automaticlly**

Database: MongoDB

DatabaseName: Helpme

CollectionName:
"Test"Store testdata.

"Train" Store TrainLabels

"Training_token" Store Trainingdata.

"func_test" collection for testing functions.

"TweetsData" Store all the TweetsData.
