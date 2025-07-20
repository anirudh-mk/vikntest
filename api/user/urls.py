from django.urls import path
from . import views
urlpatterns = [
    path('auth-user/', views.AuthUserView.as_view())
]