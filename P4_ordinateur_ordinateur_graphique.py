# -*- coding: utf-8 -*-
"""
########################################################################
#
#  Puissance 4 - Ordinateur contre Ordinateur avec IA (mode Graphique)
#
#  Copyright 2016-2019 - Eric Sérandour
#  Version du 06 octobre 2019 à 19 h 47
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation; either version 2 of
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

import time
import random
import math
import tkinter

########################################################################
# REGLAGES POUR LA COMPETITION
########################################################################

NB_PARTIES = 6  # A adapter (un nombre pair plus grand que 1)
IA_JAUNE = 5  # Numéro de l'IA en compétition (entre 0 et 9 actuellement)
IA_ROUGE = 0  # Numéro de l'IA en compétition (entre 0 et 9 actuellement)

########################################################################

NB_COLONNES = 7  # A adapter
NB_LIGNES = 6  # A adapter
positions = [0] * NB_COLONNES*NB_LIGNES

finPartie = False
couleur = ''
victoiresJaunes = 0
victoiresRouges = 0
partiesNulles = 0

TEMPS_PAUSE = 1  # A adapter

nbCoupsGagnant = 0
positionsGagnantes = [0] * NB_COLONNES*NB_LIGNES  # A traiter plus tard




########################################################################
# AFFICHAGE DE LA GRILLE ET DES JETONS DANS LA CONSOLE
########################################################################

def affiche_grille_console():
    " Affiche la grille dans la console"
    i = NB_COLONNES*(NB_LIGNES-1)
    while i >= 0:
        print(positions[i:i+NB_COLONNES])
        i = i - NB_COLONNES
    print()

########################################################################




########################################################################
# FENETRE TKINTER
########################################################################

########################################################################
# Création du widget principal ("parent") : fenetreJeu
########################################################################

fenetreJeu = tkinter.Tk()
fenetreJeu.title("Puissance 4")

########################################################################
# AFFICHAGE DE LA GRILLE ET DES JETONS DANS LA FENETRE TKINTER
########################################################################

LARGEUR_GRILLE = 480  # A adapter
ESPACEMENT = LARGEUR_GRILLE / 64  # Espace entre 2 trous de la grille
rayon = (LARGEUR_GRILLE-(NB_COLONNES+1)*ESPACEMENT)/(2*NB_COLONNES)
hauteurGrille = 2*NB_LIGNES*rayon+(NB_LIGNES+1)*ESPACEMENT

########################################################################

def creation_disque(x, y, r, c, tag):
    "Création d'un disque tag (trou ou jeton), de rayon r et de couleur c à la position (x,y)"
    identifiant = grille.create_oval(x-r, y-r, x+r, y+r, fill=c, width=0, tags=tag)
    return identifiant

########################################################################

def creation_grille():
    "Création de la grille"
    ligne = 1
    while ligne <= NB_LIGNES:
        colonne = 1
        while colonne <= NB_COLONNES:
            creation_disque(ESPACEMENT+rayon+(colonne-1)*(ESPACEMENT+2*rayon),
                            ESPACEMENT+rayon+(ligne-1)*(ESPACEMENT+2*rayon),
                            rayon, 'white', 'trou')
            colonne += 1
        ligne += 1

########################################################################

def creation_jeton(colonne, ligne, c):  # Dépend de la grille
    "Création d'un jeton de couleur c à la colonne et à la ligne indiquée"
    identifiant = creation_disque(colonne*(ESPACEMENT+2*rayon)-rayon,
                                  (NB_LIGNES-ligne+1)*(ESPACEMENT+2*rayon)-rayon,
                                  rayon, c, 'jeton')
    return identifiant

########################################################################

def mouvement_jeton(identifiant):
    "Mouvement d'un jeton"
    grille.move(identifiant, 0, ESPACEMENT+2*rayon)

########################################################################

def affiche_coup_fenetre(colonne, ligneSupport):
    "Affichage du coup joué (avec chute du pion)"
    TEMPS_CHUTE = 0  # 0.1 pour visualiser la chute des pions                     # TEMPS_CHUTE des pions
    ligne = NB_LIGNES
    identifiant = creation_jeton(colonne, ligne, couleur)
    while ligne > ligneSupport:
        if ligne < NB_LIGNES:
            mouvement_jeton(identifiant)
        fenetreJeu.update()
        time.sleep(TEMPS_CHUTE)
        ligne = ligne - 1

########################################################################

def destruction_jetons():
    "Destruction de tous les jetons"
    grille.delete('jeton')

########################################################################
# Création des widgets "enfants" : grille (Canvas)
########################################################################

grille = tkinter.Canvas(fenetreJeu, width=LARGEUR_GRILLE, height=hauteurGrille, background='blue')
creation_grille()
grille.pack()

########################################################################
# Création des widgets "enfants" : message (Label)
########################################################################

message = tkinter.Label(fenetreJeu)
message.pack()

########################################################################
# Création des widgets "enfants" : scoreJaunes (Label)
########################################################################

scoreJaunes = tkinter.Label(fenetreJeu, text='Jaunes : 0')
scoreJaunes.pack(side='left')

########################################################################
# Création des widgets "enfants" : scoreRouges (Label)
########################################################################

scoreRouges = tkinter.Label(fenetreJeu, text='Rouges : 0')
scoreRouges.pack(side='right')

########################################################################




########################################################################
# AFFICHAGE DES MESSAGES
########################################################################

def affiche_joueur_qui_commence_console():
    """Affichage du joueur qui commence dans la console"""
    if couleur == 'yellow':
        print('Les jaunes commencent')
    elif couleur == 'red':
        print('Les rouges commencent')

########################################################################

def affiche_joueur_qui_commence_fenetre():
    "Affichage du premier joueur dans la fenêtre Tkinter"
    if couleur == 'yellow':
        message['text'] = 'Les jaunes commencent'
    elif couleur == 'red':
        message['text'] = 'Les rouges commencent'

########################################################################

def affiche_joueur_qui_commence():
    "Affichage du premier joueur"
    affiche_joueur_qui_commence_console()
    affiche_joueur_qui_commence_fenetre()

########################################################################

def affiche_joueur_console():
    "Affichage du joueur dans la console"
    if couleur == 'yellow':
        print('Les jaunes jouent')
    elif couleur == 'red':
        print('Les rouges jouent')

########################################################################

def affiche_joueur_fenetre():
    "Affichage du joueur dans la fenêtre Tkinter"
    if couleur == 'yellow':
        message['text'] = 'Les jaunes jouent'
    elif couleur == 'red':
        message['text'] = 'Les rouges jouent'

########################################################################

def affiche_joueur():
    "Affichage du joueur"
    affiche_joueur_console()
    affiche_joueur_fenetre()

########################################################################

def affiche_gagnant_console():
    "Affichage du gagnant dans la console"
    if couleur == 'yellow':
        print('Les jaunes gagnent')
    elif couleur == 'red':
        print('Les rouges gagnent')

########################################################################

def affiche_gagnant_fenetre():
    "Affichage du gagnant dans la fenêtre Tkinter"
    if couleur == 'yellow':
        message['text'] = 'Les jaunes gagnent'
        scoreJaunes['text'] = 'Jaunes : ' + str(victoiresJaunes)
    elif couleur == 'red':
        message['text'] = 'Les rouges gagnent'
        scoreRouges['text'] = 'Rouges : ' + str(victoiresRouges)

########################################################################

def affiche_gagnant():
    "Affichage du gagnant"
    affiche_gagnant_console()
    affiche_gagnant_fenetre()

########################################################################

def affiche_aucun_gagnant_console():
    "Affichage aucun gagnant dans la console"
    print('Aucun gagnant')

########################################################################

def affiche_aucun_gagnant_fenetre():
    "Affichage aucun gagnant dans la fenêtre Tkinter"
    message['text'] = 'Aucun gagnant'

########################################################################

def affiche_aucun_gagnant():
    "Affichage aucun gagnant"
    affiche_aucun_gagnant_console()
    affiche_aucun_gagnant_fenetre()

########################################################################

def efface_message_fenetre():
    "Efface le label message dans la fenêtre Tkinter"
    message['text'] = ''

########################################################################

def affiche_statistiques_console():
    """Affichage des statistiques"""
    print('Nombre de coups du gagnant :', nbCoupsGagnant)
    print('Jaunes : ' + str(victoiresJaunes))
    print('Rouges : ' + str(victoiresRouges))
    print('Nulles : ' + str(partiesNulles))
    print()

########################################################################




########################################################################
# MOTEUR DU JEU
########################################################################

def initialise_liste_positions():
    """Vide la grille"""
    for i in range(NB_COLONNES*NB_LIGNES):
        positions[i] = 0

########################################################################

def alignement(somme, nbPions, couleur):
    """Analyse la somme dont il est question dans alignements()"""
    pionsAlignes = False
    if (couleur == 'yellow' and somme == nbPions) or (couleur == 'red' and somme == -nbPions):
        pionsAlignes = True
    return pionsAlignes

########################################################################

def alignements(nbPions, couleur):
    """Teste les alignements d'un nombre de pions donnés
       et les retourne sous forme de liste"""
    listeAlignements = []
    # Vérification des alignements horizontaux
    for j in range(NB_LIGNES):
        for i in range(NB_COLONNES-nbPions+1):
            somme = 0
            for k in range(nbPions):
                somme += positions[NB_COLONNES*j+i+k]
            if alignement(somme, nbPions, couleur):
                listeAlignements += [i+1,j+1,"H"]
    # Vérification des alignements verticaux
    for j in range(NB_LIGNES-nbPions+1):
        for i in range(NB_COLONNES):
            somme = 0
            for k in range(nbPions):
                somme += positions[NB_COLONNES*j+i+k*NB_COLONNES]
            if alignement(somme, nbPions, couleur):
                listeAlignements += [i+1,j+1,"V"]
    # Vérification des diagonales montantes
    for j in range(NB_LIGNES-nbPions+1):
        for i in range(NB_COLONNES-nbPions+1):
            somme = 0
            for k in range(nbPions):
                somme += positions[NB_COLONNES*j+i+k*NB_COLONNES+k]
            if alignement(somme, nbPions, couleur):
                listeAlignements += [i+1,j+1,"DM"]
    # Vérification des diagonales descendantes
    for j in range(nbPions-1, NB_LIGNES):
        for i in range(NB_COLONNES-nbPions+1):
            somme = 0
            for k in range(nbPions):
                somme += positions[NB_COLONNES*j+i-k*NB_COLONNES+k]
            if alignement(somme, nbPions, couleur):
                listeAlignements += [i+1,j+1,"DD"]
    if listeAlignements != []:
        listeAlignements = [nbPions] + listeAlignements
    return listeAlignements

########################################################################

def grille_pleine():
    "Teste si la grille est pleine"
    plein = True
    for i in range(NB_LIGNES*NB_COLONNES):
        if positions[i] == 0:
            plein = False
    return plein

########################################################################

def fin_partie():
    """ Test de fin de partie"""
    global victoiresJaunes
    global victoiresRouges
    global partiesNulles
    global couleur
    # On teste si la partie est finie
    fin = False
    if alignements(4, couleur):
        fin = True
        if couleur == 'yellow':
            victoiresJaunes += 1
        elif couleur == 'red':
            victoiresRouges += 1
        # On affiche le gagnant
        affiche_gagnant()
    elif grille_pleine():
        fin = True
        partiesNulles += 1
        # On affiche aucun gagnant
        affiche_aucun_gagnant()
    else:
        if couleur == 'red':
            couleur = 'yellow'
        elif couleur == 'yellow':
            couleur = 'red'
        # On affiche qui doit jouer
        affiche_joueur()
    return fin

########################################################################

def colonne_pleine(colonne):
    "Teste si la colonne indiquée est pleine"
    plein = True
    position = NB_COLONNES*(NB_LIGNES-1)+colonne-1
    if positions[position] == 0:
        plein = False
    return plein

########################################################################

def jouer(colonne):
    "Moteur du jeu"
    if not colonne_pleine(colonne):
        # On remplit la liste des positions
        position = colonne - 1
        ligneSupport = 0
        while positions[position]:
            ligneSupport = ligneSupport + 1
            position = position + NB_COLONNES
        if couleur == 'yellow':
            valeur = 1
        elif couleur == 'red':
            valeur = -1
        positions[position] = valeur
        # On affiche la grille pour visualiser les positions
        affiche_grille_console()
        affiche_coup_fenetre(colonne, ligneSupport)

########################################################################

def joueur_qui_commence(choix):
    """Choix du joueur qui commence"""
    if choix == 'random':
        choix = random.choice(['yellow', 'red'])
    return choix

########################################################################




########################################################################
# STRATEGIES DE JEU (CUISINE INTERNE)
########################################################################

def jouer_ordi_hasard():
    """L'ordinateur joue au hasard"""
    colonne = random.randint(1, NB_COLONNES)
    while colonne_pleine(colonne):
        colonne = random.randint(1, NB_COLONNES)
    jouer(colonne)

########################################################################

def jouer_ordi_poids_cases():
    """L'ordinateur joue en ne tenant compte que du poids des cases de la grille (7x6) potentiellement victorieuses"""
    POIDS_POSITIONS = [3,4,5,7,5,4,3,4,6,8,10,8,6,4,5,8,11,13,11,8,5,5,8,11,13,11,8,5,4,6,8,10,8,6,4,3,4,5,7,5,4,3]
    poids_colonne = [0] * NB_COLONNES
    for colonne in range(1, NB_COLONNES + 1):
        if not colonne_pleine(colonne):
            position = colonne - 1
            while positions[position]:
                position += NB_COLONNES
            poids_colonne[colonne - 1] = POIDS_POSITIONS[position]
        else:
            poids_colonne[colonne - 1] = 0
        colonne = poids_colonne.index(max(poids_colonne)) + 1
    jouer(colonne)

########################################################################

def position(colonne, ligne):
    """Convertit une position de la grille vers la liste positions[]"""
    position = (colonne-1) + (ligne-1)*NB_COLONNES
    return position

########################################################################

def colonne_extraite(position):
    """Déduit d'une position dans la grille la colonne correspondante"""
    colonne = position % NB_COLONNES + 1
    return colonne

########################################################################

def position_potentielle(colonne, ligne):
    """ """
    test = False
    if colonne >= 1 and colonne <= NB_COLONNES and ligne >= 1 and ligne <= NB_LIGNES:
        if positions[position(colonne, ligne)] == 0: # Position libre
            test = True
            if ligne > 1:
                if positions[position(colonne, ligne - 1)] == 0: # Ligne support inexistante
                    test = False
    return test

########################################################################

def meilleure_position(positionsPotentielles):
    """ """
    POIDS_POSITIONS = [3,4,5,7,5,4,3,4,6,8,10,8,6,4,5,8,11,13,11,8,5,5,8,11,13,11,8,5,4,6,8,10,8,6,4,3,4,5,7,5,4,3]
    poidsMax = 0
    longueurListe = len(positionsPotentielles)
    for i in range(longueurListe):
        if POIDS_POSITIONS[positionsPotentielles[i]] > poidsMax:
            poidsMax = POIDS_POSITIONS[positionsPotentielles[i]]
            iMax = i
    return positionsPotentielles[iMax]

########################################################################

def positions_potentielles(listeAlignements):
    """ """
    positionsPotentielles = []
    if listeAlignements != []:
        nbPions = listeAlignements[0]
        for i in range(0, len(listeAlignements) // 3):
            c = listeAlignements[1 + 3*i] # Colonne
            l = listeAlignements[2 + 3*i] # Ligne
            d = listeAlignements[3 + 3*i] # Direction
            if d == "H": # Horizontal
                if position_potentielle(c - 1, l):
                    positionsPotentielles += [position(c - 1, l)]
                if position_potentielle(c + nbPions, l):
                    positionsPotentielles += [position(c + nbPions, l)]
            if d == "V": # Vertical
                if position_potentielle(c, l + nbPions):
                    positionsPotentielles += [position(c, l + nbPions)]
            if d == "DM": # Diagonale Montante
                if position_potentielle(c - 1, l - 1):
                    positionsPotentielles += [position(c - 1, l - 1)]
                if position_potentielle(c + nbPions, l + nbPions):
                    positionsPotentielles += [position(c + nbPions, l + nbPions)]
            if d == "DD": # Diagonale Descendante
                if position_potentielle(c - 1, l + 1):
                    positionsPotentielles += [position(c - 1, l + 1)]
                if position_potentielle(c + nbPions, l - nbPions):
                    positionsPotentielles += [position(c + nbPions, l - nbPions)]
    colonne = -1
    if len(positionsPotentielles) > 0:
        colonne = colonne_extraite(meilleure_position(positionsPotentielles))
    return colonne

########################################################################

def priorite(nbPions, couleur):
    """ """
    aPuJouer = False
    colonne = positions_potentielles(alignements(nbPions-1, couleur))
    if colonne != -1:
        jouer(colonne)
        aPuJouer = True
    return aPuJouer

########################################################################




########################################################################
# LISTE DES IA
########################################################################

def jouer_ordi_ia0():
    """ """
    jouer_ordi_hasard()                        # H  : L'IA joue au hasard

########################################################################

def jouer_ordi_ia1():
    """ """
    jouer_ordi_poids_cases()                   # P  : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia2():
    """ """
    if priorite(4, couleur): pass              # A4P : L'IA essaye en priorité d'aligner 4 pions
    elif priorite(3, couleur): pass            # A3P : L'IA essaye d'aligner 3 pions
    elif priorite(2, couleur): pass            # A2P : L'IA essaye d'aligner 2 pions
    else: jouer_ordi_poids_cases()             # P  : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia3():
    """ """
    if couleur == 'red':
        couleurAdversaire = 'yellow'
    elif couleur == 'yellow':
        couleurAdversaire = 'red'
    if priorite(4, couleurAdversaire): pass    # B4P : L'IA essaye en priorité d'empêcher l'adversaire d'aligner 4 pions
    elif priorite(3, couleurAdversaire): pass  # B3P : L'IA essaye d'empêcher l'adversaire d'aligner 3 pions
    elif priorite(2, couleurAdversaire): pass  # B2P : L'IA essaye d'empêcher l'adversaire d'aligner 2 pions
    else: jouer_ordi_poids_cases()             # P  : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia4():
    """ """
    if couleur == 'red':
        couleurAdversaire = 'yellow'
    elif couleur == 'yellow':
        couleurAdversaire = 'red'
    if priorite(4, couleur): pass              # A4P : L'IA essaye en priorité d'aligner 4 pions
    elif priorite(4, couleurAdversaire): pass  # B4P : L'IA essaye d'empêcher l'adversaire d'aligner 4 pions
    elif priorite(3, couleur): pass            # A3P : L'IA essaye d'aligner 3 pions
    elif priorite(3, couleurAdversaire): pass  # B3P : L'IA essaye d'empêcher l'adversaire d'aligner 3 pions
    elif priorite(2, couleur): pass            # A2P : L'IA essaye d'aligner 2 pions
    elif priorite(2, couleurAdversaire): pass  # B2P : L'IA essaye d'empêcher l'adversaire d'aligner 2 pions
    else: jouer_ordi_poids_cases()             # P  : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia5():
    """ """
    if couleur == 'red':
        couleurAdversaire = 'yellow'
    elif couleur == 'yellow':
        couleurAdversaire = 'red'
    if priorite(4, couleur): pass              # A4P : L'IA essaye en priorité d'aligner 4 pions
    elif priorite(4, couleurAdversaire): pass  # B4P : L'IA essaye d'empêcher l'adversaire d'aligner 4 pions
    elif priorite(3, couleur): pass            # A3P : L'IA essaye d'aligner 3 pions
    elif priorite(3, couleurAdversaire): pass  # B3P : L'IA essaye d'empêcher l'adversaire d'aligner 3 pions
    elif priorite(2, couleurAdversaire): pass  # B2P : L'IA essaye d'empêcher l'adversaire d'aligner 2 pions
    elif priorite(2, couleur): pass            # A2P : L'IA essaye d'aligner 2 pions
    else: jouer_ordi_poids_cases()             # P  : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia6():
    """ """
    if couleur == 'red':
        couleurAdversaire = 'yellow'
    elif couleur == 'yellow':
        couleurAdversaire = 'red'
    if priorite(4, couleur): pass              # A4P : L'IA essaye en priorité d'aligner 4 pions
    elif priorite(4, couleurAdversaire): pass  # B4P : L'IA essaye d'empêcher l'adversaire d'aligner 4 pions
    elif priorite(3, couleurAdversaire): pass  # B3P : L'IA essaye d'empêcher l'adversaire d'aligner 3 pions
    elif priorite(3, couleur): pass            # A3P : L'IA essaye d'aligner 3 pions
    elif priorite(2, couleur): pass            # A2P : L'IA essaye d'aligner 2 pions
    elif priorite(2, couleurAdversaire): pass  # B2P : L'IA essaye d'empêcher l'adversaire d'aligner 2 pions
    else: jouer_ordi_poids_cases()             # P  : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia7():
    """ """
    if couleur == 'red':
        couleurAdversaire = 'yellow'
    elif couleur == 'yellow':
        couleurAdversaire = 'red'
    if priorite(4, couleur): pass              # A4P : L'IA essaye en priorité d'aligner 4 pions
    elif priorite(4, couleurAdversaire): pass  # B4P : L'IA essaye d'empêcher l'adversaire d'aligner 4 pions
    elif priorite(3, couleurAdversaire): pass  # B3P : L'IA essaye d'empêcher l'adversaire d'aligner 3 pions
    elif priorite(3, couleur): pass            # A3P : L'IA essaye d'aligner 3 pions
    elif priorite(2, couleurAdversaire): pass  # B2P : L'IA essaye d'empêcher l'adversaire d'aligner 2 pions
    elif priorite(2, couleur): pass            # A2P : L'IA essaye d'aligner 2 pions
    else: jouer_ordi_poids_cases()             # P  : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia8():
    """ """
    if couleur == 'red':
        couleurAdversaire = 'yellow'
    elif couleur == 'yellow':
        couleurAdversaire = 'red'
    if priorite(4, couleur): pass              # A4P : L'IA essaye en priorité d'aligner 4 pions
    elif priorite(4, couleurAdversaire): pass  # B4P : L'IA essaye d'empêcher l'adversaire d'aligner 4 pions
    elif priorite(2, couleur): pass            # A2P : L'IA essaye d'aligner 2 pions
    elif priorite(2, couleurAdversaire): pass  # B2P : L'IA essaye d'empêcher l'adversaire d'aligner 2 pions
    else: jouer_ordi_poids_cases()             # P  : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia9():
    """ """
    if couleur == 'red':
        couleurAdversaire = 'yellow'
    elif couleur == 'yellow':
        couleurAdversaire = 'red'
    if priorite(4, couleur): pass              # A4P : L'IA essaye en priorité d'aligner 4 pions
    elif priorite(4, couleurAdversaire): pass  # B4P : L'IA essaye d'empêcher l'adversaire d'aligner 4 pions
    elif priorite(2, couleurAdversaire): pass  # B2P : L'IA essaye d'empêcher l'adversaire d'aligner 2 pions
    elif priorite(2, couleur): pass            # A2P : L'IA essaye d'aligner 2 pions
    else: jouer_ordi_poids_cases()             # P  : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia(ia):
    """ """
    if ia == 0: jouer_ordi_ia0()
    if ia == 1: jouer_ordi_ia1()
    if ia == 2: jouer_ordi_ia2()
    if ia == 3: jouer_ordi_ia3()
    if ia == 4: jouer_ordi_ia4()
    if ia == 5: jouer_ordi_ia5()
    if ia == 6: jouer_ordi_ia6()
    if ia == 7: jouer_ordi_ia7()
    if ia == 8: jouer_ordi_ia8()
    if ia == 9: jouer_ordi_ia9()

########################################################################




########################################################################
# ANALYSE
########################################################################

def positions_gagnantes():
    """Enregistre les positions gagnantes dans une liste"""
    # Pour plus tard...

########################################################################

def analyse_positions():
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
# PARTIE PRINCIPALE
########################################################################

if NB_PARTIES > 1:
    
    # IA JAUNE joue en premier sur la moitié des parties
    finPartie = False
    for i in range(NB_PARTIES // 2):
        couleur = joueur_qui_commence('yellow')
        affiche_joueur_qui_commence()
        while not finPartie:
            jouer_ordi_ia(IA_JAUNE)
            finPartie = fin_partie()  # Teste si la partie est finie
            if not finPartie:
                jouer_ordi_ia(IA_ROUGE)
                finPartie = fin_partie()  # Teste si la partie est finie
        analyse_positions()
        affiche_statistiques_console()
        initialise_liste_positions()
        finPartie = False
        # Dans la fenêtre graphique
        fenetreJeu.update()
        # Pause en seconde
        time.sleep(TEMPS_PAUSE)
        if NB_PARTIES == 2:
            time.sleep(TEMPS_PAUSE *9)  # Pour pouvoir faire une copie écran
        # Dans la fenêtre graphique
        destruction_jetons()
        efface_message_fenetre()
        fenetreJeu.update()
        # Pause en seconde
        time.sleep(TEMPS_PAUSE)

    # IA ROUGE joue en premier sur l'autre moitié des parties
    finPartie = False
    for i in range(NB_PARTIES // 2):
        couleur = joueur_qui_commence('red')
        affiche_joueur_qui_commence()
        while not finPartie:
            jouer_ordi_ia(IA_ROUGE)
            finPartie = fin_partie()  # Teste si la partie est finie
            if not finPartie:
                jouer_ordi_ia(IA_JAUNE)
                finPartie = fin_partie()  # Teste si la partie est finie
        analyse_positions()
        affiche_statistiques_console()
        initialise_liste_positions()
        finPartie = False
        # Dans la fenêtre graphique
        fenetreJeu.update()
        # Pause en seconde
        time.sleep(TEMPS_PAUSE)
        if NB_PARTIES == 2:
            time.sleep(TEMPS_PAUSE *9)  # Pour pouvoir faire une copie écran
        # Dans la fenêtre graphique
        destruction_jetons()
        efface_message_fenetre()
        fenetreJeu.update()
        # Pause en seconde
        time.sleep(TEMPS_PAUSE)

# Démarrage du réceptionnaire d'évènements (boucle principale) :
fenetreJeu.mainloop()

########################################################################


