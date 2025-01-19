# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 14:09:35 2025

@author: 33674
"""

import tkinter as tk
import serial
import time

# Fonction pour envoyer la commande à Arduino via série
def envoyer_commande():
    # Récupérer la valeur du champ "Mesure" (distance)
    mesure = mesure_entry.get()
    
    try:
        # Convertir la mesure en float
        distance = float(mesure)
        
        # Envoyer la distance via le port série
        ser.write(f"{distance}\n".encode())  # Envoie la distance à Arduino sous forme de chaîne de caractères
        
        # Afficher la valeur dans la console
        print(f"Commande envoyée : {distance} mm")
        
        # Attendre la réponse d'Arduino (si nécessaire)
        time.sleep(1)  # Attendre un peu pour que le moteur termine son mouvement
        
    except ValueError:
        print("Veuillez entrer une valeur valide pour la mesure.")

# Créer la fenêtre principale
root = tk.Tk()
root.title("Contrôle du Rail - Interface graphique")

# Créer les champs de texte et les étiquettes
tk.Label(root, text="Mesure (distance à parcourir en mm):").grid(row=0, column=0, padx=10, pady=5, sticky='w')
mesure_entry = tk.Entry(root)
mesure_entry.grid(row=0, column=1, padx=10, pady=5)

# Créer un bouton pour envoyer la commande
submit_button = tk.Button(root, text="Envoyer la commande", command=envoyer_commande)
submit_button.grid(row=1, column=0, columnspan=2, pady=20)

# Initialiser la communication série avec Arduino
ser = serial.Serial('COM3', 9600)  # Remplacez 'COM3' par le port correct sur votre machine
time.sleep(2)  # Attendre que la connexion série soit établie

# Démarrer la boucle principale de Tkinter
root.mainloop()

# Fermer la connexion série à la fin du programme
ser.close()
#%%
import tkinter as tk
import serial
import time

# Fonction pour envoyer une commande à Arduino
def envoyer_commande():
    mesure = mesure_entry.get()
    try:
        distance = float(mesure)
        ser.write(f"{distance}\n".encode())
        print(f"Commande envoyée : {distance} mm")
    except ValueError:
        print("Veuillez entrer une valeur valide pour la mesure.")

# Fonction pour envoyer la commande d'arrêt
def arreter_commande():
    ser.write("abort\n".encode())
    print("Commande d'arrêt envoyée !")

# Fonction pour surveiller les messages d'Arduino
def surveiller_capteur():
    while True:
        # Lire les messages envoyés par Arduino
        if ser.in_waiting > 0:
            message = ser.readline().decode().strip()
            print(f"Message de l'Arduino : {message}")
            if "Capteur de fin de course activé" in message:
                print("Arrêt du mouvement en raison du capteur de fin de course")
                # Ici vous pouvez envoyer d'autres commandes ou afficher un message à l'utilisateur.
                break  # Quitter la fonction ou effectuer d'autres actions

# Créer la fenêtre principale
root = tk.Tk()
root.title("Contrôle du Rail - Interface graphique")

# Champs et étiquettes
tk.Label(root, text="Mesure (distance à parcourir en mm):").grid(row=0, column=0, padx=10, pady=5, sticky='w')
mesure_entry = tk.Entry(root)
mesure_entry.grid(row=0, column=1, padx=10, pady=5)

# Bouton pour envoyer la commande
submit_button = tk.Button(root, text="Envoyer la commande", command=envoyer_commande)
submit_button.grid(row=1, column=0, columnspan=2, pady=10)

# Bouton pour arrêter le mouvement
abort_button = tk.Button(root, text="Arrêter", command=arreter_commande, bg="red", fg="white")
abort_button.grid(row=2, column=0, columnspan=2, pady=10)

# Initialiser la communication série avec Arduino
ser = serial.Serial('COM3', 9600)  # Remplacez 'COM3' par le port approprié
time.sleep(2)  # Attendre que la connexion série soit établie

# Démarrer un thread ou un processus pour surveiller le capteur
import threading
capteur_thread = threading.Thread(target=surveiller_capteur)
capteur_thread.daemon = True
capteur_thread.start()

# Démarrer la boucle principale de Tkinter
root.mainloop()

# Fermer la connexion série
ser.close()

#%%
import tkinter as tk
import serial
import time
import threading

# Variables globales
ser = None
abort_flag = False

# Fonction pour envoyer la commande à Arduino via série
def envoyer_commande():
    global abort_flag
    # Récupérer la valeur du champ "Mesure" (distance)
    mesure = mesure_entry.get()

    try:
        # Convertir la mesure en float
        distance = float(mesure)
        if distance <= 0:
            raise ValueError("La distance doit être un nombre positif.")

        # Envoyer la distance via le port série
        ser.write(f"{distance}\n".encode())  # Envoie la distance à Arduino sous forme de chaîne de caractères
        
        # Réinitialiser le flag d'arrêt
        abort_flag = False

        # Démarrer un thread pour surveiller la progression
        threading.Thread(target=suivre_mouvement, daemon=True).start()

    except ValueError as e:
        print(f"Erreur : {e}")
        status_label.config(text="Erreur : Veuillez entrer une valeur valide.")

# Fonction pour suivre l'état du rail depuis Arduino
def suivre_mouvement():
    global abort_flag
    while True:
        if abort_flag:
            break
        try:
            if ser.in_waiting > 0:
                message = ser.readline().decode('utf-8').strip()
                print(f"Arduino : {message}")
                status_label.config(text=f"Arduino : {message}")
                if message == "Mouvement terminé" or message == "Mouvement annulé":
                    break
        except Exception as e:
            print(f"Erreur lors de la lecture série : {e}")
            status_label.config(text="Erreur de communication avec Arduino.")
            break

# Fonction d'arrêt d'urgence
def abort():
    global abort_flag
    abort_flag = True
    try:
        ser.write(b"ABORT\n")  # Envoyer la commande d'annulation à Arduino
        print("Arrêt d'urgence activé")
        status_label.config(text="Arrêt d'urgence activé.")
    except Exception as e:
        print(f"Erreur lors de l'envoi de la commande d'arrêt : {e}")

# Fonction pour initialiser la connexion série
def initialiser_serie(port, baudrate=9600):
    global ser
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)  # Attendre que la connexion série soit établie
        print(f"Connexion série établie sur {port} à {baudrate} bauds.")
        status_label.config(text=f"Connexion série établie sur {port}.")
    except serial.SerialException as e:
        print(f"Erreur lors de la connexion au port série : {e}")
        status_label.config(text="Erreur : Impossible de se connecter au port série.")
        ser = None

# Créer la fenêtre principale
root = tk.Tk()
root.title("Contrôle du Rail - Interface graphique")

# Créer les champs de texte et les étiquettes
tk.Label(root, text="Mesure (distance à parcourir en mm):").grid(row=0, column=0, padx=10, pady=5, sticky='w')
mesure_entry = tk.Entry(root)
mesure_entry.grid(row=0, column=1, padx=10, pady=5)

# Créer un bouton pour envoyer la commande
submit_button = tk.Button(root, text="Envoyer la commande", command=envoyer_commande)
submit_button.grid(row=1, column=0, columnspan=2, pady=20)

# Créer un bouton pour arrêter le mouvement (Abort)
abort_button = tk.Button(root, text="Arrêter le mouvement", command=abort)
abort_button.grid(row=2, column=0, columnspan=2, pady=20)

# Ajouter une étiquette pour afficher l'état
status_label = tk.Label(root, text="Statut : En attente de commande.")
status_label.grid(row=3, column=0, columnspan=2, pady=10)

# Initialiser la communication série avec Arduino
initialiser_serie('COM3')  # Remplacez 'COM3' par le port correct sur votre machine

# Démarrer la boucle principale de Tkinter
if ser:
    root.mainloop()

# Fermer la connexion série à la fin du programme
if ser:
    ser.close()
