from django.http import HttpResponseServerError
from datetime import date
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from travlogapi.models import Day_itinerary, Traveler, Trip

class DayItinerarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Day_itinerary
        url = serializers.HyperlinkedIdentityField(
            view_name="day_itinerarys",
            lookup_field="id"
        )
        fields = (
          'id', 'url', 'description', 'name', 'trip'
        )
        depth = 2


class DayItineraryViewSet(ViewSet):

    def create(self, request):
        day_itinerary = Day_itinerary()
        day_itinerary.name = request.data["name"]
        day_itinerary.description = request.data["description"]
        day_itinerary.trip_id = request.data['trip_id']
        day_itinerary.save()

        serializer = DayItinerarySerializer(day_itinerary, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):

        day_itinerary = Day_itinerary.objects.get(pk=pk)
        day_itinerary.name = request.data["name"]
        day_itinerary.description = request.data["description"]
        day_itinerary.trip_id = request.data['trip_id']
        day_itinerary.save()
        serializer = DayItinerarySerializer(day_itinerary, context={'request': request})

        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk=None):

        try:
            day_itinerary = Day_itinerary.objects.get(pk=pk)
            day_itinerary.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except day_itinerary.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            day_itinerary = Day_itinerary.objects.get(pk=pk)
            serializer = DayItinerarySerializer(day_itinerary, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):

        trip = self.request.query_params.get('trip', None)
        traveler = Traveler.objects.get(user=request.auth.user)

        day_itinerarys = Day_itinerary.objects.all()

        if trip is not None:
          day_itinerarys = Day_itinerary.objects.filter(trip_id=int(trip))

        serializer = DayItinerarySerializer(
          day_itinerarys,
          many=True,
          context={'request': request}
        )

        return Response(serializer.data)