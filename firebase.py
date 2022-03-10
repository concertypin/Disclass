import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

db = None


class FirebaseNotReady(Exception):
    def __init__(self, msg=None):
        if msg is not None:
            self.msg = msg
        else:
            self.msg = "db is None. call firebase.auth() to fix these."

    def __str__(self):
        return self.msg


def auth(certificate_path):
    global db
    cred = credentials.Certificate(certificate_path)
    firebase_admin.initialize_app(cred)

    db = firestore.client()


def write(collection_name, document_name, data):
    # data must be dict
    if db is None:
        raise FirebaseNotReady
    # noinspection PyUnresolvedReferences
    doc_ref = db.collection(collection_name).document(document_name)
    doc_ref.set(data)


def read(collection_name):
    if db is None:
        raise FirebaseNotReady
    # noinspection PyUnresolvedReferences
    users_ref = db.collection(collection_name)
    docs = users_ref.stream()

    r = {}
    for doc in docs:
        r[doc.id] = doc.to_dict()
    return r
