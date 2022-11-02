from . import models
from rest_framework import serializers

class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Receipt
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'id',
            'username',
            'enrollment',
            'name',
            'course',
            'image',
            'balance',
        )
        extra_kwargs = {'password': {'write_only': True}}

class TransferDataSerializer(serializers.Serializer):
    transfer_user =  serializers.IntegerField()
    transfer_value = serializers.CharField(max_length=7)

