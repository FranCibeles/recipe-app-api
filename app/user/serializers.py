"""
Serializers for the Users API View
"""

from django.contrib.auth import (
    get_user_model,
    authenticate
)

from django.utils.translation import gettext as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """ Serializer for the user object """

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """ Create and return a user with encrypted password """
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return user - Overwritting the update method of DRF
        Instance: Is the model instance that is going to be updated
        Validated Data: Data which is going to be passed through the Serializer
        """

        # Pop() retrieves the password and pops out of the request
        password = validated_data.pop('password', None)

        # Overwritting the update method from the ModelSerializer
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """ Serializer for the User Token """
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """ Validate and authenticate the user. Method called on the validaton phase in the user create view"""

        # Retrieves the email and password which is passed in the request atributes
        email = attrs.get('email')
        password = attrs.get('password')

        """
            Authenticate is Django built-in Function - Accepts three parameters
            Request -> Checks if the request is passed correctly (required)
            Username -> We use the email
            Password -> If the password is correct than is going to return the user object. 
                        If not returns an empty object
        """
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')

        # If there is a user created succesfully -> It's going to be saved and returned
        attrs['user'] = user
        return attrs