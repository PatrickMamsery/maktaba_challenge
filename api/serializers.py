from rest_framework import serializers
from upload.models import CSVFile

class CSVFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CSVFile
        fields = ['id', 'file_name', 'file', 'uploaded_at', 'active']


class DataSerializer(serializers.Serializer):
    data = serializers.ListField()