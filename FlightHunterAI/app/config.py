from dotenv import load_dotenv
import os

load_dotenv()

DUFFEL_API_KEY = os.getenv("DUFFEL_API_KEY")
TIMEOUT = 20