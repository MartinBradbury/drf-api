from rest_framework import serializers
from .models import Post

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializer.ReadOnlyField(source='owner.profile.id')
    profile_image = serializer.ReadOnlyField(source='owner.profile.image.url')

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def validate_image(self, value):
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Image size is too large, 2MB maximum.'
            )
        if value.image.width > 4096:
            raise serializer.ValidationError(
                'Image width is too large, 4096px maximum'
            )
        if value.image.height > 4096:
            raise serializer.ValidationError(
                'Image height is too large, 4096 maximum'
            )
        return value


    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'is_owner', 'profile_id',
            'profile_image', 'created_at', 'updated_at',
            'title', 'content', 'image', 'image_filter',
        ]