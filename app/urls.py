from django.urls import path
from . import views


app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('chatbot', views.chatbot, name="chatbot"),
    path('response', views.response, name="response"),
    path('refresh', views.refresh, name="refresh"),
    path('summarizer', views.summarizer, name="summarizer"),
]
