from django.urls import path

from StudentQA.views import attend_ask

urlpatterns = [
    path('ask/', attend_ask)
]
