from django.urls import path

from .views import InfoDataView, FormView

urlpatterns = [
    path('', FormView.as_view(), name='info'),
    path('view/', InfoDataView.as_view(), name='info_data'),
]
