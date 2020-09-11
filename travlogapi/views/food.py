from django.http import HttpResponseServerError
from datetime import date
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from travlogapi.models import Day_itinerary, Food, Traveler

class FoodSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Food
        url = serializers.HyperlinkedIdentityField(
            view_name="foods",
            lookup_field="id"
        )
        fields = (
          'id', 'url', 'address', 'name', 'notes', 'datetime', 'cost', 'day_itinerary'
        )
        depth = 2


class FoodViewSet(ViewSet):

    def create(self, request):
        food = Food()
        food.name = request.data["name"]
        food.address = request.data["address"]
        food.notes = request.data['notes']
        food.datetime = request.data['datetime']
        food.cost = request.data['cost']
        food.day_itinerary = Day_itinerary.objects.get(pk=request.data['day_itinerary_id'])
        food.save()

        serializer = FoodSerializer(food, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):

        food = Food.objects.get(pk=pk)
        food.name = request.data["name"]
        food.address = request.data["address"]
        food.notes = request.data['notes']
        food.datetime = request.data['datetime']
        food.cost = request.data['cost']
        food.day_itinerary = Day_itinerary.objects.get(pk=request.data['day_itinerary_id'])
        food.save()
        serializer = FoodSerializer(food, context={'request': request})

        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk=None):

        try:
            food = Food.objects.get(pk=pk)
            food.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except food.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            food = Food.objects.get(pk=pk)
            serializer = FoodSerializer(food, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):

        day_itinerary = self.request.query_params.get('day_itinerary', None)
        traveler = Traveler.objects.get(user=request.auth.user)
 
        foods = Food.objects.all()

        if day_itinerary is not None:
          foods = Food.objects.filter(day_itinerary=int(day_itinerary))

        serializer = FoodSerializer(
          foods,
          many=True,
          context={'request': request}
        )

        return Response(serializer.data)