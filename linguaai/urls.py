"""LinguaAI URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('lessons/', views.lessons, name='lessons'),
    path('practice/', views.practice, name='practice'),
    path('profile/', views.profile, name='profile'),
    path('api/chat/', views.chat_api, name='chat_api'),
    path('api/progress/', views.progress_api, name='progress_api'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)