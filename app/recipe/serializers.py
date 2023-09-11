"""
    Recipe serializer
"""

from rest_framework import serializers

from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """ Serializer for recipes """

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link']
        read_only_fields = ['id']


# RecipeDetailSerializer is an extension of the RecipeSerializer for that reason extends it
class RecipeDetailSerializer(RecipeSerializer):
    """ Serializer fo recipe detail view"""

    # Taking the model and fields of the Base Recipe Serializer
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']



