# Importation des bibliothèques nécessaires
import cv2              # Pour la capture vidéo
import handtracking    # Pour la détection de la main
import serialobject    # Pour la communication série

# Ouvre la caméra vidéo (l'indice 1 peut être modifié pour choisir la caméra à utiliser)
cap = cv2.VideoCapture(1)

# Crée un objet "HandDetector" avec une limite de 1 main détectable maximum et un seuil de détection de 0,7
detector = handtracking.HandDetector(maxHands=1, detectionCon=int(0.7))

# Crée un objet "SerialObject" pour la communication série avec le port /dev/cu.usbmodem1101, une vitesse de transmission de données de 9600 bauds et une attente d'une seconde entre chaque envoi de données.
mySerial = serialobject.SerialObject("/dev/cu.usbmodem1101", 9600, 1)

# Boucle principale qui capture en continu des images de la caméra et détecte les doigts
while True:
    # Lecture d'une image à partir de la caméra
    success, img = cap.read()

    # Détecte les mains dans l'image lue et dessine des marqueurs sur les mains détectées
    img = detector.findHands(img)

    # Détecte la position des marqueurs sur les doigts et les paumes et renvoie une liste des positions des marqueurs ainsi qu'une boîte englobante qui entoure la main.
    lmlist, bbox = detector.findPosition(img)

    # Si au moins une main a été détectée, détermine quels doigts sont levés et envoie les données des doigts détectés à l'autre appareil via la connexion série.
    if lmlist:
        fingers = detector.fingersUp()     # Détermine quels doigts sont levés
        print(fingers)                     # Affiche les résultats dans la console
        mySerial.sendData(fingers)         # Envoie les données des doigts détectés via la connexion série

    # Affiche l'image lue dans une fenêtre avec le nom "Image"
    cv2.imshow("Image", img)

    # Attend une milliseconde pour permettre l'affichage de la fenêtre
    cv2.waitKey(1)
