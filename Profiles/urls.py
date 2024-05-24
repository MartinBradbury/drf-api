from django.urls import path
from Profiles import views

urlpatterns = [
    path('profiles/', views.ProfileList.as_view()),
]


