
from django.urls import path

from . import views
from .views import signup, login_user

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', signup, name='signup'),
	path('login/', login_user, name='login'),
]
