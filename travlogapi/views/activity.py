from django.http import HttpResponseServerError
from datetime import date
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from travlogapi.models import Day_itinerary, Activity

class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Activity
        url = serializers.HyperlinkedIdentityField(
            view_name="activitys",
            lookup_field="id"
        )
        fields = (
          'id', 'url', 'address', 'name', 'notes', 'cost', 'datetime', 'day_itinerary', 'day_itinerary_id'
        )
        depth = 2


class ActivitysViewSet(ViewSet):

    def create(self, request):
        activity = Activity()
        activity.name = request.data["name"]
        activity.address = request.data["address"]
        activity.notes = request.data['notes']
        activity.datetime = request.data['datetime']
        activity.cost = request.data['cost']
        activity.day_itinerary = Day_itinerary.objects.get(pk=request.data['day_itinerary_id'])
        activity.save()

        serializer = ActivitySerializer(activity, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):

        activity = Activity.objects.get(pk=pk)
        activity.name = request.data["name"]
        activity.address = request.data["address"]
        activity.notes = request.data['notes']
        activity.datetime = request.data['datetime']
        activity.cost = request.data['cost']
        activity.day_itinerary = Day_itinerary.objects.get(pk=request.data['day_itinerary_id'])
        activity.save()
        serializer = ActivitySerializer(activity, context={'request': request})

        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk=None):

        try:
            activity = Activity.objects.get(pk=pk)
            activity.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except activity.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            activity = Activity.objects.get(pk=pk)
            serializer = ActivitySerializer(activity, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):

        day_itinerary = self.request.query_params.get('day_itinerary', None)
 
        activitys = Activity.objects.all()

        if day_itinerary is not None:
          activitys = Activity.objects.filter(day_itinerary=int(day_itinerary))

        serializer = ActivitySerializer(
          activitys,
          many=True,
          context={'request': request}
        )

        return Response(serializer.data)