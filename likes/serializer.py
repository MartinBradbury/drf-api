from rest_framework import serializers
from .models import Like
from django.db import IntegrityError

class LikesSerializer(serializers.ModelSerializer):
    """
    Serializer for the Like model
    The create method handles the unique constraint on 'owner' and 'post'
    """

    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Like
        fields = [
            'id', 'owner', 'created_at', 'post',
            
        ]
    
    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializer.ValidationError({
                'detail': 'Possible Duplication'
            })