from django.http import HttpResponseServerError
from datetime import date
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from travlogapi.models import Lodging, Day_itinerary, Traveler

class LodgingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lodging
        url = serializers.HyperlinkedIdentityField(
            view_name="lodgings",
            lookup_field="id"
        )
        fields = (
          'id', 'url', 'address', 'name', 'phone_number', 'website', 'check_in', 'check_out', 'notes', 'cost'
        )
        depth = 2


class LodgingViewSet(ViewSet):

    def create(self, request):
        lodging = Lodging()
        lodging.name = request.data["name"]
        lodging.address = request.data["address"]
        lodging.phone_number = request.data['phone_number']
        lodging.website = request.data['website']
        lodging.check_in = request.data['check_in']
        lodging.check_out = request.data['check_out']
        lodging.notes = request.data['notes']
        lodging.cost = request.data['cost']
        lodging.day_itinerary = Day_itinerary.objects.get(pk=request.data['day_itinerary_id'])
        lodging.save()

        serializer = LodgingSerializer(lodging, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):

        lodging = Lodging.objects.get(pk=pk)
        lodging.name = request.data["name"]
        lodging.address = request.data["address"]
        lodging.phone_number = request.data['phone_number']
        lodging.website = request.data['website']
        lodging.check_in = request.data['check_in']
        lodging.check_out = request.data['check_out']
        lodging.notes = request.data['notes']
        lodging.cost = request.data['cost']
        lodging.day_itinerary = Day_itinerary.objects.get(pk=request.data['day_itinerary_id'])
        lodging.save()
        serializer = LodgingSerializer(lodging, context={'request': request})

        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk=None):

        try:
            lodging = Lodging.objects.get(pk=pk)
            lodging.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except lodging.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            lodging = Lodging.objects.get(pk=pk)
            serializer = LodgingSerializer(lodging, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):

        day_itinerary = self.request.query_params.get('day_itinerary', None)
        traveler = Traveler.objects.get(user=request.auth.user)
 
        lodgings = Lodging.objects.all()

        if day_itinerary is not None:
          lodgings = Lodging.objects.filter(day_itinerary=int(day_itinerary))

        serializer = LodgingSerializer(
          lodgings,
          many=True,
          context={'request': request}
        )

        return Response(serializer.data)