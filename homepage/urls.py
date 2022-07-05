from django.urls import path
from .views import HomeView,SearchResultView,AddTravelPlace,PlacesListView,RoutePageView,AddTravelFromRecomm,ListofAddedPlaces

urlpatterns=[
    path('',HomeView,name='home'),
    path('result/',SearchResultView,name="search-result"),
    path('places/<int:id>/<str:place>',AddTravelPlace,name='add-places'),
    path('addplace/<int:id>',AddTravelFromRecomm,name='add-places-recomm'),
    path('to-visit/',PlacesListView,name='list-of-places'),
    path('route/',RoutePageView,name='route-map'),
    path('saved/',ListofAddedPlaces,name='saved-places')
    
]