
from rest_framework import viewsets, permissions, status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from .models import ImportSession
from .serializers import ImportSessionSerializer


class ImportSessionViewSet(viewsets.ModelViewSet):
    serializer_class = ImportSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]

    def get_queryset(self):
        return ImportSession.objects.filter(user=self.request.user).order_by('-uploaded_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
