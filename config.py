import os
from dotenv import load_dotenv
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
load_dotenv()

SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PWD']}" \
                          f"@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"
