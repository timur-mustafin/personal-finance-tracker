
from rest_framework import serializers
from .models import ImportSession


class ImportSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportSession
        fields = '__all__'
        read_only_fields = ('user', 'status', 'uploaded_at', 'error_message')
