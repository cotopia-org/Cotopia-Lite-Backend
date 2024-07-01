import os
from dotenv import load_dotenv


load_dotenv()

GOOGLE_CLIENT_ID = os.environ.get('google-client-id', None)
GOOGLE_CLIENT_SECRET = os.environ.get('google-client-secret', None)
GOOGLE_REDIRECT_URL=os.environ.get('google-redirect-url', None)