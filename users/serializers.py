from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, PasswordResetCode
from django.core.mail import send_mail
from django.conf import settings
import uuid

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'image')
        read_only_fields = ('id', 'role')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, label=_('Password'))
    confirm_password = serializers.CharField(write_only=True, label=_('Confirm Password'))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'confirm_password', 'first_name', 'last_name', 'role')

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": _("Parollar mos emas")})
        if data['role'] == 'moderator':
            if CustomUser.objects.filter(role='moderator').count() >= 10:
                raise serializers.ValidationError({"role": _("Moderatorlar soni 10 tadan oshmasligi kerak")})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(label=_('Username'))
    password = serializers.CharField(write_only=True, label=_('Password'))

class ProfileUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, min_length=8, label=_('Password'))

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'image', 'password')

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(label=_('Email'))

    def validate_email(self, value):
        try:
            user = CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(_("Bu email bilan foydalanuvchi topilmadi"))
        return value

    def save(self):
        email = self.validated_data['email']
        user = CustomUser.objects.get(email=email)
        code = PasswordResetCode.objects.create(user=user)
        send_mail(
            subject=_('Password Reset Code'),
            message=f"{_('Your password reset code')}: {code.code}\n{_('This code is valid for 30 minutes.')}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

class ResetPasswordConfirmSerializer(serializers.Serializer):
    code = serializers.UUIDField(label=_('Code'))
    new_password = serializers.CharField(min_length=8, write_only=True, label=_('New Password'))
    confirm_password = serializers.CharField(write_only=True, label=_('Confirm Password'))

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"new_password": _("Parollar mos emas")})
        try:
            reset_code = PasswordResetCode.objects.get(code=data['code'])
            if reset_code.expires_at < timezone.now():
                raise serializers.ValidationError({"code": _("Kodning amal qilish muddati tugagan")})
        except PasswordResetCode.DoesNotExist:
            raise serializers.ValidationError({"code": _("Noto‘g‘ri kod")})
        return data

    def save(self):
        code = self.validated_data['code']
        new_password = self.validated_data['new_password']
        reset_code = PasswordResetCode.objects.get(code=code)
        user = reset_code.user
        user.set_password(new_password)
        user.save()
        reset_code.delete()