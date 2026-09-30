from django import forms
from django.forms import inlineformset_factory

from .models import (
    Membre,
    Conjoint,
    Enfant,
    Parent
)


# =========================================================
# FORMULAIRE MEMBRE
# =========================================================
# =========================================================
# FORMULAIRE MEMBRE
# =========================================================

class MembreForm(forms.ModelForm):

    class Meta:
        model = Membre

        fields = [
            'nom',
            'prenom',
            'matricule',
            'emploi',
            'service',
            'sexe',
            'photo'
        ]

        widgets = {

            'nom': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'prenom': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'matricule': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'emploi': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'service': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'sexe': forms.Select(attrs={
                'class': 'form-control'
            }),

            'photo': forms.ClearableFileInput(attrs={
                 'class': 'form-control'
            }),

        }


# =========================================================
# FORMULAIRE PHOTO
# =========================================================

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Membre
        fields = ['photo']
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

        widgets = {

            'nom': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'prenom': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'matricule': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'emploi': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'service': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'sexe': forms.Select(attrs={
                'class': 'form-control'
            }),

            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),

        }


# =========================================================
# LOGIN
# =========================================================
class LoginForm(forms.Form):

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    pwd = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )


# =========================================================
# FORMULAIRE CONJOINT
# =========================================================
class ConjointForm(forms.ModelForm):

    class Meta:
        model = Conjoint

        fields = ['nom', 'prenom']

        widgets = {

            'nom': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'prenom': forms.TextInput(attrs={
                'class': 'form-control'
            }),

        }


# =========================================================
# FORMSET CONJOINTS (MAX 4)
# =========================================================
ConjointFormSet = inlineformset_factory(

    Membre,
    Conjoint,

    form=ConjointForm,

    extra=1,

    max_num=4,

    validate_max=True,

    can_delete=True
)




# =========================================================
# FORMULAIRE ENFANT
# =========================================================
class EnfantForm(forms.ModelForm):

    class Meta:
        model = Enfant

        fields = [
            'nom',
            'prenom',
            'date_naissance'
        ]

        widgets = {

            'nom': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'prenom': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'date_naissance': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

        }


# =========================================================
# FORMSET ENFANTS (MAX 9)
# =========================================================
EnfantFormSet = inlineformset_factory(

    Membre,
    Enfant,

    form=EnfantForm,

    extra=1,

    max_num=9,

    validate_max=True,

    can_delete=True
)


# =========================================================
# FORMULAIRE PARENTS
# =========================================================
class ParentForm(forms.ModelForm):

    class Meta:
        model = Parent

        fields = [
            'type_parent',
            'nom',
            'prenom'
        ]

        widgets = {

            'type_parent': forms.Select(attrs={
                'class': 'form-control'
            }),

            'nom': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'prenom': forms.TextInput(attrs={
                'class': 'form-control'
            }),

        }
        
        
        
# =========================================================
# FORMSET PARENTS (MAX 2)
# =========================================================

ParentFormSet = inlineformset_factory(

    Membre,
    Parent,

    form=ParentForm,

    extra=1,

    max_num=2,

    validate_max=True,

    can_delete=True
)