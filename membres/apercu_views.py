from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .views import Generer_carte


def Apercu_carte_pdf(request, membre_id):
    # Générer le même PDF que la carte officielle,
    # sans modifier le statut de production.
    response = Generer_carte(request, membre_id, apercu=True)

    # Afficher le PDF dans le navigateur.
    response["Content-Disposition"] = "inline; filename=apercu_carte.pdf"

    return response
