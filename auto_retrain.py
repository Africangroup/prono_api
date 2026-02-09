import pandas as pd
import subprocess
import os

# Charger la mémoire
memory = pd.read_csv("memory.csv")

print(f"📊 Paris enregistrés : {len(memory)}")

# Condition : on réentraîne tous les 20 paris
if len(memory) < 20:
    print("⏳ Pas assez de données pour réentraîner")
    exit()

print("🧠 Réentraînement du modèle en cours...")

# Lancer le script d'entraînement existant
os.system("C:\\Python313\\python.exe train_live_model.py")

print("✅ Modèle mis à jour avec les nouvelles données")
