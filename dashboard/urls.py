from django.urls import path,include
from django.conf.urls.static import static
from . import views
from django.conf import settings

urlpatterns = [
    path('', views.accueil, name='accueil'),
    #path('membres/', views.Membre_list, name='liste_membres'),
]