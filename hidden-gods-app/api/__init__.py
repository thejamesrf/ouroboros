"""
Hidden Gods API
===============
Flask/FastAPI routes for the Hidden Gods game app.
"""

from flask import Flask

app = Flask(__name__)

# Import routes
from . import routes
