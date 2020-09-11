from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Traveler
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        url = serializers.HyperlinkedIdentityField(
            view_name='user',
            lookup_field='id'
        )
        fields = ('id', 'url', 'username', 'first_name', 'last_name', 'email',)


class Users(ViewSet):
    def retrieve(self, request, pk=None):
        '''
        Handling a GET request for a traveler/user
        Returns -- JSON serialized traveler instance
        '''
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user,
            context = {'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        '''
        Handling a FETCH request for a traveler/user
        Returns -- JSON serialized list of traveler instances
        '''
        user = Traveler.objects.filter(user=request.auth.user)

        serializer = UserSerializer(
            user, many = True, context={'request':request})

        return Response(serializer.data)


class TravelerSerializer(serializers.HyperlinkedModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Traveler
        url = serializers.HyperlinkedIdentityField(
            view_name = 'traveler',
            lookup_field = 'id'
        )
        fields = ('id', 'url', 'user', 'bio')
        depth = 2


class TravelerViewSet(ViewSet):
    def update(self, request, pk=None):
        '''
        Handling a PUT request for a traveler/user
        Returns -- Empty body with 204 status code
        '''
        traveler = Traveler.objects.get(pk=pk)
        traveler.bio = request.data['bio']
        traveler.save()

        user = User.objects.get(pk=traveler.user.id)
        user.first_name = request.data['first_name']
        user.last_name = request.data['last_name']
        user.username = request.data['username']
        user.email = request.data['email']
        user.password = make_password(request.data['password'])
        user.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):
        '''
        Handling a GET request for a traveler/user
        Returns -- JSON serialized traveler instance
        '''
        try:
            traveler = Traveler.objects.get(pk=pk)
            serializer = TravelerSerializer(traveler, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        '''
        Handling a FETCH request for a traveler/user
        Returns -- JSON serialized list of traveler instances
        '''

        traveler = Traveler.objects.filter(user=request.auth.user)
        serializer = TravelerSerializer(traveler, many=True, context={'request': request})
        return Response(serializer.data)