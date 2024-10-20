import firebase_admin
from firebase_admin import storage, firestore

db = firestore.client()
bucket = storage.bucket()

def subir_avatar(archivo_local, nombre_usuario):
    blob = bucket.blob(f'avatars/{nombre_usuario}.jpg')
    blob.upload_from_filename(archivo_local)
    blob.make_public()
    
    avatar_url = blob.public_url
    print(f"Avatar subido con éxito. URL: {avatar_url}")
    
    agregar_usuario(nombre_usuario, f'{nombre_usuario}@example.com', avatar_url)
