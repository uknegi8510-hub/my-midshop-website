from rest_framework import serializers
from Accounts.models import User
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='display_name')

    class Meta:
        model = User
        fields = ['username', 'email', 'password','register_otp']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            display_name=validated_data.get('display_name')
        )
        return user

class VerifyRegisterSerializer(serializers.Serializer):
    email=serializers.EmailField()
    register_otp=serializers.CharField()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data["email"],
            password=data["password"]
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials")


        data["user"] = user
        return data
    


class VerifyLoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    login_otp=serializers.CharField()
