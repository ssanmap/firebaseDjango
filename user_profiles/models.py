# user_profiles/models.py

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from firebase_admin import storage, auth
from firebase_django_auth.server.conection import db
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError



class UserProfile(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def clean(self):
        if not self.avatar:
            raise ValidationError("El avatar es obligatorio.")

    def save(self, *args, **kwargs):
        self.full_clean()  
        avatar_url = None
        if self.avatar:
            avatar_url = self.upload_avatar_to_storage()

        # Guardar datos del usuario en Firestore (excepto la contraseña)
        user_data = {
            'name': self.name,
            'email': self.email,
            'avatar_url': avatar_url if self.avatar else None,
        }
        db.collection('users').document(self.email).set(user_data)
        print(f"Usuario guardado en Firestore: {user_data}")

        # Crear el usuario en Firebase Authentication (opcional)
        try:
            user = auth.get_user_by_email(self.email)
        except auth.UserNotFoundError:
            user = auth.create_user(
                email=self.email,
                display_name=self.name,
                password='YourSecurePassword'  # Deberías generar contraseñas seguras
            )
            print(f"Usuario creado en Firebase Authentication: {user.uid}")

    def upload_avatar_to_storage(self):
        # Guardar la imagen en Firebase Storage
        avatar_path = default_storage.save(self.avatar.name, self.avatar)
        bucket = storage.bucket()
        avatar_blob = bucket.blob(f'avatars/{self.email}/{self.avatar.name}')
        avatar_blob.upload_from_filename(avatar_path)
        avatar_url = avatar_blob.public_url
        return avatar_url            