from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chat_page, name='chat'),
    path('api/send/', views.chat_api, name='chat_api'),
    path('api/history/', views.chat_history, name='chat_history'),
    path('api/history/<str:session_id>/', views.chat_history, name='chat_session_history'),
    path('api/debug/', views.debug_endpoint, name='debug'),
    path('test/', views.test_form, name='test_form'),
    path('api/test-fetch/', views.test_fetch, name='test_fetch'),
]