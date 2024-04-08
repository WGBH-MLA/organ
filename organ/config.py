from os import environ

ENVIRONMENT = environ.get('ENVIRONMENT', 'development')
DB_URL = environ.get('DB_URL', 'postgresql://postgres:pw@localhost:5432')

# postgresql://postgres:coolcool@organ-db-dev.cmrjt7rckp5r.us-east-1.rds.amazonaws.com:5432
ORGAN_SECRET = environ.get('ORGAN_SECRET', 1234567890)

# TEMPLATES_DIR = environ.get('TEMPLATES_DIR', 'templates')
# STATIC_DIR = environ.get('STATIC_DIR', 'static')
