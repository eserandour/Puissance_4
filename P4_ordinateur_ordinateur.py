# -*- coding: utf-8 -*-
"""
########################################################################
#
#  Puissance 4 - Ordinateur contre Ordinateur avec IA
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
from constantes import MODE_GRAPHIQUE, NB_PARTIES, IA_JAUNE, IA_ROUGE
from commun import *
from ia import *
if MODE_GRAPHIQUE:
    from mode_graphique import *




# Variables globales
victoires = [0] * 3  # Jaunes, Rouges, Nulles




########################################################################

def competition(couleur, ia1, ia2):
    """Compétition entre 2 IA"""
    global victoires
    listePositions = initialise_liste_positions()
    finPartie = False
    # ia1 joue en premier sur la moitié des parties
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
