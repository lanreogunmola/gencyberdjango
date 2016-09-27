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

class Session(APIView):
	permission_classes = (AllowAny,)
	def form_response(self, isauthenticated, userid, username, error=""):
		data = {
			'isauthenticated': isauthenticated,
			'userid': userid,
			'username': username
		}
		if error:
			data['message'] = error

		return Response(data)

	def get(self, request, *args, **kwargs):
		# Get the current user
		if request.user.is_authenticated():
			return self.form_response(True, request.user.id, request.user.username)
		return self.form_response(False, None, None)

	def post(self, request, *args, **kwargs):
		# Login
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return self.form_response(True, user.id, user.username)
			return self.form_response(False, None, None, "Account is suspended")
		return self.form_response(False, None, None, "Invalid username or password")

	def delete(self, request, *args, **kwargs):
		# Logout
		logout(request)
		return Response(status=status.HTTP_204_NO_CONTENT)

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
			if serializer.validated_data['user'] == request.user:
				serializer.save()
				print str(serializer.data)
				profile, created = Userprofile.objects.get_or_create(user__id=int(serializer.data['user']))
				profile.likes.add(serializer.data['id'])
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			else:
				return Response('Not authorized')
		else:
			return Response(serializer.errors)

	def list(self, request):
		likes = Like.objects.filter(user=request.user)
		serializer = LikeSerializer(likes, many=True, context={'request': request})
		return Response(serializer.data)

	def retrieve(self, request, pk):
		like = get_object_or_404(Like, id=pk,user=request.user)
		serializer = LikeSerializer(like, context={'request': request})
		return Response(serializer.data)

class UserprofileViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewed.
	"""
	queryset = Userprofile.objects.all()
	serializer_class = UserprofileSerializer