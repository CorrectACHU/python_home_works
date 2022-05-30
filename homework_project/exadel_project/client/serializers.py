from django.contrib.auth.models import User
from rest_framework import serializers

from main.models import ClientUser, Comment, CompanyUser

from main.serializers import UserSerializer


class ClientDetailSerializer(serializers.ModelSerializer):
    profile = UserSerializer()

    def create(self, validated_data):
        profile = User.objects.create(**validated_data['profile'])
        profile.set_password(validated_data['profile']["password"])
        profile.save()
        validated_data['profile'] = profile
        client = super(ClientDetailSerializer, self).create(validated_data=validated_data)
        client.save()
        return client

    class Meta:
        model = ClientUser
        exclude = ['is_client']


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientUser
        fields = ['profile']


class CreateReviewSerializer(serializers.ModelSerializer):
    client_id = serializers.PrimaryKeyRelatedField(queryset=ClientUser.objects.all())
    company_id = serializers.PrimaryKeyRelatedField(queryset=CompanyUser.objects.all())

    class Meta:
        model = Comment
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    # client_id = serializers.SlugRelatedField(slug_field='profile',read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
