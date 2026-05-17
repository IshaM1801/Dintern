from django.urls import path
from .views import DoctorView

urlpatterns = [
    path('', DoctorView.as_view()),
    path('<uuid:id>/', DoctorView.as_view()),
]
