# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.conf.urls.static import static
import personal.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('personal.urls')),
	
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.index_home, name='home'),
    path('signup/', views.signup),
    path('signup/create_user', views.create_user),
    path('upload', views.upload),
    path('sounds/<str:sound_id>/', views.render_sound, name='render_sound'),
    path('pic/<str:pic_id>/', views.get_picture, name="get pic"),
    path('raw/<str:sound_id>/', views.get_sound, name="get_sound"),
    path('download/<str:sound_id>/', views.download_sound, name="download_sound"),
    path('profile/',views.profile, name="profile"),
    path('userUpdateProfile/', views.profile_update, name="profile_update"),
    path('changePassword/', views.change_pass, name="change_pass"),
    path('collection/<str:collection_name>/', views.collection_list, name="collection_list"),
    path('tag/<str:tag_name>/', views.tag_list, name="tag_list"),
    path('profilePic/', views.get_profile_pic, name="get_profile_pic"),

    path('collections', views.get_collections, name="get_collections"),

    path('search', views.search, name="search")
]

# Only serve static files from Django during development
# Use Google Cloud Storage or an alternative CDN for production
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
