
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializers import UserSerializer


User = get_user_model()


class MeView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
