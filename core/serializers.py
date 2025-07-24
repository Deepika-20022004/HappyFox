from rest_framework import serializers
from .models import *

class CompanyDriveSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDrive
        fields = '__all__'