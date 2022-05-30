from django.contrib.auth.models import User
from rest_framework import serializers

from main.models import CompanyUser, Comment

from main.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    client_id = serializers.SlugRelatedField(
        slug_field='nick',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = '__all__'


class CompanyDetailSerializer(serializers.ModelSerializer):
    reviews = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = CompanyUser
        fields = '__all__'


class CompanyCreateSerializer(serializers.ModelSerializer):
    profile = UserSerializer()

    def create(self, validated_data):
        profile = User.objects.create(**validated_data['profile'])
        profile.set_password(validated_data['profile']["password"])
        profile.save()
        validated_data['profile'] = profile
        company = super(CompanyCreateSerializer, self).create(validated_data=validated_data)
        company.save()
        return company

    class Meta:
        model = CompanyUser
        exclude = ['is_company']


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyUser
        fields = ['title', 'company_country', 'pay_per_hour']
