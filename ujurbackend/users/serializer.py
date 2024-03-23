from rest_framework import serializers
from users.models import UsersDetails

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersDetails
        fields = "__all__"
