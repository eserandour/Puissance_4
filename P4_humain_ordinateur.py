# -*- coding: utf-8 -*-
"""
########################################################################
#
#  Puissance 4 - Humain contre Ordinateur avec IA
#
#  Copyright 2016-2019 - Eric Sérandour
#  Version du 14 octobre 2019 à 23 h 17
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation; either version 3 of
#  the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public
#  License along with this program; if not, write to the Free
#  Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110-1301, USA.
#
########################################################################
"""
#!/usr/bin/env python

# Pour paramétrer Puissance 4, aller dans le fichier constantes.py
from constantes import MODE_GRAPHIQUE, IA_ROUGE, NB_COLONNES, ESPACEMENT
from commun import *
from ia import *
if MODE_GRAPHIQUE:
    from mode_graphique import *
import random
import time




# Variables globales
finPartie = True
listePositions = []
couleurJoueur = ''
victoires = [0] * 3  # Jaunes, Rouges, Nulles
blocageJoueur = False

########################################################################




########################################################################

def mouse_clic(event):
    "Gestion du clic de souris"
    global finPartie
    global listePositions
    global couleurJoueur
    global victoires
    global blocageJoueur  # Indispensable pour les cas où l'on clique trop vite
    if not blocageJoueur:
        if finPartie:
            blocageJoueur = True
            listePositions = initialise_liste_positions()
            destruction_jetons()
            efface_message_fenetre()
            fenetreJeu.update()
            time.sleep(1)
            couleurJoueur = random.choice(['yellow', 'red'])
            # Affiche joueur qui commence
            affiche_joueur_qui_commence_console(couleurJoueur)
            affiche_joueur_qui_commence_fenetre(couleurJoueur)
            if couleurJoueur == 'red' :
                listePositions = jouer_ordi_ia(listePositions, couleurJoueur, IA_ROUGE)
                finPartie, couleurJoueur, victoires = fin_partie(listePositions, couleurJoueur, victoires)  # Teste si la partie est finie
            finPartie = False
            blocageJoueur = False
        else:
            x = event.x
            colonne = col = 0
            while col < NB_COLONNES:
                col = col + 1
                ray = rayon()
                if x > col*ESPACEMENT+2*(col-1)*ray and x < col*ESPACEMENT+2*col*ray:
                    colonne = col
            if (colonne and not colonne_pleine(listePositions, colonne)):
                blocageJoueur = True
                listePositions = jouer(listePositions, couleurJoueur, colonne)
                finPartie, couleurJoueur, victoires = fin_partie(listePositions, couleurJoueur, victoires)  # Teste si la partie est finie
                if not finPartie :
                    listePositions = jouer_ordi_ia(listePositions, couleurJoueur, IA_ROUGE)
                    finPartie, couleurJoueur, victoires = fin_partie(listePositions, couleurJoueur, victoires)  # Teste si la partie est finie
                if finPartie:
                    # Bilan
                    affiche_victoires_console(victoires)  # Jaunes, Rouges, Nulles
                    affiche_victoires_fenetre(victoires)  # Jaunes, Rouges, Nulles
                blocageJoueur = False

########################################################################

# La méthode bind() permet de lier un évènement avec une fonction
grille.bind('<Button-1>', mouse_clic)

########################################################################




########################################################################
# PARTIE PRINCIPALE
########################################################################

finPartie = False
listePositions = initialise_liste_positions()
couleurJoueur = random.choice(['yellow', 'red'])
affiche_joueur_qui_commence_console(couleurJoueur)
affiche_joueur_qui_commence_fenetre(couleurJoueur)
if couleurJoueur == 'red':
    listePositions = jouer_ordi_ia(listePositions, couleurJoueur, IA_ROUGE)
    finPartie, couleurJoueur, victoires = fin_partie(listePositions, couleurJoueur, victoires)  # Teste si la partie est finie

# Démarrage du réceptionnaire d'évènements (boucle principale) :
fenetreJeu.mainloop()

########################################################################
