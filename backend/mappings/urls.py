from django.urls import path
from .views import MappingView

urlpatterns = [
    path('', MappingView.as_view()),
    path('<uuid:patient_id>/', MappingView.as_view()),
]
