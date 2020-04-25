from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('public_name', 'email', 'password',
                  'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def validate_public_name(self, value):
        """Validates the public name"""
        if ' ' in value.strip():
            raise serializers.ValidationError(
                'Username must not contain whitespaces.')
        return value

    def update_login(self, instance=None, login_data=None):
        if instance and login_data:
            user = super().update(instance, login_data)
            return user
        return None

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')

        # Updates last_login everytime a token is requested
        login = {'last_login': timezone.now()}
        serializer = UserSerializer(user)
        log_usr = serializer.update_login(user, login)
        if log_usr:
            user = log_usr
        attrs['user'] = user
        return attrs
