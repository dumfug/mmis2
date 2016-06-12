#!/usr/bin/env python3
# encoding: utf-8

from flask import Flask
from .frontend import frontend
from .api import api

app = Flask(__name__)
app.register_blueprint(frontend)
app.register_blueprint(api, url_prefix='/api')
