from rest_framework import serializers

from core.models import Permission, Group
from core.api.groups.serializers import GroupSerializer


class PermissionSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, required=False)

    class Meta:
        model = Permission
        fields = ['id', 'name', 'code_name', 'groups']

    def associate_group(self, pk, groups):
        list_groups = []

        for group in groups:
            list_groups.append(Group.objects.get(name=group['name']))

        permission = Permission.objects.get(id=pk)
        permission.groups.set(list_groups)
        permission.save()

    def create(self, validated_data):
        groups = validated_data.get('groups')

        if groups and len(groups) > 0:
            del validated_data['groups']
            permission = Permission.objects.create(**validated_data)
            permission.save()
            self.associate_group(permission.id, groups)

        else:
            permission = Permission.objects.create(**validated_data)
            permission.save()

        return permission

    def update(self, instance, validated_data):
        groups = validated_data.get('groups')

        if groups and len(groups) > 0:
            del validated_data['groups']
            instance.code_name = validated_data.get('code_name', instance.code_name)
            instance.name = validated_data.get('name', instance.name)
            instance.save()
            self.associate_group(instance.id, groups)

        else:
            instance.code_name = validated_data.get('code_name', instance.code_name)
            instance.name = validated_data.get('name', instance.name)
            instance.groups.set([])
            instance.save()

        return instance
