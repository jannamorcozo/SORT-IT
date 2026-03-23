import firebase_admin
from firebase_admin import credentials, firestore
from core.config import FIREBASE_KEY_PATH

cred = credentials.Certificate(FIREBASE_KEY_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()
