# serializers class to data convert to json
from rest_framework import serializers
# user model class import
from accounts.models import User
# incrypt password
from django.contrib.auth.hashers import make_password

# Registration serializer class
class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password']

        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = super(RegistrationSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

