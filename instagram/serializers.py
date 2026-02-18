from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'instagram_id', 'caption', 'media_type', 'media_url', 'permalink', 'timestamp', 'updated_at']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'instagram_id', 'post', 'text', 'timestamp', 'username', 'created_at']
        read_only_fields = ['instagram_id', 'timestamp', 'username']

class CommentCreateSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=1000)

    def create(self, validated_data):
        pass