from django.http import HttpResponseServerError
from datetime import date
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from travlogapi.models import Trip, Traveler, Day_itinerary
from .day_itinerary import DayItinerarySerializer
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse

class TripSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Trip
        url = serializers.HyperlinkedIdentityField(
            view_name="trips",
            lookup_field="id"
        )
        fields = (
          'id', 'url', 'creator', 'creator_id', 'title',
          'description', 'start_date', 'end_date', 'is_public', 'trip_length', 'date_created', 'homepage_trip'
        )
        depth = 2


class TripViewSet(ViewSet):

    def create(self, request):
        trip = Trip()
        traveler = Traveler.objects.get(user_id=request.user.id)
        trip.creator_id = traveler.id
        trip.title = request.data["title"]
        trip.description = request.data["description"]
        trip.start_date = request.data["start_date"]
        trip.end_date = request.data["end_date"]
        trip.is_public = request.data["is_public"]
        trip.trip_length = request.data["trip_length"]
        trip.homepage_trip = request.data["homepage_trip"]
        if trip.homepage_trip:
                trips = Trip.objects.filter(creator_id=traveler.id, homepage_trip=True)
                for tripObj in trips:
                    if tripObj != trip:
                        tripObj.homepage_trip = False
                        tripObj.save()
        trip.save()

        serializer = TripSerializer(trip, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):

        traveler = Traveler.objects.get(user=request.auth.user)
        trip = Trip.objects.get(pk=pk)
        if traveler.id == trip.creator_id:
            trip.creator = traveler
            trip.title = request.data["title"]
            trip.description = request.data["description"]
            trip.start_date = request.data["start_date"]
            trip.end_date = request.data["end_date"]
            trip.is_public = request.data["is_public"]
            trip.homepage_trip = request.data["homepage_trip"]
            trip.trip_length = request.data["trip_length"]
            trip.save()
            if trip.homepage_trip:
                trips = Trip.objects.filter(creator_id=traveler.id, homepage_trip=True)
                for tripObj in trips:
                    if tripObj.id != trip.id:
                        tripObj.homepage_trip = False
                        tripObj.save()
            serializer = TripSerializer(trip, context={'request': request})
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        else:
            return JsonResponse({'valid': False})


    def destroy(self, request, pk=None):

        traveler = Traveler.objects.get(user=request.auth.user)

        try:
            trip = Trip.objects.get(pk=pk)
            trip.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Trip.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            trip = Trip.objects.get(pk=pk)
            serializer = TripSerializer(trip, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):

        traveler_trip_homepage = self.request.query_params.get('user_homepage', None)
        home_page = self.request.query_params.get('homepage', None)
        creator = self.request.query_params.get('creator', None)
        traveler = Traveler.objects.get(user=request.auth.user)

        trips = Trip.objects.all()
        # trips = Trip.objects.filter(creator_id=traveler.id)

        if creator is not None:
          trips = Trip.objects.filter(creator_id=traveler.id)
        if home_page is not None:
          trips = Trip.objects.filter(is_public = True)
        if traveler_trip_homepage is not None:
          trips = Trip.objects.filter(creator_id=traveler.id, homepage_trip=1)

        serializer = TripSerializer(
          trips,
          many=True,
          context={'request': request}
        )

        return Response(serializer.data)