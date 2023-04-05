import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

# Use a service account.
creds_path = os.getcwd() +'/config/hub.json'
cred = credentials.Certificate(creds_path)

app = firebase_admin.initialize_app(cred)

db = firestore.client()