from rest_framework import serializers

#load django and webapp models
from django.contrib.auth.models import *
from api.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'url')

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'user', 'title', 'objid', 'farm', 'secret', 'server')

    def validate_user(self, value):
        return self.check_str(value);

    def validate_title(self, value):
        return self.check_str(value);

    def validate_farm(self, value):
        return self.check_str(value);

    def validate_secret(self, value):
        return self.check_str(value);

    def validate_server(self, value):
        return self.check_str(value);

    def check_str(self, value):
        if 'javascript' in str(value):
            raise serializers.ValidationError('Malicious content is blocked')
        elif '>' in str(value) or '<' in str(value):
            raise serializers.ValidationError('HTML is not allowed')
        return value

class UserprofileSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	class Meta:
		model = Userprofile
		fields = ('id', 'user', 'likes')
		depth = 1