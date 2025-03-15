from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=False,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    username = serializers.CharField(
        read_only=True,
        validators=User._meta.get_field('username').validators #  it doesn't run validation since it's assigned in the signal
    )

    def create(self, validated_data):
        print("******Creating user")
        print(validated_data)
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user

    class Meta:
        model = User
        fields = [
            'url', 'id', 'username', 'email', 'first_name', 'last_name',
            'password'
        ]
