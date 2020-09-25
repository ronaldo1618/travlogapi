from django.http import HttpResponseServerError
from datetime import date
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from travlogapi.models import Day_itinerary, Transportation

class TransportationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transportation
        url = serializers.HyperlinkedIdentityField(
            view_name="transportations",
            lookup_field="id"
        )
        fields = (
          'id', 'url', 'name', 'notes', 'dep_datetime', 'datetime', 'day_itinerary', 'day_itinerary_id', 'cost'
        )
        depth = 2


class TransportationsViewSet(ViewSet):

    def create(self, request):
        transportation = Transportation()
        transportation.name = request.data["name"]
        transportation.notes = request.data["notes"]
        transportation.cost = request.data["cost"]
        transportation.dep_datetime = request.data['datetime']
        transportation.datetime = request.data['datetime']
        transportation.day_itinerary = Day_itinerary.objects.get(pk=int(request.data['day_itinerary_id']))
        transportation.save()

        serializer = TransportationSerializer(transportation, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):

        transportation = Transportation.objects.get(pk=pk)
        transportation.name = request.data["name"]
        transportation.notes = request.data["notes"]
        transportation.cost = request.data["cost"]
        transportation.dep_datetime = request.data['dep_datetime']
        transportation.datetime = request.data['datetime']
        transportation.day_itinerary = Day_itinerary.objects.get(pk=request.data['day_itinerary_id'])
        transportation.save()
        serializer = TransportationSerializer(transportation, context={'request': request})

        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk=None):

        try:
            transportation = Transportation.objects.get(pk=pk)
            transportation.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except transportation.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            transportation = Transportation.objects.get(pk=pk)
            serializer = TransportationSerializer(transportation, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):

        day_itinerary = self.request.query_params.get('day_itinerary', None)
        transportations = Transportation.objects.all()

        if day_itinerary is not None:
          transportations = Transportation.objects.filter(day_itinerary=int(day_itinerary))

        serializer = TransportationSerializer(
          transportations,
          many=True,
          context={'request': request}
        )

        return Response(serializer.data)