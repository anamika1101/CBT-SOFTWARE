from rest_framework import serializers
# from .models import Company
from admin_zone.models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'email', 'phone', 'password']

    def create(self, validated_data):
        # Handle password hashing here if needed
        return Company.objects.create(**validated_data)
