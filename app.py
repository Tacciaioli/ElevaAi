from flask import Flask
from config.settings import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
