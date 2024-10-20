import firebase_admin
from firebase_admin import firestore

db = firestore.client()

def agregar_usuario(nombre, correo, avatar_url=None):
    doc_ref = db.collection(u'usuarios').document()
    datos_usuario = {
        u'nombre': nombre,
        u'correo': correo,
        u'avatar_url': avatar_url
    }
    doc_ref.set(datos_usuario)
    print(f"Usuario {nombre} agregado con éxito.")
