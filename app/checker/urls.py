from django.urls import path

from .views import InfoDataView, InfoView

urlpatterns = [
    path('', InfoView.as_view(), name="info"),
    path('view/', InfoDataView.as_view(), name="info_data"),
]
