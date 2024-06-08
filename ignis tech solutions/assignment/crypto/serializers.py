from rest_framework import serializers

class CryptoRequestSerializer(serializers.Serializer):
    acronyms = serializers.ListField(
        child=serializers.CharField(max_length=10)
    )
