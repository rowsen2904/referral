import random
import time
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import AuthCode, User
from helpers.validation import validate_russian_phone


class ActivateInviteCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)

    def validate_code(self, value):
        request_user = self.context['request'].user

        try:
            invited_user = User.objects.get(invite_code=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                _("Such an invite code does not exist"))

        if request_user.invite_code == value:
            raise serializers.ValidationError(
                _("You cannot activate your own code"))

        if request_user.activated_invite_code:
            raise serializers.ValidationError(
                _("You have already activated the invite code"))

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


class MyProfileSerializer(serializers.ModelSerializer):
    referrals = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("phone_number", "invite_code",
                  "activated_invite_code", "referrals")

    def get_referrals(self, obj):
        return list(obj.get_referred_users().values_list("phone_number", flat=True))


class RequestCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate_phone_number(self, value):
        return validate_russian_phone(value)

    def create(self, validated_data):
        code = f"{random.randint(1000, 9999)}"
        phone = validated_data['phone_number']

        AuthCode.objects.create(phone_number=phone, code=code)

        time.sleep(2)

        print(f"Code sent to number {phone}: {code}")
        return {"phone_number": phone}


class VerifyCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField(max_length=4)

    def validate(self, attrs):
        phone = attrs['phone_number']
        code = attrs['code']
        try:
            auth_code = AuthCode.objects.filter(
                phone_number=phone).latest('created_at')
        except AuthCode.DoesNotExist:
            raise serializers.ValidationError("Code not found")

        if auth_code.code != code:
            raise serializers.ValidationError("Invalid code")

        return attrs

    def create(self, validated_data):
        phone = validated_data['phone_number']
        user, created = User.objects.get_or_create(phone_number=phone)
        return user
