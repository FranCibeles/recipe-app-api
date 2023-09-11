"""
    Recipe serializer
"""

from rest_framework import serializers

from core.models import Recipe, Tag


class TagSerializer(serializers.ModelSerializer):
    """ Serializer for Tags """

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """ Serializer for recipes """
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags']
        read_only_fields = ['id']

    def _get_or_create(self, tags, recipe):
        """ Handle getting or creating tags as needed """
        auth_user = self.context['request'].user

        # Taking the auth_user object. It's used the context because we are doing this operation in the serializer
        # Teh context is passed through the view for the serializer
        auth_user = self.context['request'].user
        for tag in tags:
            #  get_or_create is a helper function of the model manager. If the value doesn't exist create it. If exists
            # takes the value
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag
            )
            recipe.tags.add(tag_obj)

    def create(self, validated_data):
        """ Create a recipe """

        # Removes tags from the validated data
        tags = validated_data.pop('tags', [])

        # Create a recipe with the validated data excluding tags
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create(tags, recipe)

        return recipe

    def update(self, instance, validated_data):
        """ Update a recipe """

        # Removes tags from the validated data
        tags = validated_data.pop('tags', None)

        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()


# RecipeDetailSerializer is an extension of the RecipeSerializer for that reason extends it
class RecipeDetailSerializer(RecipeSerializer):
    """ Serializer fo recipe detail view"""

    # Taking the model and fields of the Base Recipe Serializer
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
