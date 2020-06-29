"""trydjango22 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from posts.views import posts_list,posts_delete,posts_detail,posts_update,posts_create#posts_home
urlpatterns = [
    path('admin/', admin.site.urls),
    #path('',posts_home,name='home-page'),
    path('',posts_list,name='home-list'),
    path('create/',posts_create,name='post-create'),
    path('<int:id>/',posts_detail,name='post-detail'),
    path('<int:id>/edit/',posts_update,name='post-update'),
    path('<int:id>/delete/',posts_delete,name='post-delete'),
]

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)