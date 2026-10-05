from django.shortcuts import render
from page1.models import Membre, Conjoint, Enfant
from datetime import date

def index(request):
    
    enfants_age_depasse = []

    for enfant in Enfant.objects.all():
        age = calculer_age(enfant.date_naissance)

        if age > 18:
            enfants_age_depasse.append({
                "enfant": enfant,
                "age": age,
            })
    aujourd_hui = date.today()

    enfants_devenus_age_depasse_ce_mois = 0

    for enfant in Enfant.objects.all():
        age = calculer_age(enfant.date_naissance)

        if age > 18:
            if (
                 enfant.date_naissance.month == aujourd_hui.month
                 and enfant.date_naissance.year + 19 == aujourd_hui.year
            ):
                 enfants_devenus_age_depasse_ce_mois += 1        
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
        "enfants_age_depasse": enfants_age_depasse,
        "enfants_devenus_age_depasse_ce_mois": enfants_devenus_age_depasse_ce_mois,
    })
def calculer_age(date_naissance):
    aujourd_hui = date.today()

    age = aujourd_hui.year - date_naissance.year

    if (aujourd_hui.month, aujourd_hui.day) < (
        date_naissance.month,
        date_naissance.day
    ):
        age -= 1

    return age