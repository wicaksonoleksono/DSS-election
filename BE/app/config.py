import firebase_admin
from firebase_admin import credentials, firestore


def init_firebase():
    cred = credentials.Certificate("./FirebaseCred.json")
    firebase_admin.initialize_app(cred)
    return firestore.client()
