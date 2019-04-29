"""owska URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

try:
    from .settings import OWSKA_ADMIN_PATH
except ImportError:
    OWSKA_ADMIN_PATH = 'admin/'

if len(OWSKA_ADMIN_PATH) != 0:
    admin_prefix = '%s/' % OWSKA_ADMIN_PATH
else:
    admin_prefix = '%s/' % 'admin'

urlpatterns = [
    path(admin_prefix, admin.site.urls),
    path('users/', include("users.urls")),
    path('users/', include('django.contrib.auth.urls')),
    path('', include('forum.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
