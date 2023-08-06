from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from waffle.models import Switch


User = get_user_model()


class SwitchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Switch
        fields = ('id', 'name', 'active', 'note', 'created', 'modified')


class DebugSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=120,
                                     write_only=True,
                                     style={'input_type': 'password'})
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'username', 'email', 'is_active', 'is_staff', 'password')

    def create(self, validated_data):
        phone_number = validated_data['phone_number']
        password = validated_data['password']
        email = validated_data.get('email')
        user = User.objects.create_superuser(phone_number=phone_number,
                                             email=email,
                                             password=password)
        user.type = User.STAFF
        user.is_superuser = user.is_active = user.is_staff = True
        user.save()
        return user
