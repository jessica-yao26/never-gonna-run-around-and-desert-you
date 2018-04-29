from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    first_name = serializers.CharField(required=True, min_length=1)
    last_name = serializers.CharField(required=True, min_length=1)
    username = serializers.CharField(max_length=32, validators=[UniqueValidator(queryset=User.objects.all())])
    # phone_number = serializers.CharField(required=True, min_length=10, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'], validated_data['username'], validated_data['password'], validated_data['first_name'], validated_data['last_name'])
        return user        

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'first_name', 'last_name')

class TokenCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, validated_data):
        user = authenticate(username=validated_data.get('username'), password=validated_data.get('password'))
        if not user:
            raise serializers.ValidationError("invalid_credentials")
        validated_data['user'] = user
        return validated_data