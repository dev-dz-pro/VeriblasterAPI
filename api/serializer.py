from typing_extensions import Required
from rest_framework import serializers
from .models import User, Subscription


class RegisterSerializer(serializers.ModelSerializer):
    machine_uid = serializers.UUIDField()
    username = serializers.CharField(min_length=4, max_length=30)
    password = serializers.CharField(min_length=8, max_length=30, write_only=True)
    email = serializers.EmailField(required=True)
    class Meta:
        model = User
        extra_fields = ('machine_uid',)
        fields =('email', 'username', 'password', 'machine_uid')

    def validate(self, data):
        info = data['password']
        if info.isalpha():
            raise serializers.ValidationError({'password': 'Ensure this field has at least one number'})
        elif info.isdigit():
            raise serializers.ValidationError({'password': 'Ensure this field has at least one letter'})
        elif info.islower():
            raise serializers.ValidationError({'password': 'Ensure this field has at least one letter uppercase'})
        return data

    def save(self):
        if User.objects.filter(email=self.validated_data['email']).exists():
            return None
        user = User(email=self.validated_data['email'], username=self.validated_data['username'])
        user.set_password(self.validated_data['password'])
        user.save()
        return user


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('machine_uid',)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)


class LeadsSerializer(serializers.Serializer):
    leads = serializers.ListField(child=serializers.CharField(max_length=17))


class ActivateSerializer(serializers.Serializer):
    uid = serializers.UUIDField(required=True)
    months_number = serializers.IntegerField(min_value=1, max_value=12)


class SubscriptionsSerialier(serializers.Serializer):
    subscriptions = ActivateSerializer(many=True)


class OrderLeadsSerialier(serializers.Serializer):
    machine_uid = serializers.UUIDField()

class PasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, min_length=8, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        new_pass = data["new_password"]
        if new_pass != data["confirm_password"]:
            raise serializers.ValidationError({'password': 'Not match!'})
        elif new_pass.isalpha():
            raise serializers.ValidationError({'password': 'Ensure this field has at least one number'})
        elif new_pass.isdigit():
            raise serializers.ValidationError({'password': 'Ensure this field has at least one letter'})
        elif new_pass.islower():
            raise serializers.ValidationError({'password': 'Ensure this field has at least one letter uppercase'})
        return data

class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, data): # to minimize the code
        new_pass = data["new_password"]
        if new_pass != data["confirm_password"]:
            raise serializers.ValidationError({'password': 'Not match!'})
        elif new_pass.isalpha():
            raise serializers.ValidationError({'password': 'Ensure this field has at least one number'})
        elif new_pass.isdigit():
            raise serializers.ValidationError({'password': 'Ensure this field has at least one letter'})
        elif new_pass.islower():
            raise serializers.ValidationError({'password': 'Ensure this field has at least one letter uppercase'})
        return data 