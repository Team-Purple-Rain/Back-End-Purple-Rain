"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from thatguide import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', views.getMeme),
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('map/', views.HikingSessionView.as_view()),
    path('map/<int:pk>/', views.HikingSessionViewList.as_view()),
    path('map/<int:pk>/checkpoint/', views.HikingCheckPointPostView.as_view()),
    path('map/<int:pk>/<checkpoint_pk>/', views.HikingCheckPointView.as_view()),
    path('users/', views.UserProfileView.as_view()),
    path('users/me/', views.UserEditView.as_view()),
    path('users/me/map/', views.UserHikingSessionView.as_view()),
]
