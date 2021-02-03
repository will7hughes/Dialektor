
from django.urls import path

from .views import (
	signup, 
	login_user
)
urlpatterns = [
    path('', login_user, name='login'),
    path('signup/', signup, name='signup'),
]
