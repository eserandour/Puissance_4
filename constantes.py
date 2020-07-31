# -*- coding: utf-8 -*-
"""
########################################################################
#  Version du 31 juillet 2020 à 10 h 50
########################################################################
"""

########################################################################
# REGLAGES POUR LA COMPETITION
########################################################################

NB_PARTIES = 1000000  # A adapter (un nombre pair plus grand que 1)
# Pour Ordinateur contre Ordinateur : IA_JAUNE et IA_ROUGE
# Pour Humain contre Ordinateur : IA_ROUGE
# L'IA 15 est actuellement la meilleure
IA_JAUNE = 15  # Numéro de l'IA en compétition (entre 0 et 20 actuellement, mais pas de 11)
IA_ROUGE = 15  # Numéro de l'IA en compétition (entre 0 et 20 actuellement, mais pas de 11)

########################################################################




########################################################################
# CHOIX DE L'AFFICHAGE
########################################################################

MODE_GRAPHIQUE = True  # True : Pour afficher la grille dans une fenêtre et dans la console
                       # False : Pour afficher la grille dans la console exclusivement
TEMPS_CHUTE = 0.1  # 0.1 pour visualiser la chute des pions sinon 0
LARGEUR_GRILLE = 480  # A adapter
ESPACEMENT = LARGEUR_GRILLE / 64  # Espace entre 2 trous de la grille

########################################################################




########################################################################
# CONTRAINTES DU JEU
########################################################################

NB_COLONNES = 7  # Nombre de colonnes de la grille de jeu
NB_LIGNES = 6  # Nombre de lignes de la grille de jeu
ALIGNEMENT = 4  # Nombre de pions à aligner pour gagner

########################################################################
