# -*- coding: utf-8 -*-
"""
########################################################################
#
#  Puissance 4 - Ordinateur contre Ordinateur avec IA
#
#  Copyright 2016-2019 - Eric Sérandour
#  Version du 14 octobre 2019 à 18 h 20
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
from constantes import MODE_GRAPHIQUE, NB_PARTIES, IA_JAUNE, IA_ROUGE, NB_COLONNES, NB_LIGNES
from commun import *
from ia import *
if MODE_GRAPHIQUE:
    from mode_graphique import *
import math




# Variables globales
couleurJoueur = ''
victoires = [0] * 3  # Jaunes, Rouges, Nulles
nbCoupsGagnant = 0

########################################################################




########################################################################
# ANALYSE
########################################################################

def analyse_positions(positions):
    """Analyse les positions"""
    global nbCoupsGagnant
    # Nombre de coups du gagnant
    nbPositionsPleines = NB_LIGNES*NB_COLONNES
    for i in range(NB_LIGNES*NB_COLONNES):
        if positions[i] == 0:
            nbPositionsPleines -= 1
    nbCoupsGagnant = math.ceil(nbPositionsPleines/2)  ## Arrondi à l'entier supérieur

########################################################################




########################################################################

def competition(couleur, ia1, ia2):
    """ """
    global couleurJoueur
    global victoires
    listePositions = initialise_liste_positions()
    # ia1 joue en premier sur la moitié des parties
    finPartie = False
    for i in range(NB_PARTIES // 2):
        affiche_joueur_qui_commence_console(couleur)
        if MODE_GRAPHIQUE:
            affiche_joueur_qui_commence_fenetre(couleur)
        couleurJoueur = couleur
        while not finPartie:
            listePositions = jouer_ordi_ia(listePositions, couleurJoueur, ia1)
            finPartie, couleurJoueur, victoires = fin_partie(listePositions, couleurJoueur, victoires)  # Teste si la partie est finie
            if not finPartie:
                listePositions = jouer_ordi_ia(listePositions, couleurJoueur, ia2)
                finPartie, couleurJoueur, victoires = fin_partie(listePositions, couleurJoueur, victoires)  # Teste si la partie est finie
        # Bilan
        nbCoupsGagnant = analyse_positions(listePositions)
        affiche_victoires_console(victoires)  # Jaunes, Rouges, Nulles
        if MODE_GRAPHIQUE:
            affiche_victoires_fenetre(victoires)  # Jaunes, Rouges, Nulles
        # Initialisation
        listePositions = initialise_liste_positions()
        finPartie = False
        if MODE_GRAPHIQUE:
            initialise_fenetre(NB_PARTIES)

########################################################################




########################################################################
# PARTIE PRINCIPALE
########################################################################

if NB_PARTIES > 1:
    competition('yellow', IA_JAUNE, IA_ROUGE)  # Les jaunes commencent sur la moitié des parties
    competition('red', IA_ROUGE, IA_JAUNE)  # Les rouges commencent sur la moitié des parties

# Démarrage du réceptionnaire d'évènements (boucle principale) :
if MODE_GRAPHIQUE:
    fenetreJeu.mainloop()

########################################################################
