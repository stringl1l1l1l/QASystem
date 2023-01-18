from django.urls import path

from LawQA.views import law_ask

urlpatterns = [
    path('ask/', law_ask)
]
