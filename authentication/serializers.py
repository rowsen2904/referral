from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import User


class ActivateInviteCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)

    def validate_code(self, value):
        request_user = self.context['request'].user

        try:
            invited_user = User.objects.get(invite_code=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(_("Such an invite code does not exist"))

        if request_user.invite_code == value:
            raise serializers.ValidationError(_("You cannot activate your own code"))

        if request_user.activated_invite_code:
            raise serializers.ValidationError(_("You have already activated the invite code"))

        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        code = self.validated_data['code']
        user.activated_invite_code = code
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'invite_code', 'activated_invite_code']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['phone_number'] = instance.phone_number
        return data
