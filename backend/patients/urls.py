from django.urls import path
from .views import PatientView

urlpatterns = [
    path('', PatientView.as_view()),
    path('<uuid:id>/', PatientView.as_view()),
]
