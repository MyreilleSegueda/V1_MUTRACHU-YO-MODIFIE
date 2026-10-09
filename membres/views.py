from page1.models import Membre, Conjoint, Parent,Carte  
from page1.forms import (
    MembreForm,
    PhotoForm,
    ConjointFormSet,
    ParentForm,
    EnfantFormSet,
    ParentFormSet
)
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from openpyxl import Workbook
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
import qrcode
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.utils import simpleSplit
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.enums import TA_RIGHT
from django.db.models import Q
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone


# Affichage de la liste des membres


from django.core.paginator import Paginator
from django.db.models import Q

def Membre_list(request):

    membres = Membre.objects.all().order_by("nom", "prenom")

    search = request.GET.get("search", "").strip()

    if search:
        membres = membres.filter(
            Q(nom__icontains=search) |
            Q(prenom__icontains=search) |
            Q(matricule__icontains=search)
        )

    # Nombre total de membres correspondant à la recherche
    total_membres = membres.count()

    # 10 membres par page
    paginator = Paginator(membres, 10)

    # Page demandée dans l'URL
    page_number = request.GET.get("page")

    membres = paginator.get_page(page_number)

    return render(request, "Membre_list_refais.html", {
        "membres": membres,
        "search": search,
        "total_membres": total_membres,
    })

def Liste_cartes(request):

    recherche = request.GET.get("recherche", "").strip()

    membres = Membre.objects.all().order_by("nom", "prenom")

    # Recherche
    if recherche:
        membres = membres.filter(
            Q(nom__icontains=recherche) |
            Q(prenom__icontains=recherche) |
            Q(matricule__icontains=recherche) |
            Q(compteur__icontains=recherche)
        )

    # Pagination : 10 membres par page
    paginator = Paginator(membres, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "liste_cartes.html", {
        "membres": page_obj,
        "page_obj": page_obj,
        "recherche": recherche,
        "onglet_actif": "toutes",
    })
def Cartes_produites(request):

    cartes = Carte.objects.filter(
        statut='PRODUITE'
    ).select_related('membre').order_by(
        'membre__nom',
        'membre__prenom'
    )

    return render(request, "liste_cartes.html", {
        "membres": [carte.membre for carte in cartes],
        "cartes_produites": True,
        "onglet_actif": "produites",
    })
def Exporter_cartes_excel(request):

    membres = Membre.objects.all().order_by("nom", "prenom")

    workbook = Workbook()
    feuille = workbook.active
    feuille.title = "Cartes membres"

    feuille.append([
        "N° d'ordre",
        "Membre",
        "N° carte"
    ])

    for index, membre in enumerate(membres, start=1):

        feuille.append([
            index,
            f"{membre.nom} {membre.prenom}",
            f"{membre.compteur:04d}"
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = (
        'attachment; filename="cartes_membres.xlsx"'
    )

    workbook.save(response)

    return response
def verifier_matricule(request):
    matricule = request.GET.get('matricule', '').strip()

    existe = Membre.objects.filter(matricule=matricule).exists()

    return JsonResponse({
        'existe': existe
    })
#Ajouter les membres
def etape1_membre(request):
    if request.method == "POST":
        form = MembreForm(request.POST)

        if form.is_valid():
            membre = form.save()

            # Stocker l'id du membre pour les étapes suivantes
            request.session['membre_id'] = membre.id

            messages.success(request, "Étape 1 validée ✅")

            return redirect('etape2')

    else:
        form = MembreForm()

    return render(request, 'page1/enrolement/etape1_refonte.html', {
        'form': form
    })
#Ajout des conjoint et parents des memebres
def etape2(request):

    # 🔐 Sécurité
    membre_id = request.session.get('membre_id')

    if not membre_id:
        return redirect('etape1')

    membre = Membre.objects.get(id=membre_id)

    # =====================================================
    # FORMULAIRES
    # =====================================================

    conjoint_formset = ConjointFormSet(
        request.POST or None,
        instance=membre,
        prefix='conjoint'
    )

    parent_pere_form = ParentForm(
        request.POST or None,
        prefix='pere'
    )

    parent_mere_form = ParentForm(
        request.POST or None,
        prefix='mere'
    )

    # =====================================================
    # TRAITEMENT POST
    # =====================================================

    if request.method == 'POST':

        # 🔹 Validation des conjoints
        if conjoint_formset.is_valid():

            conjoint_formset.save()

        # =================================================
        # PÈRE
        # =================================================

        nom_pere = request.POST.get('pere-nom')

        prenom_pere = request.POST.get('pere-prenom')

        if nom_pere or prenom_pere:

            Parent.objects.update_or_create(

                membre=membre,

                type_parent='P',

                defaults={

                    'nom': nom_pere or '',

                    'prenom': prenom_pere or ''

                }

            )

        # =================================================
        # MÈRE
        # =================================================

        nom_mere = request.POST.get('mere-nom')

        prenom_mere = request.POST.get('mere-prenom')

        if nom_mere or prenom_mere:

            Parent.objects.update_or_create(

                membre=membre,

                type_parent='M',

                defaults={

                    'nom': nom_mere or '',

                    'prenom': prenom_mere or ''

                }

            )

        # 🔹 Redirection étape suivante
        return redirect('etape3')

    # =====================================================
    # AFFICHAGE PAGE
    # =====================================================

    return render(request, 'page1/enrolement/etape2_refonte.html', {

        'conjoint_formset': conjoint_formset,

        'parent_pere_form': parent_pere_form,

        'parent_mere_form': parent_mere_form

    })
#ajout des enfantsdu membres

def etape3(request):
    membre_id = request.session.get('membre_id')

    if not membre_id:
        return redirect('etape1')

    membre = get_object_or_404(Membre, id=membre_id)

    formset = EnfantFormSet(
        request.POST or None,
        instance=membre,
        prefix='enfant'
    )

    if request.method == 'POST':
        if formset.is_valid():
            formset.save()

            # On garde membre_id en session
            # car il sera encore utilisé aux étapes 4 et 5

            return redirect('etape4')

    return render(request, 'page1/enrolement/etape3_refonte.html', {
        'formset': formset,
        'membre': membre
    })
def etape4(request):
    membre_id = request.session.get('membre_id')

    if not membre_id:
        return redirect('etape1')

    membre = get_object_or_404(Membre, id=membre_id)

    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES, instance=membre)

        if form.is_valid():
            membre = form.save()

            # Traitement de la photo
            if 'photo' in request.FILES:
                enregistrer_photo_sans_fond(
                    membre,
                    request.FILES['photo'],
                    background_color=(255, 255, 255)
                )

                rogner_zoom_visage(membre, membre.photo)

            messages.success(request, "Photo enregistrée ✅")

            return redirect('validation')

    else:
        form = PhotoForm(instance=membre)

    return render(request, 'page1/enrolement/etape4_refonte.html', {
        'form': form,
        'membre': membre
    })
def validation(request):
    membre_id = request.session.get('membre_id')

    if not membre_id:
        return redirect('etape1')

    membre = get_object_or_404(Membre, id=membre_id)

    if request.method == 'POST':
        messages.success(
            request,
            "Membre enrôlé avec succès ✅"
        )

        # Fin de l'enrôlement
        del request.session['membre_id']

        return redirect('liste_membres')

    return render(request, 'page1/enrolement/validation_refonte.html', {
        'membre': membre
    })
#Modifier un membres
def Modifier_membre(request, id):

    membre = get_object_or_404(Membre, id=id)

    if request.method == "POST":

        form = MembreForm(
            request.POST,
            request.FILES,
            instance=membre
        )

        if form.is_valid():

            membre = form.save(commit=False)

            # 🔥 Nouvelle photo
            if 'photo' in request.FILES:

                enregistrer_photo_sans_fond(
                    membre,
                    request.FILES['photo'],
                    background_color=(255, 255, 255)
                )

                rogner_zoom_visage(
                    membre,
                    membre.photo
                )

            membre.save()

            # 🔥 Aller étape suivante
            return redirect(
                'modifier_parents_conjoints',
                id=membre.id
            )

    else:

        form = MembreForm(instance=membre)

    return render(request, 'modifier_membre.html', {

        'form': form,
        'membre': membre,
        'step': 1

    })

#Modifier un parents +conjoints






def modifier_parents_conjoints(request, id):

    membre = get_object_or_404(Membre, id=id)

    # =====================================================
    # RÉCUPÉRER LE PÈRE ET LA MÈRE EXISTANTS
    # =====================================================

    pere = membre.parents.filter(type_parent='P').first()
    mere = membre.parents.filter(type_parent='M').first()

    # =====================================================
    # POST
    # =====================================================

    if request.method == 'POST':

        pere_form = ParentForm(
            request.POST,
            instance=pere,
            prefix='pere'
        )

        mere_form = ParentForm(
            request.POST,
            instance=mere,
            prefix='mere'
        )

        conjoint_formset = ConjointFormSet(
            request.POST,
            instance=membre
        )

        if (
            pere_form.is_valid()
            and mere_form.is_valid()
            and conjoint_formset.is_valid()
        ):

            # =================================================
            # PÈRE
            # =================================================

            pere_obj = pere_form.save(commit=False)

            if pere_obj.nom or pere_obj.prenom:
                pere_obj.membre = membre
                pere_obj.type_parent = 'P'
                pere_obj.save()

            # =================================================
            # MÈRE
            # =================================================

            mere_obj = mere_form.save(commit=False)

            if mere_obj.nom or mere_obj.prenom:
                mere_obj.membre = membre
                mere_obj.type_parent = 'M'
                mere_obj.save()

            # =================================================
            # CONJOINTS
            # =================================================

            conjoints = conjoint_formset.save(commit=False)

            for conjoint in conjoints:
                conjoint.membre = membre
                conjoint.save()

            for obj in conjoint_formset.deleted_objects:
                obj.delete()

            return redirect(
                'modifier_enfants',
                id=membre.id
            )

    # =====================================================
    # AFFICHAGE INITIAL
    # =====================================================

    else:

        pere_form = ParentForm(
            instance=pere,
            prefix='pere',
            initial={
                'type_parent': 'P'
            } if not pere else None
        )

        mere_form = ParentForm(
            instance=mere,
            prefix='mere',
            initial={
                'type_parent': 'M'
            } if not mere else None
        )

        conjoint_formset = ConjointFormSet(
            instance=membre
        )

    # =====================================================
    # AFFICHAGE
    # =====================================================

    return render(
        request,
        'modifier_parents_conjoints.html',
        {
            'membre': membre,

            'pere_form': pere_form,
            'mere_form': mere_form,

            'conjoint_formset': conjoint_formset,

            'step': 2
        }
    )
#modifier les enfants
def modifier_enfants(request, id):

    membre = get_object_or_404(Membre, id=id)

    if request.method == 'POST':

        enfant_formset = EnfantFormSet(
            request.POST,
            instance=membre
        )

        if enfant_formset.is_valid():

            enfants = enfant_formset.save(commit=False)

            for enfant in enfants:

                enfant.membre = membre
                enfant.save()

            for obj in enfant_formset.deleted_objects:
                obj.delete()

            messages.success(
                request,
                "Profil complet modifié avec succès ✅"
            )

            return redirect('liste_membres')

    else:

        enfant_formset = EnfantFormSet(
            instance=membre
        )

    return render(
        request,
        'modifier_parents_enfants.html',
        {

            'membre': membre,

            'enfant_formset': enfant_formset,

            'step': 3
        }
    )

#supprimer un membre

def Supprimer_membre(request, id):
    membre = get_object_or_404(Membre, id=id)
    if request.method == "POST":
        membre.delete()
        messages.success(request, "Membre supprimé avec succès ! ✅")
        return redirect('liste_membres')  # Redirige vers la liste après suppression
    return render(request, 'supprimer_membre.html', {'membre': membre})

#details des membres

def Detail_membre(request, membre_id):
    membre = get_object_or_404(Membre, id=membre_id)
    return render(request, 'detail_membre.html', {'membre': membre})


#Generation de la carte recto-verso
def Generer_carte(request, membre_id,apercu=False):
    membre = get_object_or_404(Membre, id=membre_id)

    # Dimensions carte PVC
    largeur = 85.6 * 72 / 25.4
    hauteur = 53.98 * 72 / 25.4

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=(largeur, hauteur))

    # ===================== RECTO =====================

    # Fond recto
    maquette_recto = finders.find('images/Maquette.jpg')
    if maquette_recto:
        c.drawImage(ImageReader(maquette_recto), 0, 0, width=largeur, height=hauteur)

    # Police
    font_path = finders.find('fonts/SourceSansPro-Bold.ttf')
    pdfmetrics.registerFont(TTFont('OpenSans', font_path))
    c.setFont("OpenSans", 8)

    # Coordonnées
    x_label = 6
    x_value = 46
    y = hauteur - 59
    step = 10
    c.setFont("Helvetica-Bold", 7)

    c.drawString(
        143,
        y + 11,
        f"N : {membre.compteur:04d}"
    )
    # Infos membre
   


    # ===================== INFOS MEMBRE =====================
    
    c.drawString(x_label, y, "Nom:")
    c.setFillColorRGB(0, 0, 0)
    c.drawString(x_value, y, membre.nom.upper())
    
    # ===================== PRENOMS =====================
    y -= step
    
    c.drawString(x_label, y, "Prénom(s):")
    
    prenom_lines = simpleSplit(
        membre.prenom,
        "Helvetica-Bold",
        7,
        70
    )
    
    for line in prenom_lines:
        c.drawString(x_value, y, line)
        y -= 7
    
    
    # ===================== SEXE =====================
    c.drawString(x_label, y, "Sexe:")
    c.drawString(x_value, y, membre.sexe)
    
    # ===================== MATRICULE =====================
    y -= step
    
    c.drawString(x_label, y, "Matricule:")
    c.drawString(x_value, y, membre.matricule)
    
    # ===================== EMPLOI =====================
    y -= step
    
    c.drawString(x_label, y, "Emploi:")
    
    emploi_lines = simpleSplit(
        membre.emploi,
        "Helvetica-Bold",
        7,
        70
    )
    
    for line in emploi_lines:
        c.drawString(x_value, y, line)
        y -= 7


    # Photo
    if membre.photo:
        c.drawImage(ImageReader(membre.photo.path),
                    largeur - 85, hauteur - 147,
                    width=80, height=80)

    # QR Code
    qr_data = f"http://127.0.0.1:8000/verifier/{membre.matricule}"
    qr = qrcode.make(qr_data)

    qr_buffer = BytesIO()
    qr.save(qr_buffer, format='PNG')
    qr_buffer.seek(0)

    c.drawImage(ImageReader(qr_buffer), 8, 4, width=45, height=45)

    # ===================== PASSAGE VERSO =====================
    c.showPage()

# Fond verso

# ===================== VERSO =====================

# Fond verso
    maquette_verso = finders.find('images/Maquette_verso.jpg')
    if maquette_verso:
        c.drawImage(ImageReader(maquette_verso), 0, 0, width=largeur, height=hauteur)

    # 🔥 TITRE CENTRÉ
    titre = "PERSONNES A CHARGES"
    c.setFont("OpenSans", 7)
    #c.setFillColorRGB(0.145, 0.243, 0.565)

    text_width = c.stringWidth(titre, "OpenSans", 7)
    x_titre = (largeur - text_width) / 2
    y_titre = hauteur - 10

    c.drawString(x_titre, y_titre, titre)

# 🔥 IMPORTS


    styles = getSampleStyleSheet()
    #styleN = styles["Normal"]
    styleN = ParagraphStyle(
    name='Normal',
    fontName='OpenSans',   # 👈 même police que recto
    fontSize=6,
    leading=7
)   
    styleHeader = ParagraphStyle(
    name='Header',
    fontName='Helvetica-Bold',
    fontSize=7,
    leading=8,
    textColor=colors.black
)

# 🔥 RÉCUPÉRATION DES ENFANTS
    enfants = membre.enfants.all()

# 🔥 LIMITE
    max_rows = 9

# 🔥 FONCTION ANTI-DÉBORDEMENT
    def truncate(text, max_len=48):
        return text[:max_len] + "..." if len(text) > max_len else text

# 🔥 DONNÉES TABLEAU
    data = [[Paragraph("Descendants", styleHeader),Paragraph("Date de naissance", styleHeader)]]

    for e in enfants[:max_rows]:
        nom_complet = f"{e.nom.upper()} {e.prenom.title()}"

        data.append([
            Paragraph(truncate(nom_complet), styleN),
            Paragraph(e.date_naissance.strftime("%d/%m/%Y"), styleN)
        ])

# 🔥 SI DÉPASSEMENT
    if enfants.count() > max_rows:
        data.append([
            Paragraph("...", styleN),
            Paragraph(f"+{enfants.count() - max_rows} autres", styleN)
        ])

# 🔥 LARGEUR CONTRÔLÉE
    table_width = largeur - 20

    # 🔥 TABLEAU (SANS rowHeights)
    table = Table(
        data,
        colWidths=[table_width * 0.7, table_width * 0.3],
    )

# 🔥 STYLE
    table.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.5, colors.black),
        ("FONTSIZE", (0,0), (-1,-1), 7),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 2),
        ("RIGHTPADDING", (0,0), (-1,-1), 2),
        ("TOPPADDING", (0,0), (-1,-1), 1),
        ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ]))

# 🔥 CALCUL HAUTEUR RÉELLE DU TABLEAU
    w, h = table.wrap(largeur, hauteur)

# 🔥 POSITION DYNAMIQUE (ALIGNÉ SOUS LE TITRE)
    x = 10
    y = y_titre - 4 - h  # espace propre entre titre et tableau

# 🔥 AFFICHAGE
    table.drawOn(c, x, y)

    # 🔥 Affichages des conjoints-pere et mere juste apres le tableau
    y_info = y - 8   # espace après tableau

    c.setFont("OpenSans", 6)
    c.setFillColorRGB(0, 0, 0)

# ===================== CONJOINTE =====================#

    conjoints = membre.conjoints.all()

    if conjoints.exists():

        text = c.beginText()

        text.setTextOrigin(10, y_info)

        text.setFont("OpenSans", 6)

        # 🔹 Titre
        text.textLine("Conjoint(e)(s) :")

        # 🔹 Liste des conjoints
        for conjoint in conjoints:

            nom = (
                f"- {conjoint.nom.upper()} "
                f"{conjoint.prenom.capitalize()}"
            )

            text.textLine(nom)

        c.drawText(text)

        # 🔹 Ajustement position verticale
        y_info -= (len(conjoints) + 1) * 7
# ===================== PARENTS =====================
    parents = membre.parents.all()

    for p in parents:
        type_parent = "Père" if p.type_parent == 'P' else "Mère"
        nom_parent = f"{p.prenom.capitalize()} {p.nom.upper()}"
        
        c.setFont("OpenSans", 6)

        c.drawString(
            10,
            y_info,
            f"{type_parent} : {nom_parent}"
        )
        y_info -= 6
        
    # ===================== TEXTE BAS =====================
# 🔥 Style centré petite police
    styleFooter = ParagraphStyle(
        name='Footer',
        fontName='OpenSans',
        fontSize=5,
        leading=6,
        alignment=TA_RIGHT,
        textColor=colors.black
    )

    # 🔥 Texte (avec saut de ligne)
    footer_text = """Cette carte est la propriété exclusive de la MU.TRA.CHU-YO"""

    # 🔥 Création paragraphe
    footer = Paragraph(footer_text, styleFooter)

    # 🔥 Largeur contrôlée
    footer_width = largeur - 20

    # 🔥 Calcul taille
    w, h = footer.wrap(footer_width, hauteur)

    # 🔥 Position (collé en bas avec petite marge)
    x_footer = 15
    y_footer = 3

# 🔥 Affichage
    footer.drawOn(c, x_footer, y_footer)
    c.save()

    # Enregistrer la carte comme produite
    # Enregistrer la carte uniquement lors de la production officielle
    if not apercu:
        Carte.objects.update_or_create(
            membre=membre,
            defaults={
                 'statut': 'PRODUITE',
                 'date_production': timezone.now()
           }
        )

    buffer.seek(0)

    return HttpResponse(buffer, content_type='application/pdf')

def Apercu_carte(request, membre_id):
    membre = get_object_or_404(Membre, id=membre_id)

    return render(request, 'apercu_carte.html', {
        'membre': membre,
    })

#vertification du qrcode
def verifier_membre(request, matricule):
    try:
        membre = Membre.objects.get(matricule=matricule)
        return render(request, 'verification.html', {'membre': membre})
    except Membre.DoesNotExist:
        return render(request, 'verification.html', {'membre': None})
    
    
#VUE CARTE VERSO
def carte_verso(request, membre_id):
    membre = get_object_or_404(Membre, id=membre_id)

    # 🔹 Récupération des données
    conjoint = getattr(membre, 'conjoint', None)
    enfants = membre.enfants.all()
    parents = membre.parents.all()

    # 🔹 Séparer père et mère
    pere = parents.filter(type_parent='P').first()
    mere = parents.filter(type_parent='M').first()

    return render(request, 'carte_verso.html', {
        'membre': membre,
        'conjoint': conjoint,
        'enfants': enfants,
        'pere': pere,
        'mere': mere
    })