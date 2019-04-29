from rest_framework import serializers
from .models import *


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('name',)
