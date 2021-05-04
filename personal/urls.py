
from django.urls import path

from .views import (
	index_home,
	signup, 
	login_user,
	create_user,
)
urlpatterns = [
    path('', index_home, name='home'),
    path('signup/', signup, name='signup'),
    path('signup/create_user', create_user, name='create_user'),
]
