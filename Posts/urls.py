from django.urls import path
from Posts import views

urlpatterns = [
    path('posts/', views.PostList.as_view()),
    
    
]


