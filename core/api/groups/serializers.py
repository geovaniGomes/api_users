from rest_framework import serializers


from core.models import Group

"""
  {
    "username": "aaaateste",
    "email": "aaateste@gmail.com",
    "first_name": "aa",
    "last_name": "aaa",
    "is_active": true,
    "is_staff": false,
    "password": "52002600NN"
  }

"""


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['id', 'name']

