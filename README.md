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
**first you need have a python 3.5+ installed**
To check it, use command and input:

    >> python -V
    
#### 1. Activate the virtual enviroment built in this project.

    in windows, enter msccs-t23 folder by cmd, type following command.
    
    >> flask\Scripts\activate
    
    in Linux/Macos, enter msccs-t23 folder by cd, type following command.
    
    >> source ./flask/Scripts/activate

#### 2. Install the dependences.
You can install the dependences by two ways:

    1. use our requirements.txt to automacticlly install the dependences.
    
    >> python -m pip install -r requirements.txt

    >> python

    >> import nltk

    >> nltk.download('stopwords')

    >> exit()

2. Check the following dependences and install them by yourself.

- Flask:

    python -m pip install Flask

- Pymongo:


    python -m pip install pymongo
    

- flask_wtf:
     
    python -m pip install flask_wtf

- numpy:
         
    python -m pip install numpy
    
- sklearn:
         
    python -m pip install sklearn
    
- nltk:
         
    python -m pip install nltk
    
- nltk data:
       
    python 
       
    import nltk
       
    nltk.download('stopwords')
       
    exit()
           
- Tweepy:
        
    python -m pip install tweepy

- dateutil:
    
    python -m pip install python-dateutil
    
### Database

**This project is based on a could database and will connect to it automaticlly**

Database: MongoDB

DatabaseName: Helpme

CollectionName:
"Test"Store testdata.

"Train" Store TrainLabels


"Training_Token" Store Trainingdata.


"func_test" collection for testing functions.

"TweetsData" Store all the TweetsData.
