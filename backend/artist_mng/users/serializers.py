from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['is_staff', 'is_admin']

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            date_of_birth=validated_data['date_of_birth'],
            gender=validated_data['gender'],
            address=validated_data['address'],
            country=validated_data['country'],
            is_artist=True 
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
