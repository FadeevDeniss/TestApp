import os

# Settings allows you to manage app running mode
# and calculate project root paths etc.

# Debug mode

DEBUG = True

# Absolute paths to project directories

ROOT = os.path.dirname(os.path.abspath('src'))
STATIC = os.path.join(ROOT, 'static')

# Base url address requested application server
# Set the correct url if you run app in production!

BASE_URL = 'http://127.0.0.1:5000' if DEBUG else ''
