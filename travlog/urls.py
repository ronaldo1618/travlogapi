"""travlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from travlogapi.views import register_user
from travlogapi.views import login_user
from travlogapi.views import TravelerViewSet
from travlogapi.views import Users
from travlogapi.views import TripViewSet
from travlogapi.views import DayItineraryViewSet
from travlogapi.views import ActivitysViewSet
from travlogapi.views import TransportationsViewSet
from travlogapi.views import FoodViewSet
from travlogapi.views import LodgingViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'travelers', TravelerViewSet, 'traveler')
router.register(r'users', Users, 'user')
router.register(r'trips', TripViewSet, 'trip')
router.register(r'day_itinerarys', DayItineraryViewSet, 'day_itinerary')
router.register(r'activitys', ActivitysViewSet, 'activity')
router.register(r'transportations', TransportationsViewSet, 'transportation')
router.register(r'foods', FoodViewSet, 'food')
router.register(r'lodgings', LodgingViewSet, 'lodging')

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('register/', register_user),
    path('login/', login_user)
]
