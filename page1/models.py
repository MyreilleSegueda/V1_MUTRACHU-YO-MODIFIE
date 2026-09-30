from django.db import models
from django.core.exceptions import ValidationError

from django.db import models
from django.core.exceptions import ValidationError

class Membre(models.Model):

    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Feminin'),
    ]

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=500)
    matricule = models.CharField(max_length=50, unique=True)

    emploi = models.CharField(max_length=100)
    service = models.CharField(max_length=100)

    photo = models.ImageField(upload_to='photos/', blank=True, null=True)

    cle = models.CharField(max_length=1, default='A')

    sexe = models.CharField(
        max_length=1,
        choices=SEXE_CHOICES,
        default='M'
    )

    date_naissance = models.DateField(
        null=True,
        blank=True
    )

    # 🔥 Compteur automatique
    compteur = models.PositiveIntegerField(
        unique=True,
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):

        # 🔥 Génération automatique du compteur
        if not self.compteur:

            dernier = Membre.objects.order_by('-compteur').first()

            if dernier and dernier.compteur:
                self.compteur = dernier.compteur + 1
            else:
                self.compteur = 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Conjoint(models.Model):
    membre = models.ForeignKey(
        Membre,
        on_delete=models.CASCADE,
        related_name='conjoints'
    )

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)

    def clean(self):
        if self.membre.conjoints.count() >= 4 and not self.pk:
            raise ValidationError("Un membre ne peut pas avoir plus de 4 conjoints.")

    def __str__(self):
        return f"{self.prenom} {self.nom}"    

#class Enfant(models.Model):
#    membre = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name='enfants')

#    nom = models.CharField(max_length=100)
#    prenom = models.CharField(max_length=100)
#    date_naissance = models.DateField()

#    def __str__(self):
#        return f"{self.prenom} {self.nom}"

class Enfant(models.Model):
    membre = models.ForeignKey(
        Membre,
        on_delete=models.CASCADE,
        related_name='enfants'
    )

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()

    def clean(self):
        if self.membre.enfants.count() >= 9 and not self.pk:
            raise ValidationError("Un membre ne peut pas avoir plus de 9 enfants.")

    def __str__(self):
        return f"{self.prenom} {self.nom}"    

class Parent(models.Model):
    TYPE_PARENT = [
        ('P', 'Père'),
        ('M', 'Mère'),
    ]

    membre = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name='parents')

    type_parent = models.CharField(max_length=1, choices=TYPE_PARENT)

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.get_type_parent_display()} : {self.prenom} {self.nom}"



