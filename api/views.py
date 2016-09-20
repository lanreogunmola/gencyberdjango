from django.shortcuts import *

# Import models
from django.db import models
from django.contrib.auth.models import *
from api.models import *

#REST API
from rest_framework import viewsets
from api.serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import *
from rest_framework.decorators import *

def home(request):
	"""
	Send request to the ember.js clientside app """

	return render_to_response('index.html', {}, RequestContext(request))

class UserViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewed.
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer

class LikeViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewed.
	"""
	queryset = Like.objects.all()
	serializer_class = LikeSerializer

	def create(self, request):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			print str(serializer.data)
			profile, created = Userprofile.objects.get_or_create(user__id=int(serializer.data['user']))
			profile.likes.add(serializer.data['id'])
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors)

class UserprofileViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewed.
	"""
	queryset = Userprofile.objects.all()
	serializer_class = UserprofileSerializer