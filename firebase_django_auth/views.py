from django.http import JsonResponse
from firebase_admin import auth
from user_profiles.serializers import UserProfileSerializer
from rest_framework import viewsets
from user_profiles.models import UserProfile
from firebase_admin import firestore


def verify_token(request):
    token = request.headers.get('Authorization').split('Bearer ')[1]
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        return JsonResponse({"status": "success", "uid": uid})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

class UserProfileViewSet(viewsets.ViewSet):
    def list(self, request):
        db = firestore.client()
        users_ref = db.collection('users')
        docs = users_ref.stream()

        user_list = []
        for doc in docs:
            user_list.append(doc.to_dict())

        return JsonResponse(user_list, safe=False)