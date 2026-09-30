from django.urls import path,include
from django.conf.urls.static import static
from . import views
from django.conf import settings

urlpatterns = [
    path('', views.Membre_list, name='liste_membres'),
    path('cartes/', views.Liste_cartes, name='liste_cartes'),
    path('ajouter/', views.etape1_membre, name='etape1'),
    path('etape2/', views.etape2, name='etape2'),
    path('etape3/', views.etape3, name='etape3'),
    path('etape4/', views.etape4, name='etape4'),
    path('validation/', views.validation, name='validation'),
    path('modifier/', views.Modifier_membre, name='modifier_membre'),
    path('modifier/<int:id>/', views.Modifier_membre, name='modifier_membre'),
    path('supprimer/<int:id>/', views.Supprimer_membre, name='supprimer_membre'),
    path('details/<int:membre_id>/', views.Detail_membre, name='detail_membre'),
    path('carte/<int:membre_id>/', views.Generer_carte, name='generer_carte'),
    path('carte/<int:membre_id>/apercu/', views.Apercu_carte, name='apercu_carte'),
    path(
    "exporter-cartes-excel/",
    views.Exporter_cartes_excel,
    name="exporter_cartes_excel"
    ),
    path('verify/<str:matricule>/', views.verifier_membre, name='verifier_membre'),
    path('modifier/<int:id>/parents-conjoints/',views.modifier_parents_conjoints,name='modifier_parents_conjoints'),
    path('modifier/<int:id>/enfants/',views.modifier_enfants,name='modifier_enfants'),
    path('supprimer/<int:id>/', views.Supprimer_membre, name='supprimer_membre'),
]