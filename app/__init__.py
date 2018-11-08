from flask import Flask
from config import Config
#init, create Flask instance
app = Flask(__name__)
app.config.from_object(Config) #set congif from config.py
from app import routes