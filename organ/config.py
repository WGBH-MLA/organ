from os import environ

from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = environ.get('ENVIRONMENT', 'development')
DB_URL = environ.get('DB_URL', 'postgresql://postgres:postgres@localhost:5432/organ')

# postgresql://postgres:coolcool@organ-db-dev.cmrjt7rckp5r.us-east-1.rds.amazonaws.com:5432
ORGAN_SECRET = environ.get('ORGAN_SECRET', 1234567890)

# TEMPLATES_DIR = environ.get('TEMPLATES_DIR', 'templates')
# STATIC_DIR = environ.get('STATIC_DIR', 'static')
SECRET_KEY = environ.get('SECRET_KEY', 'secret')
AUTH0_DOMAIN = environ.get('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = environ.get('AUTH0_CLIENT_ID')
