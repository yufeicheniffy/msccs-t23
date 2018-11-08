#this is a class used to store Flask configs.
import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-code' #secret key to prevent Cross-Site Request Forgery
