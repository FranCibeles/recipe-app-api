"""
    Views for the Recipes API
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers

"""
    ModelViewSet is specific to CRUD Operations with Models
"""


class RecipeViewSet(viewsets.ModelViewSet):
    """ View for manage recipe APIs"""

    serializer_class = serializers.RecipeDetailSerializer

    # Queryset represents the objects which are available for all the viewset
    queryset = Recipe.objects.all()

    # In order to use every endpoint the user must be authenticated -> This can be proved with this two classes
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    """
        To obtain the recipes of the autenticated users there must be the queryset filtered
    """

    def get_queryset(self):
        """ Retrieve recipes for authenticated user """
        return self.queryset.filter(user=self.request.user).order_by('-id')

    """
        Overwritting the method that uses Django to obtain the serializers to modify therefore, everytime the detail endpoint
        is called, is going to be used the Detail Serializer
    """

    def get_serializer_class(self):
        """ Return the serializer class for detail request """
        if self.action == 'list':
            return serializers.RecipeSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """ Create a new recipe """
        serializer.save(user=self.request.user)
