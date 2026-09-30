from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from page1.models import Membre, Conjoint, Parent, Enfant  
from page1.forms import MembreForm
from django.contrib import messages
from PIL import Image, ImageDraw, ImageFont
import io
import requests
from io import BytesIO
from django.conf import settings
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from page1.outils import enregistrer_photo_sans_fond,rogner_zoom_visage
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from django.contrib.staticfiles import finders


@login_required
def accueil(request):

    total_membres = Membre.objects.count()
    total_conjoints = Conjoint.objects.count()
    total_enfants = Enfant.objects.count()

    membres_hommes = Membre.objects.filter(sexe='M').count()
    membres_femmes = Membre.objects.filter(sexe='F').count()

    derniers_membres = Membre.objects.order_by('-id')[:5]

    return render(request, 'index.html', {
        'total_membres': total_membres,
        'total_conjoints': total_conjoints,
        'total_enfants': total_enfants,
        'membres_hommes': membres_hommes,
        'membres_femmes': membres_femmes,
        'derniers_membres': derniers_membres,
    })