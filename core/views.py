from django.shortcuts import render
from page1.models import Membre, Conjoint, Enfant


def index(request):
    total_membres = Membre.objects.count()
    total_conjoints = Conjoint.objects.count()
    total_enfants = Enfant.objects.count()

    membres_hommes = Membre.objects.filter(sexe='M').count()
    membres_femmes = Membre.objects.filter(sexe='F').count()

    # Pourcentage de femmes
    if total_membres > 0:
        pourcentage_femmes = round(
            (membres_femmes / total_membres) * 100
        )
    else:
        pourcentage_femmes = 0

    # 5 derniers membres
    derniers_membres = Membre.objects.order_by('-id')[:5]

    return render(request, 'core/index.html', {
        'total_membres': total_membres,
        'total_conjoints': total_conjoints,
        'total_enfants': total_enfants,
        'membres_hommes': membres_hommes,
        'membres_femmes': membres_femmes,
        'pourcentage_femmes': pourcentage_femmes,
        'derniers_membres': derniers_membres,
    })