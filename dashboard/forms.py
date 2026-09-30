from django import forms
from .models import Membre

class MembreForm(forms.ModelForm):
    
    class Meta:
        model = Membre
        fields = ['nom', 'prenom', 'matricule', 'emploi', 'service', 'sexe', 'photo']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'matricule': forms.TextInput(attrs={'class': 'form-control'}),
            'emploi': forms.TextInput(attrs={'class': 'form-control'}),
            'service': forms.TextInput(attrs={'class': 'form-control'}),
            'sexe': forms.Select(attrs={'class': 'form-control'}),  # menu déroulant pour sexe
        }



class LoginForm(forms.Form):
    username = forms.CharField()
    pwd = forms.CharField()