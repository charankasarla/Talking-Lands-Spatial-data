from django.urls import path
from .views import PointAPIView, PolygonAPIView

urlpatterns = [
    path('points/', PointAPIView.as_view(), name='point-api'),
    path('polygons/', PolygonAPIView.as_view(), name='polygon-api'),
]
