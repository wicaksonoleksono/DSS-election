from app.utils.config import Config
from firebase_admin import firestore
from google.cloud.firestore_v1.collection import CollectionReference


# pakai logic ini factory method / abstrck fact method
class Connection:
    @staticmethod
    def get_collection(collection_name: str) -> CollectionReference:
        Config.init_firebase()
        db = firestore.client()
        return db.collection(collection_name)
