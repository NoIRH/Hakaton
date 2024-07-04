"""
URL configuration for video_cupturer_web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from main_app import views
from django.contrib import admin
from users import views as user_views
from django.contrib.auth import views as auth_views
from users.views import UserLoginView, UserLogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', UserLoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path("", views.index, name ="index"),
    path("file_upload/", views.file_upload, name = "file_upload"),
    path("file_handle/", views.file_handle, name = "file_handle"),
    path("user_files/", views.user_files, name = "user_files")
]

# включаем возможность обработки картинок
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)