from rembg import remove
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import cv2
import numpy as np


def enregistrer_photo_sans_fond(membre, photo_field, background_color=(255, 255, 255)):
    input_image = Image.open(photo_field).convert("RGBA")
    output_image = remove(input_image)
    background = Image.new("RGBA", output_image.size, background_color + (255,))
    
    final_image = Image.alpha_composite(background, output_image)
    
 
  
    
    final_image = final_image.convert("RGB")

    buffer = BytesIO()
    final_image.save(buffer, format="PNG")
    buffer.seek(0)
    membre.photo.save(f"{membre.nom}_clean.png", ContentFile(buffer.read()), save=True)







def rogner_zoom_visage(membre, photo_field, largeur_identite=413, hauteur_identite=331):
    """
    Rogne et zoom sur le visage pour créer une photo d'identité.
    """
   
    image = Image.open(photo_field).convert("RGB")

    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

   
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) > 0:
        # Prendre le premier visage détecté
        x, y, w, h = faces[0]
        # Ajouter une marge autour du visage
        margin_x = int(w * 0.3)
        margin_y = int(h * 0.5)
        left = max(0, x - margin_x)
        top = max(0, y - margin_y)
        right = min(image.width, x + w + margin_x)
        bottom = min(image.height, y + h + margin_y)
        image = image.crop((left, top, right, bottom))
    else:
        # Si aucun visage détecté, rogner au centre
        crop_size = min(image.width, image.height)
        left = (image.width - crop_size) / 2
        top = (image.height - crop_size) / 2
        right = (image.width + crop_size) / 2
        bottom = (image.height + crop_size) / 2
        image = image.crop((left, top, right, bottom))

   
    image = image.resize((largeur_identite, hauteur_identite), Image.Resampling.LANCZOS)

   
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)
    membre.photo.save(f"{membre.nom}_identite.jpg", ContentFile(buffer.read()), save=True)
