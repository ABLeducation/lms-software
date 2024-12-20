"""
URL configuration for lms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include
from rest_framework import permissions # type: ignore
from drf_yasg.views import get_schema_view # type: ignore
from drf_yasg import openapi # type: ignore
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls

schema_view = get_schema_view(
    openapi.Info(
        title="LMS Backend Endpoint",
        default_version='v1',
        description="Backend API documentation",
    ),
    public=True,
    url='https://credible-becoming-spider.ngrok-free.app',
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('user.urls', 'user'), namespace='users')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('curriculum/', include(('curriculum.urls','curriculum'), namespace='curriculum')),
    path('quiz/', include(('quiz.urls','quiz'), namespace='quiz')),
    path(r'docs/', include_docs_urls(title='LMS API')),
] 

urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)