from .views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', Main.as_view(), name='main'),
    path('category/<slug:cat_slug>/', CategoryView.as_view(), name='category'),
    path('login', LoginUser.as_view(), name='login'),
    path('register', RegisterUser.as_view(), name='register'),
    path('thing/<slug:thing_slug>/', ThingView.as_view()),    
    path('logout', logout_user, name='logout'),
    path('profile', profile, name='profile'),
    path('basket', bakset, name='basket'),
    path('basket/add/<slug:thing_slug>/<int:size>', add_to_basket, name='add_to_basket'),
    path('basket/update/<int:basket_id>/<str:action>/', basket_update, name='basket_update'),
    path('basket/clean', clean_basket, name='clean_basket'),
    path('formalization', formalization, name='formalization'),
    path('settings', profile_settings, name='settings')
    


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)