from rest_framework import serializers

from .models import Products


class StandartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = '__all__'