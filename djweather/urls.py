from django.urls import path
from . import views
from .views import city_detail_view

urlpatterns = [
    path('', views.index ),
    path('<int:id>/', city_detail_view, name='city-detail')
]