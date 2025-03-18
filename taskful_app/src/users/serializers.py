from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):

    user = serializers.HyperlinkedRelatedField(
        read_only=True,
        many=False,
        view_name="user-detail"
    )

    class Meta:
        model = Profile
        fields = ('url', 'id', 'image', 'user')


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=False,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    old_password = serializers.CharField(
        write_only=True,
        required=False,
        style={'input_type': 'password', 'placeholder': 'Old Password'}
    )
    username = serializers.CharField(
        read_only=True,
        validators=User._meta.get_field('username').validators #  it doesn't run validation since it's assigned in the signal
    )

    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'url', 'id', 'username', 'email', 'first_name', 'last_name',
            'password', 'old_password', 'profile'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            if 'old_password' in self.fields:
                self.fields.pop('old_password')

    def validate(self, data):
        """
        Validate input data from the serializer
        """
        request_method = self.context["request"].method
        password = data.get("password", None)
        if request_method == "POST":
            if password == None:
                raise serializers.ValidationError({"info": "Please provide a password"})
        elif request_method == "PUT" or request_method == "PATCH":
            old_password = data.get("old_password", None)
            if password != None and old_password == None:
                raise serializers.ValidationError({"info": "Please provide the old password"})
        
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user
    
    def update(self, instance, validated_data):
        try:
            user = instance
            if ('password' in validated_data
                    and 'old_password' in validated_data):
                password = validated_data.pop('password')
                old_password = validated_data.pop('old_password')
                if not user.check_password(old_password):
                    raise serializers.ValidationError({
                        "old_password": "Old password is not correct"
                    })
                user.set_password(password)

            # Update other fields
            for attr, value in validated_data.items():
                setattr(user, attr, value)

            user.save()
        except Exception as e:
            raise serializers.ValidationError({"info": str(e)})
            
        return user
