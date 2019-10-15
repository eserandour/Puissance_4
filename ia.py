# -*- coding: utf-8 -*-
"""
########################################################################
#  Version du 15 octobre 2019 à 14 h 01
########################################################################
"""

from constantes import NB_COLONNES, NB_LIGNES, ALIGNEMENT
from commun import alignements, colonne_pleine, jouer, inverse
import random




########################################################################
# STRATEGIES DE JEU
########################################################################

def jouer_ordi_hasard(positions, couleur):
    """L'ordinateur joue au hasard"""
    colonne = random.randint(1, NB_COLONNES)
    while colonne_pleine(positions, colonne):
        colonne = random.randint(1, NB_COLONNES)
    return jouer(positions, couleur, colonne)

########################################################################

def poids_cases(nbPions):
    """Calcule le poids des cases"""
    """[3,4,5,7,5,4,3,4,6,8,10,8,6,4,5,8,11,13,11,8,5,5,8,11,13,11,8,5,4,6,8,10,8,6,4,3,4,5,7,5,4,3] pour une grille 7x6"""
    positions = [0] * NB_COLONNES*NB_LIGNES
    # Sur les horizontales
    for j in range(NB_LIGNES):
        for i in range(NB_COLONNES-nbPions+1):
            for k in range(nbPions):
                positions[NB_COLONNES*j+i+k] += 1
    # Sur les verticales
    for j in range(NB_LIGNES-nbPions+1):
        for i in range(NB_COLONNES):
            for k in range(nbPions):
                positions[NB_COLONNES*j+i+k*NB_COLONNES] += 1
    # Sur les diagonales montantes
    for j in range(NB_LIGNES-nbPions+1):
        for i in range(NB_COLONNES-nbPions+1):
            for k in range(nbPions):
                positions[NB_COLONNES*j+i+k*NB_COLONNES+k] += 1
    # Sur les diagonales descendantes
    for j in range(nbPions-1, NB_LIGNES):
        for i in range(NB_COLONNES-nbPions+1):
            for k in range(nbPions):
                positions[NB_COLONNES*j+i-k*NB_COLONNES+k] += 1
    return positions

########################################################################

def liste_indices_maximum(liste):
    """Renvoie les indices des maximums d'une liste"""
    maxi = max(liste)
    longueur = len(liste)
    indices = []
    for i in range(longueur):
        if liste[i] == maxi:
            indices += [i]
    return indices

########################################################################

def jouer_ordi_poids_cases(positions, couleur):
    """L'ordinateur joue en ne tenant compte que du poids des cases de la grille potentiellement victorieuses"""
    poidsCases = poids_cases(ALIGNEMENT)
    poidsColonnes = [0] * NB_COLONNES
    for colonne in range(1, NB_COLONNES + 1):
        if not colonne_pleine(positions, colonne):
            position = colonne - 1
            while positions[position]:
                position += NB_COLONNES
            poidsColonnes[colonne - 1] += poidsCases[position]
        else:
            poidsColonnes[colonne - 1] += 0
    indicesPoidsMaximum = liste_indices_maximum(poidsColonnes)
    # Si plusieurs cases sont possibles (même poids), on tire au hasard
    colonne = 1 + random.choice(indicesPoidsMaximum)
    return jouer(positions, couleur, colonne)

########################################################################
""" ANCIENNE VERSION (SANS HASARD EN CAS D'EGALITE DE POIDS)
def jouer_ordi_poids_cases(positions, couleur):
    "L'ordinateur joue en ne tenant compte que du poids des cases de la grille (7x6) potentiellement victorieuses"
    POIDS_POSITIONS = [3,4,5,7,5,4,3,4,6,8,10,8,6,4,5,8,11,13,11,8,5,5,8,11,13,11,8,5,4,6,8,10,8,6,4,3,4,5,7,5,4,3]
    poidsColonne = [0] * NB_COLONNES
    for colonne in range(1, NB_COLONNES + 1):
        if not colonne_pleine(positions, colonne):
            position = colonne - 1
            while positions[position]:
                position += NB_COLONNES
            poidsColonne[colonne - 1] = POIDS_POSITIONS[position]
        else:
            poidsColonne[colonne - 1] = 0
        colonne = poidsColonne.index(max(poidsColonne)) + 1
    return jouer(positions, couleur, colonne)
"""
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

def position_potentielle(positions, colonne, ligne):
    """ """
    test = False
    if colonne >= 1 and colonne <= NB_COLONNES and ligne >= 1 and ligne <= NB_LIGNES:
        if positions[position(colonne, ligne)] == 0:  # Position libre
            test = True
            if ligne > 1:
                if positions[position(colonne, ligne - 1)] == 0:  # Ligne support inexistante
                    test = False
    return test

########################################################################

def meilleure_position(positionsPotentielles):
    """ """
    # Calcule le poids des cases
    poidsCases = poids_cases(ALIGNEMENT)
    # Détermine le poids des positions potentielles
    poidsPositionsPotentielles = []
    for i in range(len(positionsPotentielles)):
        poidsPositionsPotentielles += [poidsCases[positionsPotentielles[i]]]
    # Détermine les indices du poids maximum dans la liste ci-dessus
    indicesPoidsMaximum = liste_indices_maximum(poidsPositionsPotentielles)
    # Extrait les meilleures positions potentielles (celles qui ont un poids maximum)
    meilleuresPositionsPotentielles = []
    for i in range(len(indicesPoidsMaximum)):
        meilleuresPositionsPotentielles += [positionsPotentielles[indicesPoidsMaximum[i]]]
    # Si plusieurs positions sont possibles (même poids), on tire au hasard
    meilleurePosition = random.choice(meilleuresPositionsPotentielles)
    return meilleurePosition

########################################################################
""" ANCIENNE VERSION (SANS HASARD EN CAS D'EGALITE DE POIDS)
def meilleure_position(positionsPotentielles):
    ""
    POIDS_POSITIONS = [3,4,5,7,5,4,3,4,6,8,10,8,6,4,5,8,11,13,11,8,5,5,8,11,13,11,8,5,4,6,8,10,8,6,4,3,4,5,7,5,4,3]
    poidsMax = 0
    longueurListe = len(positionsPotentielles)
    for i in range(longueurListe):
        if POIDS_POSITIONS[positionsPotentielles[i]] > poidsMax:
            poidsMax = POIDS_POSITIONS[positionsPotentielles[i]]
            iMax = i
    return positionsPotentielles[iMax]
"""
########################################################################

def positions_potentielles(positions, listeAlignements):
    """ """
    positionsPotentielles = []
    if listeAlignements != []:
        nbPions = listeAlignements[0]
        for i in range(0, len(listeAlignements) // 3):
            c = listeAlignements[1 + 3*i] # Colonne
            l = listeAlignements[2 + 3*i] # Ligne
            d = listeAlignements[3 + 3*i] # Direction
            if d == "H": # Horizontal
                if position_potentielle(positions, c - 1, l):
                    positionsPotentielles += [position(c - 1, l)]
                if position_potentielle(positions, c + nbPions, l):
                    positionsPotentielles += [position(c + nbPions, l)]
            if d == "V": # Vertical
                if position_potentielle(positions, c, l + nbPions):
                    positionsPotentielles += [position(c, l + nbPions)]
            if d == "DM": # Diagonale Montante
                if position_potentielle(positions, c - 1, l - 1):
                    positionsPotentielles += [position(c - 1, l - 1)]
                if position_potentielle(positions, c + nbPions, l + nbPions):
                    positionsPotentielles += [position(c + nbPions, l + nbPions)]
            if d == "DD": # Diagonale Descendante
                if position_potentielle(positions, c - 1, l + 1):
                    positionsPotentielles += [position(c - 1, l + 1)]
                if position_potentielle(positions, c + nbPions, l - nbPions):
                    positionsPotentielles += [position(c + nbPions, l - nbPions)]
    colonne = -1
    if len(positionsPotentielles) > 0:
        colonne = colonne_extraite(meilleure_position(positionsPotentielles))
    return colonne

########################################################################

def priorite(positions, nbPions, couleur):
    """Retourne une colonne où jouer"""
    listeAlignements = alignements(positions, nbPions-1, couleur)
    return positions_potentielles(positions, listeAlignements)

########################################################################




########################################################################
# LISTE DES IA
########################################################################

def jouer_ordi_ia0(positions, couleur):
    """ """
    return jouer_ordi_hasard(positions, couleur)                    # H  : L'IA joue au hasard

########################################################################

def jouer_ordi_ia1(positions, couleur):
    """ """
    return jouer_ordi_poids_cases(positions, couleur)               # P  : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia2(positions, couleur):
    """ """
    colA4P = priorite(positions, 4, couleur)
    colA3P = priorite(positions, 3, couleur)
    colA2P = priorite(positions, 2, couleur)
    if colA4P != -1: return jouer(positions, couleur, colA4P)      # A4P : L'IA essaye en priorité d'aligner 4 pions
    elif colA3P != -1: return jouer(positions, couleur, colA3P)    # A3P : L'IA essaye d'aligner 3 pions
    elif colA2P != -1: return jouer(positions, couleur, colA2P)    # A2P : L'IA essaye d'aligner 2 pions
    else: return jouer_ordi_poids_cases(positions, couleur)        # P   : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia3(positions, couleur):
    """ """
    couleurAdversaire = inverse(couleur)
    colB4P = priorite(positions, 4, couleurAdversaire)
    colB3P = priorite(positions, 3, couleurAdversaire)
    colB2P = priorite(positions, 2, couleurAdversaire)
    if colB4P != -1: return jouer(positions, couleur, colB4P)      # B4P : L'IA essaye en priorité d'empêcher l'adversaire d'aligner 4 pions
    elif colB3P != -1: return jouer(positions, couleur, colB3P)    # B3P : L'IA essaye d'empêcher l'adversaire d'aligner 3 pions
    elif colB2P != -1: return jouer(positions, couleur, colB2P)    # B2P : L'IA essaye d'empêcher l'adversaire d'aligner 2 pions
    else: return jouer_ordi_poids_cases(positions, couleur)        # P   : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia4(positions, couleur):
    """ """
    colA4P = priorite(positions, 4, couleur)
    colA3P = priorite(positions, 3, couleur)
    colA2P = priorite(positions, 2, couleur)
    couleurAdversaire = inverse(couleur)
    colB4P = priorite(positions, 4, couleurAdversaire)
    colB3P = priorite(positions, 3, couleurAdversaire)
    colB2P = priorite(positions, 2, couleurAdversaire)
    if colA4P != -1: return jouer(positions, couleur, colA4P)      # A4P : L'IA essaye en priorité d'aligner 4 pions
    elif colB4P != -1: return jouer(positions, couleur, colB4P)    # B4P : L'IA essaye en d'empêcher l'adversaire d'aligner 4 pions
    elif colA3P != -1: return jouer(positions, couleur, colA3P)    # A3P : L'IA essaye d'aligner 3 pions
    elif colB3P != -1: return jouer(positions, couleur, colB3P)    # B3P : L'IA essaye d'empêcher l'adversaire d'aligner 3 pions
    elif colA2P != -1: return jouer(positions, couleur, colA2P)    # A2P : L'IA essaye d'aligner 2 pions
    elif colB2P != -1: return jouer(positions, couleur, colB2P)    # B2P : L'IA essaye d'empêcher l'adversaire d'aligner 2 pions
    else: return jouer_ordi_poids_cases(positions, couleur)        # P   : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia5(positions, couleur):
    """ """
    colA4P = priorite(positions, 4, couleur)
    colA3P = priorite(positions, 3, couleur)
    colA2P = priorite(positions, 2, couleur)
    couleurAdversaire = inverse(couleur)
    colB4P = priorite(positions, 4, couleurAdversaire)
    colB3P = priorite(positions, 3, couleurAdversaire)
    colB2P = priorite(positions, 2, couleurAdversaire)
    if colA4P != -1: return jouer(positions, couleur, colA4P)      # A4P : L'IA essaye en priorité d'aligner 4 pions
    elif colB4P != -1: return jouer(positions, couleur, colB4P)    # B4P : L'IA essaye en d'empêcher l'adversaire d'aligner 4 pions
    elif colA3P != -1: return jouer(positions, couleur, colA3P)    # A3P : L'IA essaye d'aligner 3 pions
    elif colB3P != -1: return jouer(positions, couleur, colB3P)    # B3P : L'IA essaye d'empêcher l'adversaire d'aligner 3 pions
    elif colB2P != -1: return jouer(positions, couleur, colB2P)    # B2P : L'IA essaye d'empêcher l'adversaire d'aligner 2 pions
    elif colA2P != -1: return jouer(positions, couleur, colA2P)    # A2P : L'IA essaye d'aligner 2 pions
    else: return jouer_ordi_poids_cases(positions, couleur)        # P   : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia6(positions, couleur):
    """ """
    colA4P = priorite(positions, 4, couleur)
    colA3P = priorite(positions, 3, couleur)
    colA2P = priorite(positions, 2, couleur)
    couleurAdversaire = inverse(couleur)
    colB4P = priorite(positions, 4, couleurAdversaire)
    colB3P = priorite(positions, 3, couleurAdversaire)
    colB2P = priorite(positions, 2, couleurAdversaire)
    if colA4P != -1: return jouer(positions, couleur, colA4P)      # A4P : L'IA essaye en priorité d'aligner 4 pions
    elif colB4P != -1: return jouer(positions, couleur, colB4P)    # B4P : L'IA essaye en d'empêcher l'adversaire d'aligner 4 pions
    elif colB3P != -1: return jouer(positions, couleur, colB3P)    # B3P : L'IA essaye d'empêcher l'adversaire d'aligner 3 pions
    elif colA3P != -1: return jouer(positions, couleur, colA3P)    # A3P : L'IA essaye d'aligner 3 pions
    elif colA2P != -1: return jouer(positions, couleur, colA2P)    # A2P : L'IA essaye d'aligner 2 pions
    elif colB2P != -1: return jouer(positions, couleur, colB2P)    # B2P : L'IA essaye d'empêcher l'adversaire d'aligner 2 pions
    else: return jouer_ordi_poids_cases(positions, couleur)        # P   : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia7(positions, couleur):
    """ """
    colA4P = priorite(positions, 4, couleur)
    colA3P = priorite(positions, 3, couleur)
    colA2P = priorite(positions, 2, couleur)
    couleurAdversaire = inverse(couleur)
    colB4P = priorite(positions, 4, couleurAdversaire)
    colB3P = priorite(positions, 3, couleurAdversaire)
    colB2P = priorite(positions, 2, couleurAdversaire)
    if colA4P != -1: return jouer(positions, couleur, colA4P)      # A4P : L'IA essaye en priorité d'aligner 4 pions
    elif colB4P != -1: return jouer(positions, couleur, colB4P)    # B4P : L'IA essaye en d'empêcher l'adversaire d'aligner 4 pions
    elif colB3P != -1: return jouer(positions, couleur, colB3P)    # B3P : L'IA essaye d'empêcher l'adversaire d'aligner 3 pions
    elif colA3P != -1: return jouer(positions, couleur, colA3P)    # A3P : L'IA essaye d'aligner 3 pions
    elif colB2P != -1: return jouer(positions, couleur, colB2P)    # B2P : L'IA essaye d'empêcher l'adversaire d'aligner 2 pions
    elif colA2P != -1: return jouer(positions, couleur, colA2P)    # A2P : L'IA essaye d'aligner 2 pions
    else: return jouer_ordi_poids_cases(positions, couleur)        # P   : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia8(positions, couleur):
    """ """
    colA4P = priorite(positions, 4, couleur)
    colA2P = priorite(positions, 2, couleur)
    couleurAdversaire = inverse(couleur)
    colB4P = priorite(positions, 4, couleurAdversaire)
    colB2P = priorite(positions, 2, couleurAdversaire)
    if colA4P != -1: return jouer(positions, couleur, colA4P)      # A4P : L'IA essaye en priorité d'aligner 4 pions
    elif colB4P != -1: return jouer(positions, couleur, colB4P)    # B4P : L'IA essaye en d'empêcher l'adversaire d'aligner 4 pions
    elif colA2P != -1: return jouer(positions, couleur, colA2P)    # A2P : L'IA essaye d'aligner 2 pions
    elif colB2P != -1: return jouer(positions, couleur, colB2P)    # B2P : L'IA essaye d'empêcher l'adversaire d'aligner 2 pions
    else: return jouer_ordi_poids_cases(positions, couleur)        # P   : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia9(positions, couleur):
    """ """
    colA4P = priorite(positions, 4, couleur)
    colA2P = priorite(positions, 2, couleur)
    couleurAdversaire = inverse(couleur)
    colB4P = priorite(positions, 4, couleurAdversaire)
    colB2P = priorite(positions, 2, couleurAdversaire)
    if colA4P != -1: return jouer(positions, couleur, colA4P)      # A4P : L'IA essaye en priorité d'aligner 4 pions
    elif colB4P != -1: return jouer(positions, couleur, colB4P)    # B4P : L'IA essaye en d'empêcher l'adversaire d'aligner 4 pions
    elif colB2P != -1: return jouer(positions, couleur, colB2P)    # B2P : L'IA essaye d'empêcher l'adversaire d'aligner 2 pions
    elif colA2P != -1: return jouer(positions, couleur, colA2P)    # A2P : L'IA essaye d'aligner 2 pions
    else: return jouer_ordi_poids_cases(positions, couleur)        # P   : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia(positions, couleur, ia):
    """ """
    if ia == 0: positions = jouer_ordi_ia0(positions, couleur)
    if ia == 1: positions = jouer_ordi_ia1(positions, couleur)
    if ia == 2: positions = jouer_ordi_ia2(positions, couleur)
    if ia == 3: positions = jouer_ordi_ia3(positions, couleur)
    if ia == 4: positions = jouer_ordi_ia4(positions, couleur)
    if ia == 5: positions = jouer_ordi_ia5(positions, couleur)
    if ia == 6: positions = jouer_ordi_ia6(positions, couleur)
    if ia == 7: positions = jouer_ordi_ia7(positions, couleur)
    if ia == 8: positions = jouer_ordi_ia8(positions, couleur)
    if ia == 9: positions = jouer_ordi_ia9(positions, couleur)
    return positions

########################################################################
