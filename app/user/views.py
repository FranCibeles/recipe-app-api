"""
    View for the User API
"""

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """ Create a new User in the System """
    serializer_class = UserSerializer


# Built in View for Token
class CreateTokenView(ObtainAuthToken):
    """ Create a new token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """ Manage authenticated user """

    user_serializer = UserSerializer

    # To manage the authentication of the users
    authentication_classes = [authentication.TokenAuthentication]

    # Authorization Management
    permission_classes = [permissions.IsAuthenticated]

    # Overwrittes the get_object which get the objects which are passed into the HTTP Request
    def get_object(self):
        """ Retrieve and return the authenticated user """

        # Returns the user object which is authenticated - Then is going to be sent to the serializer and later on
        # promted
        return self.request.user
