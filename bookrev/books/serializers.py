from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from books.models import *

class BooksSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Books
        fields = "__all__"
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from books.models import *

class BooksSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Books
        fields = "__all__"
