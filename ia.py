# -*- coding: utf-8 -*-
"""
########################################################################
#  Version du 30 juillet 2020 à 12 h 51
########################################################################
"""

from constantes import NB_COLONNES, NB_LIGNES, ALIGNEMENT
from commun import alignements_pleins, alignements_troues, colonne_pleine, jouer, inverse
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
    """Calcule le poids des cases en fonction de la dimension de la grille et du nombre de pions à aligner pour gagner"""
    """[3,4,5,7,5,4,3,4,6,8,10,8,6,4,5,8,11,13,11,8,5,5,8,11,13,11,8,5,4,6,8,10,8,6,4,3,4,5,7,5,4,3] pour une grille 7x6 avec 4 pions à aligner"""
    poids = [0] * NB_COLONNES*NB_LIGNES
    # Sur les horizontales
    for j in range(NB_LIGNES):
        for i in range(NB_COLONNES-nbPions+1):
            for k in range(nbPions):
                poids[NB_COLONNES*j+i+k] += 1
    # Sur les verticales
    for j in range(NB_LIGNES-nbPions+1):
        for i in range(NB_COLONNES):
            for k in range(nbPions):
                poids[NB_COLONNES*j+i+k*NB_COLONNES] += 1
    # Sur les diagonales montantes
    for j in range(NB_LIGNES-nbPions+1):
        for i in range(NB_COLONNES-nbPions+1):
            for k in range(nbPions):
                poids[NB_COLONNES*j+i+k*NB_COLONNES+k] += 1
    # Sur les diagonales descendantes
    for j in range(nbPions-1, NB_LIGNES):
        for i in range(NB_COLONNES-nbPions+1):
            for k in range(nbPions):
                poids[NB_COLONNES*j+i-k*NB_COLONNES+k] += 1
    return poids

########################################################################

def liste_indices_maximum(liste):
    """Renvoie les indices des maximums d'une liste"""
    maxi = max(liste)
    indices = []
    for i in range(len(liste)):
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
    # Si plusieurs colonnes sont possibles (même poids), on tire au hasard une colonne
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
    """Déduit d'une position dans la grille une position dans la liste positions[]"""
    position = (colonne-1) + (ligne-1)*NB_COLONNES
    return position

########################################################################

def colonne_extraite(position):
    """Déduit d'une position dans la grille la colonne correspondante"""
    colonne = position % NB_COLONNES + 1
    return colonne

########################################################################

def position_potentielle(positions, colonne, ligne):
    """Teste si une position est possible (case vide et support pour soutenir le pion)"""
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
    """Détermine la meilleure position en s'appuyant sur le poids des cases"""
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
    # Si plusieurs positions sont possibles (même poids), on tire au hasard une position
    return random.choice(meilleuresPositionsPotentielles)

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

def positions_potentielles(positions, listeAlignementsTroues):
    """Retourne une colonne où jouer à partir de l'ensemble des positions potentielles"""
    positionsPotentielles = []
    if listeAlignementsTroues != []:
        nbPions = listeAlignementsTroues[0]
        for i in range(0, len(listeAlignementsTroues) // 3):
            c = listeAlignementsTroues[1 + 3*i] # Colonne
            l = listeAlignementsTroues[2 + 3*i] # Ligne
            d = listeAlignementsTroues[3 + 3*i] # Direction
            if d == "H": # Horizontal
                for j in range(nbPions + 1):
                    if position_potentielle(positions, c + j, l):
                        positionsPotentielles += [position(c + j, l)]
            if d == "V": # Vertical
                if position_potentielle(positions, c, l + nbPions):
                    positionsPotentielles += [position(c, l + nbPions)]
            if d == "DM": # Diagonale Montante
                for j in range(nbPions + 1):
                    if position_potentielle(positions, c + j, l + j):
                        positionsPotentielles += [position(c + j, l + j)]
            if d == "DD": # Diagonale Descendante
                for j in range(nbPions + 1):
                    if position_potentielle(positions, c + j, l - j):
                        positionsPotentielles += [position(c + j, l - j)]
    colonne = -1
    if len(positionsPotentielles) > 0:
        colonne = colonne_extraite(meilleure_position(positionsPotentielles))
    return colonne

########################################################################

def priorite_pleine(positions, nbPions, couleur):
    """Retourne une colonne où jouer"""
    listeAlignementsPleins = alignements_pleins(positions, nbPions-1, couleur)
    return positions_potentielles(positions, listeAlignementsPleins)

########################################################################

def priorite_trouee(positions, nbPions, couleur):
    """Retourne une colonne où jouer"""
    listeAlignementsTroues = alignements_troues(positions, nbPions-1, couleur)
    return positions_potentielles(positions, listeAlignementsTroues)

########################################################################




########################################################################
# LISTE DES IA
########################################################################

def jouer_ordi_ia0(positions, couleur):
    """IA0 joue"""
    return jouer_ordi_hasard(positions, couleur)                     # H   : L'IA joue au hasard

########################################################################

def jouer_ordi_ia1(positions, couleur):
    """IA1 joue"""
    return jouer_ordi_poids_cases(positions, couleur)                # PH  : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia2(positions, couleur):                              # Priorité Alignements Pleins
    """IA2 joue"""
    colA4PH = priorite_pleine(positions, 4, couleur)
    colA3PH = priorite_pleine(positions, 3, couleur)
    colA2PH = priorite_pleine(positions, 2, couleur)
    if colA4PH != -1: return jouer(positions, couleur, colA4PH)      # A4PH : L'IA essaye en priorité d'aligner 4 pions
    elif colA3PH != -1: return jouer(positions, couleur, colA3PH)    # A3PH : L'IA essaye d'aligner 3 pions
    elif colA2PH != -1: return jouer(positions, couleur, colA2PH)    # A2PH : L'IA essaye d'aligner 2 pions
    else: return jouer_ordi_poids_cases(positions, couleur)          # PH   : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia3(positions, couleur):                              # Priorité Alignements Pleins
    """IA3 joue"""
    couleurAdversaire = inverse(couleur)
    colB4PH = priorite_pleine(positions, 4, couleurAdversaire)
    colB3PH = priorite_pleine(positions, 3, couleurAdversaire)
    colB2PH = priorite_pleinee(positions, 2, couleurAdversaire)
    if colB4PH != -1: return jouer(positions, couleur, colB4PH)      # B4PH : L'IA essaye en priorité d'empêcher l'adversaire d'aligner 4 pions
    elif colB3PH != -1: return jouer(positions, couleur, colB3PH)    # B3PH : L'IA essaye d'empêcher l'adversaire d'aligner 3 pions
    elif colB2PH != -1: return jouer(positions, couleur, colB2PH)    # B2PH : L'IA essaye d'empêcher l'adversaire d'aligner 2 pions
    else: return jouer_ordi_poids_cases(positions, couleur)          # PH   : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia4(positions, couleur):                              # Priorité Alignements Pleins
    """IA4 joue"""
    colA4PH = priorite_pleine(positions, 4, couleur)
    colA3PH = priorite_pleine(positions, 3, couleur)
    colA2PH = priorite_pleine(positions, 2, couleur)
    couleurAdversaire = inverse(couleur)
    colB4PH = priorite_pleine(positions, 4, couleurAdversaire)
    colB3PH = priorite_pleine(positions, 3, couleurAdversaire)
    colB2PH = priorite_pleine(positions, 2, couleurAdversaire)
    if colA4PH != -1: return jouer(positions, couleur, colA4PH)      # A4PH : L'IA essaye en priorité d'aligner 4 pions
    elif colB4PH != -1: return jouer(positions, couleur, colB4PH)    # B4PH : L'IA essaye d'empêcher l'adversaire d'aligner 4 pions
    elif colA3PH != -1: return jouer(positions, couleur, colA3PH)    # A3PH : L'IA essaye d'aligner 3 pions
    elif colB3PH != -1: return jouer(positions, couleur, colB3PH)    # B3PH : L'IA essaye d'empêcher l'adversaire d'aligner 3 pions
    elif colA2PH != -1: return jouer(positions, couleur, colA2PH)    # A2PH : L'IA essaye d'aligner 2 pions
    elif colB2PH != -1: return jouer(positions, couleur, colB2PH)    # B2PH : L'IA essaye d'empêcher l'adversaire d'aligner 2 pions
    else: return jouer_ordi_poids_cases(positions, couleur)          # PH   : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia5(positions, couleur):                              # Priorité Alignements Pleins
    """IA5 joue"""
    colA4PH = priorite_pleine(positions, 4, couleur)
    colA3PH = priorite_pleine(positions, 3, couleur)
    colA2PH = priorite_pleine(positions, 2, couleur)
    couleurAdversaire = inverse(couleur)
    colB4PH = priorite_pleine(positions, 4, couleurAdversaire)
    colB3PH = priorite_pleine(positions, 3, couleurAdversaire)
    colB2PH = priorite_pleine(positions, 2, couleurAdversaire)
    if colA4PH != -1: return jouer(positions, couleur, colA4PH)      # A4PH : L'IA essaye en priorité d'aligner 4 pions
    elif colB4PH != -1: return jouer(positions, couleur, colB4PH)    # B4PH : L'IA essaye d'empêcher l'adversaire d'aligner 4 pions
    elif colA3PH != -1: return jouer(positions, couleur, colA3PH)    # A3PH : L'IA essaye d'aligner 3 pions
    elif colB3PH != -1: return jouer(positions, couleur, colB3PH)    # B3PH : L'IA essaye d'empêcher l'adversaire d'aligner 3 pions
    elif colB2PH != -1: return jouer(positions, couleur, colB2PH)    # B2PH : L'IA essaye d'empêcher l'adversaire d'aligner 2 pions
    elif colA2PH != -1: return jouer(positions, couleur, colA2PH)    # A2PH : L'IA essaye d'aligner 2 pions
    else: return jouer_ordi_poids_cases(positions, couleur)          # PH   : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia6(positions, couleur):                              # Priorité Alignements Pleins
    """IA6 joue"""
    colA4PH = priorite_pleine(positions, 4, couleur)
    colA3PH = priorite_pleine(positions, 3, couleur)
    colA2PH = priorite_pleine(positions, 2, couleur)
    couleurAdversaire = inverse(couleur)
    colB4PH = priorite_pleine(positions, 4, couleurAdversaire)
    colB3PH = priorite_pleine(positions, 3, couleurAdversaire)
    colB2PH = priorite_pleine(positions, 2, couleurAdversaire)
    if colA4PH != -1: return jouer(positions, couleur, colA4PH)      # A4PH : L'IA essaye en priorité d'aligner 4 pions
    elif colB4PH != -1: return jouer(positions, couleur, colB4PH)    # B4PH : L'IA essaye d'empêcher l'adversaire d'aligner 4 pions
    elif colB3PH != -1: return jouer(positions, couleur, colB3PH)    # B3PH : L'IA essaye d'empêcher l'adversaire d'aligner 3 pions
    elif colA3PH != -1: return jouer(positions, couleur, colA3PH)    # A3PH : L'IA essaye d'aligner 3 pions
    elif colA2PH != -1: return jouer(positions, couleur, colA2PH)    # A2PH : L'IA essaye d'aligner 2 pions
    elif colB2PH != -1: return jouer(positions, couleur, colB2PH)    # B2PH : L'IA essaye d'empêcher l'adversaire d'aligner 2 pions
    else: return jouer_ordi_poids_cases(positions, couleur)          # PH   : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia7(positions, couleur):                              # Priorité Alignements Pleins
    """IA7 joue"""
    colA4PH = priorite_pleine(positions, 4, couleur)
    colA3PH = priorite_pleine(positions, 3, couleur)
    colA2PH = priorite_pleine(positions, 2, couleur)
    couleurAdversaire = inverse(couleur)
    colB4PH = priorite_pleine(positions, 4, couleurAdversaire)
    colB3PH = priorite_pleine(positions, 3, couleurAdversaire)
    colB2PH = priorite_pleine(positions, 2, couleurAdversaire)
    if colA4PH != -1: return jouer(positions, couleur, colA4PH)      # A4PH : L'IA essaye en priorité d'aligner 4 pions
    elif colB4PH != -1: return jouer(positions, couleur, colB4PH)    # B4PH : L'IA essaye d'empêcher l'adversaire d'aligner 4 pions
    elif colB3PH != -1: return jouer(positions, couleur, colB3PH)    # B3PH : L'IA essaye d'empêcher l'adversaire d'aligner 3 pions
    elif colA3PH != -1: return jouer(positions, couleur, colA3PH)    # A3PH : L'IA essaye d'aligner 3 pions
    elif colB2PH != -1: return jouer(positions, couleur, colB2PH)    # B2PH : L'IA essaye d'empêcher l'adversaire d'aligner 2 pions
    elif colA2PH != -1: return jouer(positions, couleur, colA2PH)    # A2PH : L'IA essaye d'aligner 2 pions
    else: return jouer_ordi_poids_cases(positions, couleur)          # PH   : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia8(positions, couleur):                              # Priorité Alignements Pleins
    """IA8 joue"""
    colA4PH = priorite_pleine(positions, 4, couleur)
    colA2PH = priorite_pleine(positions, 2, couleur)
    couleurAdversaire = inverse(couleur)
    colB4PH = priorite_pleine(positions, 4, couleurAdversaire)
    colB2PH = priorite_pleine(positions, 2, couleurAdversaire)
    if colA4PH != -1: return jouer(positions, couleur, colA4PH)      # A4PH : L'IA essaye en priorité d'aligner 4 pions
    elif colB4PH != -1: return jouer(positions, couleur, colB4PH)    # B4PH : L'IA essaye d'empêcher l'adversaire d'aligner 4 pions
    elif colA2PH != -1: return jouer(positions, couleur, colA2PH)    # A2PH : L'IA essaye d'aligner 2 pions
    elif colB2PH != -1: return jouer(positions, couleur, colB2PH)    # B2PH : L'IA essaye d'empêcher l'adversaire d'aligner 2 pions
    else: return jouer_ordi_poids_cases(positions, couleur)          # PH   : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia9(positions, couleur):                              # Priorité Alignements Pleins
    """IA9 joue"""
    colA4PH = priorite_pleine(positions, 4, couleur)
    colA2PH = priorite_pleine(positions, 2, couleur)
    couleurAdversaire = inverse(couleur)
    colB4PH = priorite_pleine(positions, 4, couleurAdversaire)
    colB2PH = priorite_pleine(positions, 2, couleurAdversaire)
    if colA4PH != -1: return jouer(positions, couleur, colA4PH)      # A4PH : L'IA essaye en priorité d'aligner 4 pions
    elif colB4PH != -1: return jouer(positions, couleur, colB4PH)    # B4PH : L'IA essaye d'empêcher l'adversaire d'aligner 4 pions
    elif colB2PH != -1: return jouer(positions, couleur, colB2PH)    # B2PH : L'IA essaye d'empêcher l'adversaire d'aligner 2 pions
    elif colA2PH != -1: return jouer(positions, couleur, colA2PH)    # A2PH : L'IA essaye d'aligner 2 pions
    else: return jouer_ordi_poids_cases(positions, couleur)          # PH   : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia10(positions, couleur):                             # Priorité Alignements Pleins
    """IA10 joue"""
    colA4PH = priorite_pleine(positions, 4, couleur)
    colA3PH = priorite_pleine(positions, 3, couleur)
    colA2PH = priorite_pleine(positions, 2, couleur)
    couleurAdversaire = inverse(couleur)
    colB4PH = priorite_pleine(positions, 4, couleurAdversaire)
    colB3PH = priorite_pleine(positions, 3, couleurAdversaire)
    colB2PH = priorite_pleine(positions, 2, couleurAdversaire)
    if colA4PH != -1: return jouer(positions, couleur, colA4PH)      # A4PH : L'IA essaye en priorité d'aligner 4 pions
    elif colB4PH != -1: return jouer(positions, couleur, colB4PH)    # B4PH : L'IA essaye d'empêcher l'adversaire d'aligner 4 pions
    elif colB3PH != -1: return jouer(positions, couleur, colB3PH)    # B3PH : L'IA essaye d'empêcher l'adversaire d'aligner 3 pions
    elif colB2PH != -1: return jouer(positions, couleur, colB2PH)    # B2PH : L'IA essaye d'empêcher l'adversaire d'aligner 2 pions
    elif colA3PH != -1: return jouer(positions, couleur, colA3PH)    # A3PH : L'IA essaye d'aligner 3 pions
    elif colA2PH != -1: return jouer(positions, couleur, colA2PH)    # A2PH : L'IA essaye d'aligner 2 pions
    else: return jouer_ordi_poids_cases(positions, couleur)          # PH   : L'IA joue dans la case qui a le plus de poids

########################################################################

# Pas d'IA 11

########################################################################

def jouer_ordi_ia12(positions, couleur):                            # Priorité Alignements Troués
    """IA2 joue"""
    colA4PH = priorite_trouee(positions, 4, couleur)
    colA3PH = priorite_trouee(positions, 3, couleur)
    colA2PH = priorite_trouee(positions, 2, couleur)
    if colA4PH != -1: return jouer(positions, couleur, colA4PH)      # A4PH : L'IA essaye en priorité d'aligner 4 pions
    elif colA3PH != -1: return jouer(positions, couleur, colA3PH)    # A3PH : L'IA essaye d'aligner 3 pions
    elif colA2PH != -1: return jouer(positions, couleur, colA2PH)    # A2PH : L'IA essaye d'aligner 2 pions
    else: return jouer_ordi_poids_cases(positions, couleur)          # PH   : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia13(positions, couleur):                             # Priorité Alignements Troués
    """IA3 joue"""
    couleurAdversaire = inverse(couleur)
    colB4PH = priorite_trouee(positions, 4, couleurAdversaire)
    colB3PH = priorite_trouee(positions, 3, couleurAdversaire)
    colB2PH = priorite_trouee(positions, 2, couleurAdversaire)
    if colB4PH != -1: return jouer(positions, couleur, colB4PH)      # B4PH : L'IA essaye en priorité d'empêcher l'adversaire d'aligner 4 pions
    elif colB3PH != -1: return jouer(positions, couleur, colB3PH)    # B3PH : L'IA essaye d'empêcher l'adversaire d'aligner 3 pions
    elif colB2PH != -1: return jouer(positions, couleur, colB2PH)    # B2PH : L'IA essaye d'empêcher l'adversaire d'aligner 2 pions
    else: return jouer_ordi_poids_cases(positions, couleur)          # PH   : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia14(positions, couleur):                             # Priorité Alignements Troués
    """IA4 joue"""
    colA4PH = priorite_trouee(positions, 4, couleur)
    colA3PH = priorite_trouee(positions, 3, couleur)
    colA2PH = priorite_trouee(positions, 2, couleur)
    couleurAdversaire = inverse(couleur)
    colB4PH = priorite_trouee(positions, 4, couleurAdversaire)
    colB3PH = priorite_trouee(positions, 3, couleurAdversaire)
    colB2PH = priorite_trouee(positions, 2, couleurAdversaire)
    if colA4PH != -1: return jouer(positions, couleur, colA4PH)      # A4PH : L'IA essaye en priorité d'aligner 4 pions
    elif colB4PH != -1: return jouer(positions, couleur, colB4PH)    # B4PH : L'IA essaye d'empêcher l'adversaire d'aligner 4 pions
    elif colA3PH != -1: return jouer(positions, couleur, colA3PH)    # A3PH : L'IA essaye d'aligner 3 pions
    elif colB3PH != -1: return jouer(positions, couleur, colB3PH)    # B3PH : L'IA essaye d'empêcher l'adversaire d'aligner 3 pions
    elif colA2PH != -1: return jouer(positions, couleur, colA2PH)    # A2PH : L'IA essaye d'aligner 2 pions
    elif colB2PH != -1: return jouer(positions, couleur, colB2PH)    # B2PH : L'IA essaye d'empêcher l'adversaire d'aligner 2 pions
    else: return jouer_ordi_poids_cases(positions, couleur)          # PH   : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia15(positions, couleur):                             # Priorité Alignements Troués
    """IA5 joue"""
    colA4PH = priorite_trouee(positions, 4, couleur)
    colA3PH = priorite_trouee(positions, 3, couleur)
    colA2PH = priorite_trouee(positions, 2, couleur)
    couleurAdversaire = inverse(couleur)
    colB4PH = priorite_trouee(positions, 4, couleurAdversaire)
    colB3PH = priorite_trouee(positions, 3, couleurAdversaire)
    colB2PH = priorite_trouee(positions, 2, couleurAdversaire)
    if colA4PH != -1: return jouer(positions, couleur, colA4PH)      # A4PH : L'IA essaye en priorité d'aligner 4 pions
    elif colB4PH != -1: return jouer(positions, couleur, colB4PH)    # B4PH : L'IA essaye d'empêcher l'adversaire d'aligner 4 pions
    elif colA3PH != -1: return jouer(positions, couleur, colA3PH)    # A3PH : L'IA essaye d'aligner 3 pions
    elif colB3PH != -1: return jouer(positions, couleur, colB3PH)    # B3PH : L'IA essaye d'empêcher l'adversaire d'aligner 3 pions
    elif colB2PH != -1: return jouer(positions, couleur, colB2PH)    # B2PH : L'IA essaye d'empêcher l'adversaire d'aligner 2 pions
    elif colA2PH != -1: return jouer(positions, couleur, colA2PH)    # A2PH : L'IA essaye d'aligner 2 pions
    else: return jouer_ordi_poids_cases(positions, couleur)          # PH   : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia16(positions, couleur):                             # Priorité Alignements Troués
    """IA6 joue"""
    colA4PH = priorite_trouee(positions, 4, couleur)
    colA3PH = priorite_trouee(positions, 3, couleur)
    colA2PH = priorite_trouee(positions, 2, couleur)
    couleurAdversaire = inverse(couleur)
    colB4PH = priorite_trouee(positions, 4, couleurAdversaire)
    colB3PH = priorite_trouee(positions, 3, couleurAdversaire)
    colB2PH = priorite_trouee(positions, 2, couleurAdversaire)
    if colA4PH != -1: return jouer(positions, couleur, colA4PH)      # A4PH : L'IA essaye en priorité d'aligner 4 pions
    elif colB4PH != -1: return jouer(positions, couleur, colB4PH)    # B4PH : L'IA essaye d'empêcher l'adversaire d'aligner 4 pions
    elif colB3PH != -1: return jouer(positions, couleur, colB3PH)    # B3PH : L'IA essaye d'empêcher l'adversaire d'aligner 3 pions
    elif colA3PH != -1: return jouer(positions, couleur, colA3PH)    # A3PH : L'IA essaye d'aligner 3 pions
    elif colA2PH != -1: return jouer(positions, couleur, colA2PH)    # A2PH : L'IA essaye d'aligner 2 pions
    elif colB2PH != -1: return jouer(positions, couleur, colB2PH)    # B2PH : L'IA essaye d'empêcher l'adversaire d'aligner 2 pions
    else: return jouer_ordi_poids_cases(positions, couleur)          # PH   : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia17(positions, couleur):                             # Priorité Alignements Troués
    """IA7 joue"""
    colA4PH = priorite_trouee(positions, 4, couleur)
    colA3PH = priorite_trouee(positions, 3, couleur)
    colA2PH = priorite_trouee(positions, 2, couleur)
    couleurAdversaire = inverse(couleur)
    colB4PH = priorite_trouee(positions, 4, couleurAdversaire)
    colB3PH = priorite_trouee(positions, 3, couleurAdversaire)
    colB2PH = priorite_trouee(positions, 2, couleurAdversaire)
    if colA4PH != -1: return jouer(positions, couleur, colA4PH)      # A4PH : L'IA essaye en priorité d'aligner 4 pions
    elif colB4PH != -1: return jouer(positions, couleur, colB4PH)    # B4PH : L'IA essaye d'empêcher l'adversaire d'aligner 4 pions
    elif colB3PH != -1: return jouer(positions, couleur, colB3PH)    # B3PH : L'IA essaye d'empêcher l'adversaire d'aligner 3 pions
    elif colA3PH != -1: return jouer(positions, couleur, colA3PH)    # A3PH : L'IA essaye d'aligner 3 pions
    elif colB2PH != -1: return jouer(positions, couleur, colB2PH)    # B2PH : L'IA essaye d'empêcher l'adversaire d'aligner 2 pions
    elif colA2PH != -1: return jouer(positions, couleur, colA2PH)    # A2PH : L'IA essaye d'aligner 2 pions
    else: return jouer_ordi_poids_cases(positions, couleur)          # PH   : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia18(positions, couleur):                             # Priorité Alignements Troués
    """IA8 joue"""
    colA4PH = priorite_trouee(positions, 4, couleur)
    colA2PH = priorite_trouee(positions, 2, couleur)
    couleurAdversaire = inverse(couleur)
    colB4PH = priorite_trouee(positions, 4, couleurAdversaire)
    colB2PH = priorite_trouee(positions, 2, couleurAdversaire)
    if colA4PH != -1: return jouer(positions, couleur, colA4PH)      # A4PH : L'IA essaye en priorité d'aligner 4 pions
    elif colB4PH != -1: return jouer(positions, couleur, colB4PH)    # B4PH : L'IA essaye d'empêcher l'adversaire d'aligner 4 pions
    elif colA2PH != -1: return jouer(positions, couleur, colA2PH)    # A2PH : L'IA essaye d'aligner 2 pions
    elif colB2PH != -1: return jouer(positions, couleur, colB2PH)    # B2PH : L'IA essaye d'empêcher l'adversaire d'aligner 2 pions
    else: return jouer_ordi_poids_cases(positions, couleur)          # PH   : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia19(positions, couleur):                             # Priorité Alignements Troués
    """IA9 joue"""
    colA4PH = priorite_trouee(positions, 4, couleur)
    colA2PH = priorite_trouee(positions, 2, couleur)
    couleurAdversaire = inverse(couleur)
    colB4PH = priorite_trouee(positions, 4, couleurAdversaire)
    colB2PH = priorite_trouee(positions, 2, couleurAdversaire)
    if colA4PH != -1: return jouer(positions, couleur, colA4PH)      # A4PH : L'IA essaye en priorité d'aligner 4 pions
    elif colB4PH != -1: return jouer(positions, couleur, colB4PH)    # B4PH : L'IA essaye d'empêcher l'adversaire d'aligner 4 pions
    elif colB2PH != -1: return jouer(positions, couleur, colB2PH)    # B2PH : L'IA essaye d'empêcher l'adversaire d'aligner 2 pions
    elif colA2PH != -1: return jouer(positions, couleur, colA2PH)    # A2PH : L'IA essaye d'aligner 2 pions
    else: return jouer_ordi_poids_cases(positions, couleur)          # PH   : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia20(positions, couleur):                             # Priorité Alignements Troués
    """IA10 joue"""
    colA4PH = priorite_trouee(positions, 4, couleur)
    colA3PH = priorite_trouee(positions, 3, couleur)
    colA2PH = priorite_trouee(positions, 2, couleur)
    couleurAdversaire = inverse(couleur)
    colB4PH = priorite_trouee(positions, 4, couleurAdversaire)
    colB3PH = priorite_trouee(positions, 3, couleurAdversaire)
    colB2PH = priorite_trouee(positions, 2, couleurAdversaire)
    if colA4PH != -1: return jouer(positions, couleur, colA4PH)      # A4PH : L'IA essaye en priorité d'aligner 4 pions
    elif colB4PH != -1: return jouer(positions, couleur, colB4PH)    # B4PH : L'IA essaye d'empêcher l'adversaire d'aligner 4 pions
    elif colB3PH != -1: return jouer(positions, couleur, colB3PH)    # B3PH : L'IA essaye d'empêcher l'adversaire d'aligner 3 pions
    elif colB2PH != -1: return jouer(positions, couleur, colB2PH)    # B2PH : L'IA essaye d'empêcher l'adversaire d'aligner 2 pions
    elif colA3PH != -1: return jouer(positions, couleur, colA3PH)    # A3PH : L'IA essaye d'aligner 3 pions
    elif colA2PH != -1: return jouer(positions, couleur, colA2PH)    # A2PH : L'IA essaye d'aligner 2 pions
    else: return jouer_ordi_poids_cases(positions, couleur)          # PH   : L'IA joue dans la case qui a le plus de poids

########################################################################

def jouer_ordi_ia(positions, couleur, ia):
    """L'IA choisie joue"""
    if ia == 0: positions = jouer_ordi_ia0(positions, couleur)
    elif ia == 1: positions = jouer_ordi_ia1(positions, couleur)
    
    elif ia == 2: positions = jouer_ordi_ia2(positions, couleur)
    elif ia == 3: positions = jouer_ordi_ia3(positions, couleur)
    elif ia == 4: positions = jouer_ordi_ia4(positions, couleur)
    elif ia == 5: positions = jouer_ordi_ia5(positions, couleur)
    elif ia == 6: positions = jouer_ordi_ia6(positions, couleur)
    elif ia == 7: positions = jouer_ordi_ia7(positions, couleur)
    elif ia == 8: positions = jouer_ordi_ia8(positions, couleur)
    elif ia == 9: positions = jouer_ordi_ia9(positions, couleur)
    elif ia == 10: positions = jouer_ordi_ia10(positions, couleur)
    
    elif ia == 12: positions = jouer_ordi_ia12(positions, couleur)
    elif ia == 13: positions = jouer_ordi_ia13(positions, couleur)
    elif ia == 14: positions = jouer_ordi_ia14(positions, couleur)
    elif ia == 15: positions = jouer_ordi_ia15(positions, couleur)
    elif ia == 16: positions = jouer_ordi_ia16(positions, couleur)
    elif ia == 17: positions = jouer_ordi_ia17(positions, couleur)
    elif ia == 18: positions = jouer_ordi_ia18(positions, couleur)
    elif ia == 19: positions = jouer_ordi_ia19(positions, couleur)
    elif ia == 20: positions = jouer_ordi_ia20(positions, couleur)
    return positions

########################################################################
