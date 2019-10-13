# -*- coding: utf-8 -*-
"""
########################################################################
#
#  Puissance 4 - Ordinateur contre Ordinateur avec IA
#
#  Copyright 2016-2019 - Eric Sérandour
#  Version du 13 octobre 2019 à 14 h 28
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
import math




couleurJoueur = ''
victoiresJaunes = 0
victoiresRouges = 0
partiesNulles = 0
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

def fin_partie(positions):
    """ Test de fin de partie"""
    global couleurJoueur
    global victoiresJaunes
    global victoiresRouges
    global partiesNulles
    # On teste si la partie est finie
    fin = False
    if alignements(positions, 4, couleurJoueur):
        fin = True
        if couleurJoueur == 'yellow':
            victoiresJaunes += 1
        elif couleurJoueur == 'red':
            victoiresRouges += 1
        # On affiche le gagnant
        affiche_gagnant_console(couleurJoueur)
        if MODE_GRAPHIQUE:
            affiche_gagnant_fenetre(couleurJoueur)
    elif grille_pleine(positions):
        fin = True
        partiesNulles += 1
        # On affiche aucun gagnant
        affiche_aucun_gagnant_console()
        if MODE_GRAPHIQUE:
            affiche_aucun_gagnant_fenetre()
    else:
        couleurJoueur = inverse(couleurJoueur)
        # On affiche qui doit jouer
        affiche_joueur_console(couleurJoueur)
        if MODE_GRAPHIQUE:
            affiche_joueur_fenetre(couleurJoueur)
    return fin

########################################################################

def competition(ia1, ia2):
    """ """
    listePositions = initialise_liste_positions()
    # ia1 joue en premier sur la moitié des parties
    finPartie = False
    for i in range(NB_PARTIES // 2):
        affiche_joueur_qui_commence_console(couleurJoueur)
        if MODE_GRAPHIQUE:
            affiche_joueur_qui_commence_fenetre(couleurJoueur)
        while not finPartie:
            listePositions = jouer_ordi_ia(listePositions, couleurJoueur, ia1)
            finPartie = fin_partie(listePositions)  # Teste si la partie est finie
            if not finPartie:
                listePositions = jouer_ordi_ia(listePositions, couleurJoueur, ia2)
                finPartie = fin_partie(listePositions)  # Teste si la partie est finie
        # Bilan
        nbCoupsGagnant = analyse_positions(listePositions)
        affiche_statistiques_console(victoiresJaunes, victoiresRouges, partiesNulles)
        if MODE_GRAPHIQUE:
            affiche_statistiques_fenetre(victoiresJaunes, victoiresRouges, partiesNulles)
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
    couleurJoueur = 'yellow'  # Couleur qui commence
    competition(IA_JAUNE, IA_ROUGE)
    couleurJoueur = 'red'  # Couleur qui commence
    competition(IA_ROUGE, IA_JAUNE)

########################################################################
