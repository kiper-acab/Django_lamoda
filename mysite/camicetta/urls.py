from .views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Main.as_view(), name='main'),
    path('category/<slug:cat_slug>/', CategoryView.as_view(), name='category'),
    path('login', login, name='login'),
    path('register', register, name='register'),
    path('thing/<slug:thing_slug>/', ThingView.as_view()),    

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)