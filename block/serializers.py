from rest_framework import serializers

class TokenRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    token = serializers.CharField(min_length=4)
