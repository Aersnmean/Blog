from rest_framework_mongoengine import serializers
from .models import *


class UserSerializers(serializers.DocumentSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PostSerializers(serializers.DocumentSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class ReviewSerializers(serializers.DocumentSerializer):
    class Meta:
        model = Review
        fields = '__all__'
