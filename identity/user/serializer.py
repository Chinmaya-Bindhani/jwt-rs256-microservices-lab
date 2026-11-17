from rest_framework import  serializers
from django.contrib.auth import get_user_model
User = get_user_model()

class RegisterUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password= serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_email(self, attrs):
        if User.objects.filter(email=attrs).exists():
            raise serializers.ValidationError("This email is already associated with us ")
        return attrs

    def validate(self,data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('2 passwords arent matching with each other ')
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


# this one is for user details

class ViewMe(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['id','email','username','first_name','last_name']