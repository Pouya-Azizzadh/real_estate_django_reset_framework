
from rest_framework import serializers
from user.models import CustomUser
from django.contrib.auth import authenticate

from rest_framework import serializers






class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=30)
    password = serializers.CharField()
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone_number',
                  'national_code', 'image_profile', 'password', 'confirm_password']

    def create(self, validated_data):
        del validated_data['confirm_password']
        user = CustomUser.objects.create_user(
            **validated_data
        )
        return user

    def validate(self, value):
        if value.get('password') != value.get("confirm_password"):
            raise serializers.ValidationError("تکرار پسورد درست نیست")
        return value


class LogInUserSerializer(serializers.Serializer):
    email=serializers.EmailField(required=True)
    phone_number = serializers.CharField()
    password=serializers.CharField()
    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number', 'password']

    def validate(self, attrs):
        email=attrs.get('email')
        password=attrs.get('password')
        phone_number=attrs.get('phone_number')
        user =CustomUser.objects.get(email=email)
        if not user.password==password:
                raise serializers.ValidationError({'password': 'رمز درست نیست!'})
        elif not user.phone_number==phone_number:
                raise serializers.ValidationError({'phoneNumber': 'شماره تلفن درست نیست'})
        else:
            return user
 