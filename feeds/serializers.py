from attr import field
from rest_framework import serializers
from feeds.models import Feeds, Comments
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer

class FeedsSerializer(TaggitSerializer, serializers.ModelSerializer):
    #image = serializers.SerializerMethodField()
    tags = TagListSerializerField()

    class Meta:
        model = Feeds
        fields = ['id', 
                  'author', 
                  'body', 
                  'posted_on', 
                  'likes', 
                  'image', 
                  'hide_post', 
                  'tags', 
                 # 'hitcount_generic'
                 ]

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'