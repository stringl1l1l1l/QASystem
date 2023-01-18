"""QASystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, re_path
from django.conf.urls import url, include
from rest_framework import routers

import LoginSystem
import StudentQA
from LoginSystem import views
from rest_framework.documentation import include_docs_urls

from rest_framework import permissions
from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi

router = routers.DefaultRouter()
schema_view = get_schema_view(
    openapi.Info(
        title="QASystem",
        default_version='v1',
        description="QASystem后端接口文档",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
# 这里结束

# 使用自动URL路由连接我们的API。
# 另外，我们还包括支持浏览器浏览API的登录URL。
urlpatterns = [
    re_path(r'^doc(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path("login/", LoginSystem.views.login),
    path("logout/", LoginSystem.views.logout),
    path("register/", LoginSystem.views.register),
    path('student/', include('StudentQA.urls')),
    path('law/', include('LawQA.urls'))
]
