#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import random
from typing import List, Optional, Callable, Dict, Tuple

# ======================================================================
#                       PARAMÈTRES ET CONSTANTES
# ======================================================================

# Taille de la grille logique (6 lignes x 7 colonnes) et condition de victoire
NB_LIGNES, NB_COLONNES, ALIGNER = 6, 7, 4

# Codes internes des cases
VIDE, J1, J2 = 0, 1, -1  # J1 = Jaune (Humain ou IA), J2 = Rouge (IA uniquement)

# Géométrie des cases - Dimensions en pixels du canvas
TAILLE_CASE = 100       # taille d'une case (carré) en pixels
MARGE = 8  # marge interne d'un trou (épaisseur du "plastique" autour du pion)
RAYON = (TAILLE_CASE - 2*MARGE)//2  # rayon du disque dessiné à l'écran
BORD_GRILLE = MARGE  # Bord bleu autour de la grille = même valeur que l'écart entre 2 trous
LARGEUR_GRILLE = NB_COLONNES * TAILLE_CASE
HAUTEUR_GRILLE = NB_LIGNES * TAILLE_CASE
LARGEUR_CANVAS = LARGEUR_GRILLE + 2*BORD_GRILLE
HAUTEUR_CANVAS = HAUTEUR_GRILLE + 2*BORD_GRILLE

# Couleurs de l'interface (plateau façon "bleu Puissance 4" et pions)
COULEUR_PLATEAU = "#0b3d91"  # Bleu
COULEUR_TROU    = "#e7eef7"  # Bleu-gris très clair
COULEUR_J1      = "#ffd11a"  # Jaune
COULEUR_J2      = "#ff4d4d"  # Rouge

# Traits qui soulignent un alignement gagnant
COULEUR_LIGNE_GAGNANTE   = "#3cb700"  #  Vert
EPAISSEUR_LIGNE_GAGNANTE = 12

# Tempo d'attente (ms) avant qu'une IA ne joue son coup (pour voir l'animation)
DELAI_IA_MS = 150  # tempo IA côté UI 

# Réglage taille de lot tournoi
TAILLE_LOT_TOURNOI = 2   # Nombre de parties simulées d’un coup (plus petit = UI plus fluide)

# Types utilitaires
Grille = List[List[int]]
Case = Tuple[int, int]

# ======================================================================
#                        MÉCANIQUE "MOTEUR" DU JEU
# ======================================================================

def creer_grille() -> Grille:
    """
    Crée une grille vide (liste de listes) : NB_LIGNES x NB_COLONNES pleine de VIDE.
    Les indices pour se positionner dans la grille, avec NB_LIGNES = 6 et NB_COLONNES = 7 :
    [0][0] ... [0][6]
     .             .
     .             .
     .             .
    [5][0] ... [5][6]
    """
    return [[VIDE for _ in range(NB_COLONNES)] for _ in range(NB_LIGNES)]

# ----------------------------------------------------------------------

def coups_valides(grille: Grille) -> List[int]:
    """Retourne la liste des colonnes dans lesquelles on peut encore jouer (case du haut vide)."""
    return [c for c in range(NB_COLONNES) if grille[0][c] == VIDE]

# ----------------------------------------------------------------------

def poser_pion(grille: Grille, col: int, joueur: int) -> Optional[int]:
    """
    Tente de poser un pion 'joueur' dans la colonne 'col'.
    Le pion "tombe" jusqu'à la première case vide par le bas.
    Retourne l'indice de ligne où le pion s'est posé, ou None si la colonne est pleine.
    """
    for l in range(NB_LIGNES-1, -1, -1):  # On part du bas et on remonte
        if grille[l][col] == VIDE:
            grille[l][col] = joueur
            return l
    return None

# ----------------------------------------------------------------------
#
# def retirer_pion(grille: Grille, col: int) -> Optional[int]:
#    """
#    Retire le pion le PLUS HAUT de la colonne (utile pour des simulations IA).
#    Retourne la ligne retirée, ou None si la colonne était vide.
#    """
#    for l in range(NB_LIGNES):
#        if grille[l][col] != VIDE:
#            grille[l][col] = VIDE
#            return l
#    return None

# ----------------------------------------------------------------------

def grille_pleine(grille: Grille) -> bool:
    """Vrai si la rangée du haut est entièrement occupée (aucun coup possible)."""
    return all(grille[0][c] != VIDE for c in range(NB_COLONNES))

# ----------------------------------------------------------------------

def trouver_tous_alignements(grille: Grille, l0: int, c0: int, joueur: int) -> List[List[Case]]:
    """
    Depuis la case (l0, c0) nouvellement jouée par 'joueur', détecte TOUT alignement (≥4)
    dans les 4 directions canoniques : horizontal, vertical, 2 diagonales.
    Retourne une liste de listes de cases, chaque sous-liste étant l'alignement complet
    (de l'extrémité A à l'extrémité B). Si aucun alignement : liste vide.
    """
    if l0 is None or c0 is None:
        return []
    
    directions = [(0,1), (1,0), (1,1), (1,-1)]  # →, ↓, ↘, ↙
    resultat: List[List[Case]] = []
    
    for dl, dc in directions:
		# On collecte toutes les cases contiguës identiques dans +d et -d
        cases: List[Case] = [(l0, c0)]
        # Avance +d
        l, c = l0 + dl, c0 + dc
        while 0 <= l < NB_LIGNES and 0 <= c < NB_COLONNES and grille[l][c] == joueur:
            cases.append((l, c)); l += dl; c += dc
        # Avance -d
        l, c = l0 - dl, c0 - dc
        while 0 <= l < NB_LIGNES and 0 <= c < NB_COLONNES and grille[l][c] == joueur:
            cases.insert(0, (l, c)); l -= dl; c -= dc
        # Si on a au moins 4 cases, c'est un alignement gagnant
        if len(cases) >= ALIGNER:
            resultat.append(cases)
    
    return resultat

# ======================================================================
#                       IA (joueurs automatiques)
# ======================================================================

# ----------------------------------------------------------------------
#                       Aléatoire
# ----------------------------------------------------------------------

def ia_aleatoire(grille: Grille, joueur: int) -> int:
    """IA la plus simple : choisit aléatoirement une colonne valide."""
    return random.choice(coups_valides(grille))

# ----------------------------------------------------------------------
#                       Poids des cases
# ----------------------------------------------------------------------

def _poids_cases() -> List[List[int]]:
    """
    Certaines cases amènent plus souvent vers la victoire.
    Calcule le poids des cases en fonction de la dimension de la grille et du nombre de pions à aligner pour gagner.
    Pour une grille 6 lignes x 7 colonnes avec 4 pions à aligner :
    
    [[3, 4, 5, 7, 5, 4, 3],
     [4, 6, 8, 10, 8, 6, 4],
     [5, 8, 11, 13, 11, 8, 5],
     [5, 8, 11, 13, 11, 8, 5],
     [4, 6, 8, 10, 8, 6, 4],
     [3, 4, 5, 7, 5, 4, 3]] 
    """
    
    poids = [[0] * NB_COLONNES for _ in range(NB_LIGNES)]

    # Sur les horizontales
    for l in range(NB_LIGNES):
        for c in range(NB_COLONNES - ALIGNER + 1):
            for i in range(ALIGNER):
                poids[l][c + i] += 1

    # Sur les verticales
    for c in range(NB_COLONNES):
        for l in range(NB_LIGNES - ALIGNER + 1):
            for i in range(ALIGNER):
                poids[l + i][c] += 1

    # Sur les diagonales descendantes
    for l in range(NB_LIGNES - ALIGNER + 1):
        for c in range(NB_COLONNES - ALIGNER + 1):
            for i in range(ALIGNER):
                poids[l + i][c + i] += 1

    # Sur les diagonales montantes
    for l in range(ALIGNER - 1, NB_LIGNES):
        for c in range(NB_COLONNES - ALIGNER + 1):
            for i in range(ALIGNER):
                poids[l - i][c + i] += 1

    return poids

# ----------------------------------------------------------------------

def _poids_colonnes(grille: Grille) -> List[int]:
    """Calcule le poids des colonnes en fonction d'un état de la grille à un moment donné"""
    poidsColonnes = [0] * NB_COLONNES
    for c in coups_valides(grille):
        for l in range(NB_LIGNES-1, -1, -1):  # On part du bas et on remonte
            if grille[l][c] == VIDE:
                poidsColonnes[c] = _poids_cases()[l][c]
                break
    return poidsColonnes

# ----------------------------------------------------------------------

def _indices_maximum(liste: List[int]) -> List[int]:
    """Renvoie les indices des éléments ayant la valeur maximale dans la liste"""
    maxi = max(liste)
    indices = []
    for i in range(len(liste)):
        if liste[i] == maxi:
            indices += [i]
    return indices

# ----------------------------------------------------------------------

def ia_poids_cases(grille: Grille, joueur: int) -> int:
    """L'ordinateur joue en ne tenant compte que du poids des cases.
    Si plusieurs colonnes sont possibles (même poids), on tire au hasard une colonne"""
    return random.choice(_indices_maximum(_poids_colonnes(grille)))

# ----------------------------------------------------------------------
#                       Priorités
# ----------------------------------------------------------------------
"""
# Liste des priorités. Celles-ci peuvent se combiner de différentes manières.
# a4 : L'IA essaye en priorité d'aligner 4 pions
# b4 : L'IA essaye d'empêcher l'adversaire d'aligner 4 pions
# a3 : L'IA essaye d'aligner 3 pions
# b3 : L'IA essaye d'empêcher l'adversaire d'aligner 3 pions
# a2 : L'IA essaye d'aligner 2 pions
# b2 : L'IA essaye d'empêcher l'adversaire d'aligner 2 pions
# p  : L'IA joue dans la case qui a le plus de poids
"""
# ----------------------------------------------------------------------

def _alignement(somme, nbPions, joueur) -> bool:
    """Analyse la somme dont il est question dans _alignements_troues() pour détermminer si des pions sont alignés"""
    pionsAlignes = False
    if (joueur == J1 and somme == nbPions) or (joueur == J2 and somme == -nbPions):
        pionsAlignes = True
    return pionsAlignes

# ----------------------------------------------------------------------

def _position_possible(grille: Grille, ligne, colonne) -> bool:
    """Teste si une position est possible (case vide et support pour soutenir le pion)"""
    positionPossible = False
    if colonne >= 0 and colonne <= NB_COLONNES-1 and ligne >= 0 and ligne <= NB_LIGNES-1:
        if grille[ligne][colonne] == VIDE:  # Position libre
            positionPossible = True
            if ligne < 5:
                if grille[ligne + 1][colonne] == VIDE:  # Ligne support inexistante
                    positionPossible = False
    return positionPossible

# ----------------------------------------------------------------------

def _alignements_troues(grille: Grille, nbPions, joueur) -> List[int]:
    """Teste les alignements troués d'un nombre de pions donné et retourne sous forme de liste les colonnes potentielles"""
    """
    3 pions alignés avec un trou : 1110 / 1101 / 1011 / 0111
    2 pions alignés avec un trou : 110 / 101 / 011
    1 pion aligné avec un trou : 10 / 01
    """
 
    colonnesPotentielles = []
    # Vérification des alignements horizontaux
    for l in range(NB_LIGNES):
        for c in range(NB_COLONNES-nbPions):
            somme = 0
            for k in range(nbPions+1):
                somme += grille[l][c+k]
            # Si on a un alignement troué
            if _alignement(somme, nbPions, joueur):
                # print("Alignement horizontal :", nbPions, "pion(s) aligné(s) avec un trou") # Pour mise au point du programme
                for k in range(nbPions+1):
                    if _position_possible(grille, l, c+k):
                        # On ajoute, si elle est possible, une colonne à la liste
                        colonnesPotentielles += [c+k]
                
    # Vérification des alignements verticaux
    for c in range(NB_COLONNES):
      for l in range(NB_LIGNES-nbPions):
            somme = 0
            for k in range(nbPions+1):
                somme += grille[l+k][c]
            # Si on a un alignement troué
            if _alignement(somme, nbPions, joueur):
                # print("Alignement vertical :", nbPions, "pion(s) aligné(s) avec un trou") # Pour mise au point du programme
                if _position_possible(grille, l, c):  #l-nbPions initialement
                    # On ajoute, si elle est possible, une colonne à la liste
                    colonnesPotentielles += [c]
                
    # Vérification des diagonales descendantes
    for l in range(NB_LIGNES-nbPions):
        for c in range(NB_COLONNES-nbPions):
            somme = 0
            for k in range(nbPions+1):
                somme += grille[l+k][c+k]
            # Si on a un alignement troué
            if _alignement(somme, nbPions, joueur):
                # print("Alignement diagonale descendante :", nbPions, "pion(s) aligné(s) avec un trou") # Pour mise au point du programme
                for k in range(nbPions+1):
                    if _position_possible(grille, l+k, c+k):
                        # On ajoute, si elle est possible, une colonne à la liste
                        colonnesPotentielles += [c+k]
                
    # Vérification des diagonales montantes
    for l in range(nbPions, NB_LIGNES):
        for c in range(NB_COLONNES-nbPions):
            somme = 0
            for k in range(nbPions+1):
                somme += grille[l-k][c+k]
            # Si on a un alignement troué
            if _alignement(somme, nbPions, joueur):
                # print("Alignement diagonale montante :", nbPions, "pion(s) aligné(s) avec un trou") # Pour mise au point du programme
                for k in range(nbPions+1):
                    if _position_possible(grille, l-k, c+k):
                        # On ajoute, si elle est possible, une colonne à la liste
                        colonnesPotentielles += [c+k]

    # print("colonnesPotentielles ( joueur =", joueur, ") :", colonnesPotentielles)  # Pour mise au point du programme    
    return colonnesPotentielles

# ----------------------------------------------------------------------

def _meilleure_colonne(grille: Grille, colonnesPotentielles) -> int:
    """Détermine la meilleure colonne en s'appuyant sur le poids des colonnes"""
    # Calcule le poids des colonnes
    poidsColonnes = _poids_colonnes(grille)  
    # Détermine le poids des positions potentielles
    poidsColonnesPotentielles = []
    for i in range(len(colonnesPotentielles)):
        poidsColonnesPotentielles += [poidsColonnes[colonnesPotentielles[i]]]
    # print("poidsColonnesPotentielles", poidsColonnesPotentielles) # Pour mise au point du programme
    # Détermine les indices du poids maximum dans la liste ci-dessus
    indicesPoidsMaximum = _indices_maximum(poidsColonnesPotentielles)
    # print("indicesPoidsMaximum", indicesPoidsMaximum) # Pour mise au point du programme
    # Extrait les meilleures positions potentielles (celles qui ont un poids maximum)
    meilleuresColonnesPotentielles = []
    for i in range(len(indicesPoidsMaximum)):
        meilleuresColonnesPotentielles += [colonnesPotentielles[indicesPoidsMaximum[i]]]
    # print("meilleuresColonnesPotentielles", meilleuresColonnesPotentielles) # Pour mise au point du programme
    # Si plusieurs positions sont possibles (même poids), on tire au hasard une position
    colonne = random.choice(meilleuresColonnesPotentielles)
    # print("colonne choisie :", colonne) # Pour mise au point du programme
    return colonne

# ----------------------------------------------------------------------

def _priorite(grille: Grille, nbPions, joueur) -> int:
    """Retourne une colonne où jouer"""
    colonnesPotentielles = _alignements_troues(grille, nbPions-1, joueur)
    colonne = -1
    if len(colonnesPotentielles) > 0:
        colonne = _meilleure_colonne(grille, colonnesPotentielles)
    return colonne

# ----------------------------------------------------------------------

def _inverse(joueur):
    """ Inverse les joueurs"""
    if joueur == J1:
        joueur = J2
    elif joueur == J2:
        joueur = J1
    return joueur

# ----------------------------------------------------------------------

import re

def _ia_priorites(grille: "Grille", joueur, priorites: str) -> int:
    """
    IA basée sur une chaîne de priorités.

    :param grille: La grille du jeu.
    :param joueur: Le joueur courant (IA).
    :param priorites: Chaîne indiquant l'ordre des priorités. 
                      Format : "a4b4a3b3b2a2"
                      a = IA (joueur), b = adversaire, suivi du nombre de pions à aligner.
    :return: Colonne choisie par l'IA
    """
    
    if not priorites:
        raise ValueError("Vous devez fournir une chaîne de priorités.")

    adversaire = _inverse(joueur)
    
    # Extraction des priorités sous forme de liste de tuples (lettre, nombre)
    matches = re.findall(r'([ab])(\d+)', priorites)
    if not matches:
        raise ValueError("Format invalide pour priorites")

    # Conversion en tuples (joueur_cible, nb_pions)
    priorites = [
        (joueur if letter == "a" else adversaire, int(nb))
        for letter, nb in matches
    ]
    
    # Application des priorités
    for player, count in priorites:
        colonne = _priorite(grille, count, player)
        if colonne != -1:
            return colonne
    
    return ia_poids_cases(grille, joueur)

# ----------------------------------------------------------------------

# Wrappers pour ia_priorites car elle prend des paramètres différents des autres ia (priorites: str)

def ia_priorites_a4b4a3b3a2b2(grille: Grille, joueur: int) -> int:  # Initialement A14
    return _ia_priorites(grille, joueur, priorites="a4b4a3b3a2b2")

def ia_priorites_a4b4a3b3b2a2(grille: Grille, joueur: int) -> int:  # Initialement A15
    return _ia_priorites(grille, joueur, priorites="a4b4a3b3b2a2")

def ia_priorites_a4b4b3a3a2b2(grille: Grille, joueur: int) -> int:  # Initialement A16
    return _ia_priorites(grille, joueur, priorites="a4b4b3a3a2b2")

def ia_priorites_a4b4b3a3b2a2(grille: Grille, joueur: int) -> int:  # Initialement A17
    return _ia_priorites(grille, joueur, priorites="a4b4b3a3b2a2")

def ia_priorites_a4b4a2b2(grille: Grille, joueur: int) -> int:  # Initialement A18
    return _ia_priorites(grille, joueur, priorites="a4b4a2b2")

def ia_priorites_a4b4b3b2a3a2(grille: Grille, joueur: int) -> int:  # Initialement A20
    return _ia_priorites(grille, joueur, priorites="a4b4b3b2a3a2")

# ----------------------------------------------------------------------
#                       Minimax / Alpha-Beta
# ----------------------------------------------------------------------

def _jouer_col(plateau: Grille, col: int, j: int) -> Optional[int]:
    """Pose dans une COPIE de plateau et renvoie la ligne jouée; None si plein."""
    for l in range(NB_LIGNES-1, -1, -1):
        if plateau[l][col] == VIDE:
            plateau[l][col] = j
            return l
    return None

# ----------------------------------------------------------------------

def _gagne_depuis(plateau: Grille, l0: int, c0: int, j: int) -> bool:
    """Vérifie la victoire en partant d'un dernier coup (l0,c0)."""
    for dl, dc in ((0,1),(1,0),(1,1),(1,-1)):
        n = 1
        l, c = l0+dl, c0+dc
        while 0 <= l < NB_LIGNES and 0 <= c < NB_COLONNES and plateau[l][c]==j:
            n += 1; l += dl; c += dc
        l, c = l0-dl, c0-dc
        while 0 <= l < NB_LIGNES and 0 <= c < NB_COLONNES and plateau[l][c]==j:
            n += 1; l -= dl; c -= dc
        if n >= ALIGNER:
            return True
    return False

# ----------------------------------------------------------------------

def _est_terminal(plateau: Grille) -> Optional[int]:
    """Renvoie le gagnant J1/J2, 0 si nul, None sinon."""
    # Check lignes complètes pour victoire: on parcourt toutes cases
    for l in range(NB_LIGNES):
        for c in range(NB_COLONNES):
            j = plateau[l][c]
            if j == VIDE: continue
            # Suffit de vérifier à partir des points d'origine potentiels
            if c <= NB_COLONNES-ALIGNER and all(plateau[l][c+k]==j for k in range(ALIGNER)): return j
            if l <= NB_LIGNES-ALIGNER and all(plateau[l+k][c]==j for k in range(ALIGNER)): return j
            if c <= NB_COLONNES-ALIGNER and l <= NB_LIGNES-ALIGNER and all(plateau[l+k][c+k]==j for k in range(ALIGNER)): return j
            if c <= NB_COLONNES-ALIGNER and l >= ALIGNER-1 and all(plateau[l-k][c+k]==j for k in range(ALIGNER)): return j
    if all(plateau[0][c] != VIDE for c in range(NB_COLONNES)):
        return 0
    return None

# ------------------------------------------------------ """----------------

def _score_fenetre(seq: List[int], joueur: int) -> int:
    """Score d'une fenêtre de 4 pour 'joueur'."""
    adv = J1 if joueur == J2 else J2
    c_j = seq.count(joueur)
    c_a = seq.count(adv)
    c_v = seq.count(VIDE)

    if c_j == 4: return 10_000
    if c_j == 3 and c_v == 1: return 150
    if c_j == 2 and c_v == 2: return 20

    if c_a == 3 and c_v == 1: return -160  # menace adverse forte
    if c_a == 4: return -10_000
    return 0

# ----------------------------------------------------------------------

def _evaluer_pour(plateau: Grille, joueur: int) -> int:
    """Évalue uniquement du point de vue de 'joueur' (positif=bon pour joueur)."""
    score = 0

    # Bonus centre
    centre_col = NB_COLONNES // 2
    centre_count = sum(1 for l in range(NB_LIGNES) if plateau[l][centre_col] == joueur)
    score += 4 * centre_count

    # Fenêtres horizontales
    for l in range(NB_LIGNES):
        ligne = plateau[l]
        for c in range(NB_COLONNES-3):
            score += _score_fenetre(ligne[c:c+4], joueur)
    # Fenêtres verticales
    for c in range(NB_COLONNES):
        col_vals = [plateau[l][c] for l in range(NB_LIGNES)]
        for l in range(NB_LIGNES-3):
            score += _score_fenetre(col_vals[l:l+4], joueur)
    # Diagonales descendantes
    for l in range(NB_LIGNES-3):
        for c in range(NB_COLONNES-3):
            seq = [plateau[l+i][c+i] for i in range(4)]
            score += _score_fenetre(seq, joueur)
    # Diagonales montantes
    for l in range(3, NB_LIGNES):
        for c in range(NB_COLONNES-3):
            seq = [plateau[l-i][c+i] for i in range(4)]
            score += _score_fenetre(seq, joueur)
    return score

# ----------------------------------------------------------------------

def _evaluer(plateau: Grille, joueur_max: int) -> int:
    """Score symétrique: mon_score - score_adverse."""
    adv = J1 if joueur_max == J2 else J2
    return _evaluer_pour(plateau, joueur_max) - _evaluer_pour(plateau, adv)

# ----------------------------------------------------------------------

def _minimax(plateau: Grille, profondeur: int, joueur_actuel: int, joueur_max: int, alpha: int, beta: int) -> Tuple[int, Optional[int]]:
    """Retourne (score, colonne)."""
    terminal = _est_terminal(plateau)
    if terminal is not None:
        if terminal == 0:
            return 0, None
        return (1000000 if terminal == joueur_max else -1000000), None
    if profondeur == 0:
        return _evaluer(plateau, joueur_max), None

    valides = [c for c in range(NB_COLONNES) if plateau[0][c] == VIDE]
    # Heuristique d'ordre des coups: centre puis proche du centre
    order = sorted(valides, key=lambda c: abs(c - NB_COLONNES//2))

    best_col = random.choice(valides) if valides else None
    if joueur_actuel == joueur_max:
        best_score = -10**9
        for c in order:
            child = [row[:] for row in plateau]
            _ = _jouer_col(child, c, joueur_actuel)
            score, _ = _minimax(child, profondeur-1, J1 if joueur_actuel == J2 else J2, joueur_max, alpha, beta)
            if score > best_score:
                best_score = score
                best_col = c
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return best_score, best_col
    else:
        worst_score = 10**9
        for c in order:
            child = [row[:] for row in plateau]
            _ = _jouer_col(child, c, joueur_actuel)
            score, _ = _minimax(child, profondeur-1, J1 if joueur_actuel == J2 else J2, joueur_max, alpha, beta)
            if score < worst_score:
                worst_score = score
                best_col = c
            beta = min(beta, score)
            if beta <= alpha:
                break
        return worst_score, best_col

# ----------------------------------------------------------------------

def _ia_minimax_factory(depth: int) -> Callable[[Grille, int], int]:
    def _ia(grille: Grille, joueur: int) -> int:
        # 1) Tactiques rapides au N=1 depuis la position courante
        valides = coups_valides(grille)
        adv = J1 if joueur == J2 else J2
        # a) Gagner tout de suite si possible
        for c in sorted(valides, key=lambda x: abs(x - NB_COLONNES//2)):
            tmp = [row[:] for row in grille]
            l = poser_pion(tmp, c, joueur)
            if l is not None and trouver_tous_alignements(tmp, l, c, joueur):
                return c
        # b) Bloquer victoire adverse immédiate
        for c in sorted(valides, key=lambda x: abs(x - NB_COLONNES//2)):
            tmp = [row[:] for row in grille]
            l = poser_pion(tmp, c, adv)
            if l is not None and trouver_tous_alignements(tmp, l, c, adv):
                return c

        # 2) Minimax standard
        plateau = [row[:] for row in grille]
        _, col = _minimax(plateau, depth, joueur, joueur, alpha=-10**9, beta=10**9)
        if col is None:
            # fallback si algo n'a pas pu choisir (devrait être rare)
            return random.choice(valides) if valides else 0
        return col
    _ia.__name__ = f"ia_minimax_{depth}"
    return _ia

# ----------------------------------------------------------------------

ia_minimax_1 = _ia_minimax_factory(1)
ia_minimax_2 = _ia_minimax_factory(2)
ia_minimax_4 = _ia_minimax_factory(4)

# ----------------------------------------------------------------------
#                       Liste des IA disponibles
# ----------------------------------------------------------------------

IA_DISPONIBLES: Dict[str, Callable[[Grille, int], int]] = {
    "Aléatoire": ia_aleatoire,
    "Poids des cases": ia_poids_cases,
    "a4b4a3b3a2b2": ia_priorites_a4b4a3b3a2b2,  # Initialement A14
    "a4b4a3b3b2a2": ia_priorites_a4b4a3b3b2a2,  # Initialement A15
    "a4b4b3a3a2b2": ia_priorites_a4b4b3a3a2b2,  # Initialement A16
    "a4b4b3a3b2a2": ia_priorites_a4b4b3a3b2a2,  # Initialement A17
    "a4b4a2b2": ia_priorites_a4b4a2b2,          # Initialement A18
    "a4b4b3b2a3a2": ia_priorites_a4b4b3b2a3a2,  # Initialement A20
    "Minimax-1": ia_minimax_1,
    "Minimax-2": ia_minimax_2,
    "Minimax-4": ia_minimax_4,  
}

# ----------------------------------------------------------------------

def nom_affiche_ia(nom_interne: str) -> str:
    return f"IA {nom_interne.lower()}"

# ----------------------------------------------------------------------

IA_MAP_AFFICHAGE_VERS_FUNC: Dict[str, Callable[[Grille, int], int]] = {
    nom_affiche_ia(nom): func for nom, func in IA_DISPONIBLES.items()
}

# ----------------------------------------------------------------------

OPTIONS_JAUNE = ["Humain"] + list(IA_MAP_AFFICHAGE_VERS_FUNC.keys())
OPTIONS_ROUGE = list(IA_MAP_AFFICHAGE_VERS_FUNC.keys())  # Rouge = IA obligatoire

# ======================================================================
#                      SIMULATION RAPIDE (MODE TOURNOI)
# ======================================================================

def simuler_partie_rapide_avec_ia(ia_j1: Callable[[Grille, int], int],
                                  ia_j2: Callable[[Grille, int], int],
                                  premier: int = J1) -> int:
    """
    Simule une partie complète en mémoire avec IA fournies.
    Retourne J1 (jaune) si jaune gagne, J2 (rouge) si rouge gagne, 0 si nul.
    """
    nb_l, nb_c = NB_LIGNES, NB_COLONNES
    plateau = [[VIDE]*nb_c for _ in range(nb_l)]
    hauteurs = [nb_l-1]*nb_c  # prochaine ligne libre par colonne
    joueur = premier

    def valides():
        return [c for c in range(nb_c) if hauteurs[c] >= 0]

    def poser(col, j):
        l = hauteurs[col]
        if l < 0:
            return None
        plateau[l][col] = j
        hauteurs[col] -= 1
        return l

    def gagne_depuis(l0, c0, j):
        for dl, dc in ((0,1),(1,0),(1,1),(1,-1)):
            n = 1
            l, c = l0+dl, c0+dc
            while 0 <= l < nb_l and 0 <= c < nb_c and plateau[l][c]==j:
                n += 1; l += dl; c += dc
            l, c = l0-dl, c0-dc
            while 0 <= l < nb_l and 0 <= c < nb_c and plateau[l][c]==j:
                n += 1; l -= dl; c -= dc
            if n >= ALIGNER:
                return True
        return False

    # Boucle de jeu
    while True:
        moves = valides()
        if not moves:
            return VIDE  # nul

        # Faire choisir la colonne par l'IA sur une COPIE du plateau courant
        grille_vue_par_ia = [row[:] for row in plateau]
        choisir = ia_j1 if joueur == J1 else ia_j2
        col = choisir(grille_vue_par_ia, joueur)
        if col not in moves:
            col = random.choice(moves)

        l = poser(col, joueur)
        if gagne_depuis(l, col, joueur):
            return joueur
        joueur = J2 if joueur == J1 else J1

# ======================================================================
#                               I N T E R F A C E
# ======================================================================

class Puissance4:
    def __init__(self, racine: tk.Tk):
        self.racine = racine
        self.racine.title("Puissance 4")
        self.racine.resizable(False, False)

        # État courant
        self.grille: Grille = creer_grille()
        self.tour: int = J1
        self.partie_finie = False
        self.partie_active = False
        self.historique: List[int] = []

        # Scores cumulés
        self.s_j1 = 0; self.s_j2 = 0; self.s_nul = 0

        # Choix joueurs
        self.choix_j1 = tk.StringVar(value="Humain")
        self.choix_j2 = tk.StringVar(value=nom_affiche_ia("Aléatoire"))
        self.roles_verrouilles = False

        # Tournoi
        self.tournoi_en_cours = False
        self.tournoi_total = 0
        self.tournoi_jouees = 0
        self.tournoi_var = tk.StringVar(value="")  # affiché en haut, à droite (barre 2)
        self.tournoi_vient_de_finir = False  # drapeau

        # UI dynamiques
        self.scores_var = tk.StringVar()

        # Curseur
        self.souris_sur_canvas = False

        # Segments gagnants
        self.segments_gagnants: List[Tuple[int, int, int, int]] = []

        # Style sobre
        self._configurer_style()

        # Construction UI
        self._construire_ui()
        self._maj_scores_label()
        self._dessiner_grille()
        self._maj_interaction_grille()
        self._maj_etat_boutons()
        self._maj_etat_tournoi()

    # ---------------- Thème / Style minimal ---------------- #
    def _configurer_style(self):
        style = ttk.Style()
        try:
            style.theme_use("default")  # Autres : clam, classic
        except Exception:
            pass
        # Palette simple
        style.configure(".", background="#f7f9fc", foreground="#0f172a")
        style.configure("Toolbar.TFrame", background="#f7f9fc")
        style.configure("Primary.TLabel", background="#f7f9fc", foreground="#0f172a")
        style.configure("Accent.TButton", background="#2563eb", foreground="#ffffff", borderwidth=0, padding=(10,6))
        style.map("Accent.TButton",
                  background=[("active", "#1b4fb8"), ("disabled", "#b6c3dc")])
        style.configure("Neutral.TButton", background="#e2e8f0", foreground="#0f172a", borderwidth=0, padding=(10,6))
        style.map("Neutral.TButton",
                  background=[("active", "#cbd5e1"), ("disabled", "#e5e7eb")])
        style.configure("TCombobox", fieldbackground="#ffffff", padding=4, arrowsize=14)

    # ---------------- UI ---------------- #
    def _construire_ui(self):
        root = ttk.Frame(self.racine, style="Toolbar.TFrame", padding=10)
        root.pack(fill="both", expand=True)

        # Barre 1 : sélecteurs + Revenir en arrière (à droite)
        barre1 = ttk.Frame(root, style="Toolbar.TFrame")
        barre1.pack(fill="x")
        bloc_g = ttk.Frame(barre1, style="Toolbar.TFrame"); bloc_g.pack(side="left")
        ttk.Label(bloc_g, text="Jaune :", style="Primary.TLabel").pack(side="left", padx=(0,6))
        self.cb1 = ttk.Combobox(bloc_g, textvariable=self.choix_j1, values=OPTIONS_JAUNE, width=16, state="readonly")
        self.cb1.pack(side="left"); self.cb1.bind("<<ComboboxSelected>>", self._changement_role)

        ttk.Label(bloc_g, text="   Rouge :", style="Primary.TLabel").pack(side="left", padx=(16,6))
        self.cb2 = ttk.Combobox(bloc_g, textvariable=self.choix_j2, values=OPTIONS_ROUGE, width=16, state="readonly")
        self.cb2.pack(side="left"); self.cb2.bind("<<ComboboxSelected>>", self._changement_role)

        self.btn_annuler = ttk.Button(barre1, text="Revenir en arrière", style="Neutral.TButton", command=self.annuler)
        self.btn_annuler.pack(side="right")

        # Barre 2 : Tournoi (à droite : état tournoi)
        barre2 = ttk.Frame(root, style="Toolbar.TFrame")
        barre2.pack(fill="x", pady=(8,0))
        # gauche
        ttk.Label(barre2, text="Tournoi IA — Parties :", style="Primary.TLabel").pack(side="left")
        self.VALEURS_TOURNOI = ["100", "1000", "10000"]
        self.nb_parties_var = tk.StringVar(value=self.VALEURS_TOURNOI[0])
        self.cmb_parties = ttk.Combobox(
            barre2, values=self.VALEURS_TOURNOI, textvariable=self.nb_parties_var, width=12, state="readonly"
        )
        self.cmb_parties.pack(side="left", padx=(6,10))
        self.btn_tournoi = ttk.Button(barre2, text="Lancer", style="Accent.TButton",
                                      command=self._demarrer_tournoi)
        self.btn_tournoi.pack(side="left")
        self.btn_stop = ttk.Button(barre2, text="Arrêter", style="Neutral.TButton",
                                   command=self._stop_tournoi)
        self.btn_stop.pack(side="left", padx=(8,0))
        # droite : état du tournoi (noir, Primary)
        ttk.Label(barre2, textvariable=self.tournoi_var,
                  style="Primary.TLabel", anchor="e", justify="right").pack(side="right")

        # --- GRILLE ---
        self.canvas = tk.Canvas(
            root, width=LARGEUR_CANVAS, height=HAUTEUR_CANVAS,
            bg=COULEUR_PLATEAU, highlightthickness=0, bd=0
        )
        self.canvas.pack(pady=(12,0))
        self.canvas.bind("<Button-1>", self._clic_grille)
        self.canvas.bind("<Motion>", self._mouvement_souris)
        self.canvas.bind("<Leave>", self._quitte_canvas)

        # Scores (sous la grille)
        zone_scores = ttk.Frame(root, style="Toolbar.TFrame")
        zone_scores.pack(fill="x", pady=(12,0))
        ttk.Label(zone_scores, textvariable=self.scores_var,
                  style="Primary.TLabel", anchor="center", justify="center").pack(fill="x")

    # ---------------- Helpers UI ---------------- #
    def _format_scores(self) -> str:
        return f"Jaune : {self.s_j1} | Rouge : {self.s_j2} | Nulles : {self.s_nul}"

    def _maj_scores_label(self):
        self.scores_var.set(self._format_scores())

    def _maj_interaction_grille(self):
        # Curseur main si (partie active & tour humain) ou (pré-partie & J1 humain & souris sur canvas)
        if self.partie_active and not self.partie_finie and self._est_humain(self.tour):
            self.canvas.configure(cursor="hand2")
        elif (not self.partie_active and not self.partie_finie and self._est_humain(J1) and self.souris_sur_canvas):
            self.canvas.configure(cursor="hand2")
        else:
            self.canvas.configure(cursor="arrow")

    def _maj_etat_boutons(self):
        # Bouton Revenir en arrière
        actif_annuler = self.partie_active and not self.partie_finie and bool(self.historique) and self._est_humain(self.tour)
        self.btn_annuler.configure(state=("normal" if actif_annuler else "disabled"))

        # Tournoi : actif ssi IA vs IA et pas de partie/tournoi en cours
        ia_vs_ia = (self.choix_j1.get() != "Humain")  # Rouge est déjà IA
        peut_lancer = ia_vs_ia and not self.partie_active and not self.tournoi_en_cours
        self.btn_tournoi.configure(style=("Accent.TButton" if peut_lancer else "Neutral.TButton"),
                                   state=("normal" if peut_lancer else "disabled"))
        self.cmb_parties.configure(state=("readonly" if peut_lancer else "disabled"))
        self.btn_stop.configure(state=("normal" if self.tournoi_en_cours else "disabled"))

        # Menus Jaune/Rouge désactivés si partie ou tournoi en cours
        if self.partie_active or self.tournoi_en_cours:
            self.cb1.configure(state="disabled"); self.cb2.configure(state="disabled")
        else:
            self.cb1.configure(state="readonly"); self.cb2.configure(state="readonly")

    def _maj_etat_tournoi(self):
        if self.tournoi_en_cours:
            self.tournoi_var.set(
                f"Jouées : {self.tournoi_jouees} / {self.tournoi_total}"
            )
        else:
            self.tournoi_var.set("")

    # ---------------- Rôles & IA ---------------- #
    def _est_humain(self, joueur: int) -> bool:
        return False if joueur == J2 else self.choix_j1.get() == "Humain"

    def _choisir_col_ia(self, joueur: int) -> int:
        choix_aff = self.choix_j2.get() if joueur == J2 else self.choix_j1.get()
        func = IA_MAP_AFFICHAGE_VERS_FUNC.get(choix_aff, ia_aleatoire)
        return func(self.grille, joueur)

    def _get_funcs_ia_selectionnees(self) -> Tuple[Callable[[Grille,int],int], Callable[[Grille,int],int]]:
        f1 = IA_MAP_AFFICHAGE_VERS_FUNC.get(self.choix_j1.get(), ia_aleatoire)
        f2 = IA_MAP_AFFICHAGE_VERS_FUNC.get(self.choix_j2.get(), ia_aleatoire)
        return f1, f2

    def _changement_role(self, _evt=None):
        # Refus si partie/tournoi en cours
        if (self.partie_active and not self.partie_finie) or self.tournoi_en_cours:
            self.cb1.set(self.choix_j1.get()); self.cb2.set(self.choix_j2.get()); return
        # On vide la grille ET on remet les scores à 0
        self._mettre_en_prepartie(effacer_grille=True, reinit_scores=True)
        self.tournoi_vient_de_finir = False  # on repart proprement

    # ---------------- États ---------------- #
    def _verrouiller_roles(self):
        self.cb1.configure(state="disabled"); self.cb2.configure(state="disabled")
        self.roles_verrouilles = True

    def _deverrouiller_roles(self):
        self.cb1.configure(state="readonly"); self.cb2.configure(state="readonly")
        self.roles_verrouilles = False

    def _mettre_en_prepartie(self, effacer_grille: bool, reinit_scores: bool = False):
        if effacer_grille:
            self.grille = creer_grille()
        self.tour = J1
        self.partie_finie = False
        self.partie_active = False
        self.historique.clear()
        self.segments_gagnants.clear()
        if reinit_scores:
            self.s_j1 = self.s_j2 = self.s_nul = 0
            self._maj_scores_label()
        self._deverrouiller_roles()
        self._dessiner_grille()
        self._maj_interaction_grille()
        self._maj_etat_boutons()
        self._maj_etat_tournoi()

    # ---------------- IA côté UI ---------------- #
    def _peut_planifier_ia(self):
        if self.partie_active and not self.partie_finie and not self._est_humain(self.tour):
            self.racine.after(DELAI_IA_MS, self._tique_ia)

    def _tique_ia(self):
        if not self.partie_active or self.partie_finie or self._est_humain(self.tour):
            return
        col = self._choisir_col_ia(self.tour)
        if self.grille[0][col] != VIDE:
            valides = coups_valides(self.grille)
            if not valides:
                return
            col = random.choice(valides)
        self._jouer_coup(col)
        self._peut_planifier_ia()

    # ---------------- Actions ---------------- #
    def _demarrer_partie(self, premier: int = J1):
        self.grille = creer_grille()
        self.tour = premier
        self.partie_finie = False
        self.partie_active = True
        self.historique.clear()
        self.segments_gagnants.clear()
        self._verrouiller_roles()
        self._dessiner_grille()
        self._maj_interaction_grille()
        self._maj_etat_boutons()
        self._peut_planifier_ia()
        self.tournoi_vient_de_finir = False  # on démarre une partie normale

    def annuler(self):
        if not self.partie_active or not self.historique or self.partie_finie or not self._est_humain(self.tour):
            return
        derniere = self.historique.pop()
        self._retirer_col(derniere)
        self.tour = J2 if self.tour == J1 else J1
        # Retire aussi les coups d'IA jusqu'à rendre la main à l'humain
        while self.historique and not self._est_humain(self.tour):
            derniere = self.historique.pop()
            self._retirer_col(derniere)
            self.tour = J2 if self.tour == J1 else J1
        if not self.historique:
            self._deverrouiller_roles()
        self.partie_finie = False
        self.segments_gagnants.clear()
        self._dessiner_grille()
        self._maj_interaction_grille()
        self._maj_etat_boutons()
        self._peut_planifier_ia()

    def _retirer_col(self, col: int):
        for l in range(NB_LIGNES):
            if self.grille[l][col] != VIDE:
                self.grille[l][col] = VIDE
                return

    # ---------------- Événements ---------------- #
    def _clic_grille(self, evt):
        # 1) Si un tournoi vient de se terminer : clic = scores à 0 + lancer IA vs IA (si possible)
        if self.tournoi_vient_de_finir:
            # On n'agit que si Jaune est une IA (Rouge l'est déjà)
            if self.choix_j1.get() != "Humain":
                # Remettre les compteurs à zéro
                self.s_j1 = self.s_j2 = self.s_nul = 0
                self._maj_scores_label()
                # Lancer une nouvelle partie IA vs IA (Jaune commence)
                self._demarrer_partie(premier=J1)
            # Dans tous les cas, on consomme le drapeau
            self.tournoi_vient_de_finir = False
            return

        if self.tournoi_en_cours:
            return  # ignore clics pendant tournoi

        x_local = evt.x - BORD_GRILLE
        col = int(x_local // TAILLE_CASE) if 0 <= x_local < LARGEUR_GRILLE else None

        # Si partie finie + J1 humain : clic = VIDER la grille (scores conservés)
        if self.partie_finie and self._est_humain(J1):
            self._mettre_en_prepartie(effacer_grille=True, reinit_scores=False)
            return

        # Démarrage si pas de partie
        if not self.partie_active:
            if self._est_humain(J1):
                if col is None:  # premier clic doit être dans la grille
                    return
                self._demarrer_partie(premier=J1)
                self._jouer_coup(col)
                self._peut_planifier_ia()
            else:
                # Jaune est IA : tout clic démarre, Jaune commence
                self._demarrer_partie(premier=J1)
            return

        # Partie en cours : seul l'humain peut jouer via clic
        if not self._est_humain(self.tour):
            return
        if col is None or self.grille[0][col] != VIDE:
            return
        self._jouer_coup(col)
        self._peut_planifier_ia()

    # ---------------- Tournoi (MODE TURBO) ---------------- #
    def _demarrer_tournoi(self):
        if self.choix_j1.get() == "Humain" or self.partie_active or self.tournoi_en_cours:
            return
        try:
            self.tournoi_total = max(1, int(self.nb_parties_var.get()))
        except Exception:
            self.tournoi_total = 10

        # Scores à 0 au lancement
        self.s_j1 = self.s_j2 = self.s_nul = 0
        self._maj_scores_label()

        self.tournoi_jouees = 0
        self.tournoi_en_cours = True
        self.tournoi_vient_de_finir = False  # on démarre un tournoi

        # Vider la grille à l'écran (sans re-réinitialiser les scores)
        self._mettre_en_prepartie(effacer_grille=True, reinit_scores=False)

        self._maj_etat_boutons()
        self._maj_etat_tournoi()

        # Lance la simulation par lots (mode turbo) avec la taille réglable
        self._tournoi_batch()

    def _stop_tournoi(self):
        """Stoppe le tournoi, remet les scores à 0, vide la grille et revient en pré-partie."""
        if not self.tournoi_en_cours:
            return
        self.tournoi_en_cours = False
        self.tournoi_vient_de_finir = False

        # scores à 0
        self.s_j1 = self.s_j2 = self.s_nul = 0
        self._maj_scores_label()

        # Vide la grille
        self._mettre_en_prepartie(effacer_grille=True, reinit_scores=False)

        # Reset indicateurs tournoi
        self.tournoi_total = 0
        self.tournoi_jouees = 0
        self._maj_etat_tournoi()
        self._maj_etat_boutons()

    def _tournoi_batch(self):
        """Simule un lot de parties sans UI, met à jour les compteurs, puis se replanifie."""
        if not self.tournoi_en_cours:
            return

        restant = self.tournoi_total - self.tournoi_jouees
        if restant <= 0:
            # Fin du tournoi
            self.tournoi_en_cours = False
            self.tournoi_vient_de_finir = True
            self._mettre_en_prepartie(effacer_grille=False, reinit_scores=False)
            self._maj_etat_tournoi()
            self._maj_etat_boutons()
            return

        # Utilise la constante réglable pour la taille de lot
        a_jouer = min(TAILLE_LOT_TOURNOI, restant)

        ia_j1, ia_j2 = self._get_funcs_ia_selectionnees()

        for k in range(a_jouer):
            premier = J1 if ((self.tournoi_jouees + k) % 2 == 0) else J2
            gagnant = simuler_partie_rapide_avec_ia(ia_j1=ia_j1, ia_j2=ia_j2, premier=premier)
            if gagnant == J1:
                self.s_j1 += 1
            elif gagnant == J2:
                self.s_j2 += 1
            else:
                self.s_nul += 1

        self.tournoi_jouees += a_jouer
        self._maj_scores_label()
        self._maj_etat_tournoi()

        # Replanifie très vite, tout en laissant l'UI respirer
        self.racine.after(1, self._tournoi_batch)

    # ---------------- Tour de jeu (mode normal) ---------------- #
    def _jouer_coup(self, col: int):
        l = poser_pion(self.grille, col, self.tour)
        if l is None:
            return
        self.historique.append(col)

        alignements = trouver_tous_alignements(self.grille, l, col, self.tour)
        if alignements:
            self.partie_finie = True
            self.partie_active = False
            self.segments_gagnants.clear()
            for al in alignements:
                (l1, c1), (l2, c2) = al[0], al[-1]
                x1 = BORD_GRILLE + c1*TAILLE_CASE + TAILLE_CASE//2
                y1 = BORD_GRILLE + l1*TAILLE_CASE + TAILLE_CASE//2
                x2 = BORD_GRILLE + c2*TAILLE_CASE + TAILLE_CASE//2
                y2 = BORD_GRILLE + l2*TAILLE_CASE + TAILLE_CASE//2
                self.segments_gagnants.append((x1, y1, x2, y2))

            if self.tour == J1:
                self.s_j1 += 1
            else:
                self.s_j2 += 1

            self._dessiner_grille()
            self._maj_scores_label()
            self._deverrouiller_roles()
            self._maj_interaction_grille()
            self._maj_etat_boutons()
            return

        if grille_pleine(self.grille):
            self.partie_finie = True
            self.partie_active = False
            self.segments_gagnants.clear()
            self._dessiner_grille()
            self.s_nul += 1
            self._maj_scores_label()
            self._deverrouiller_roles()
            self._maj_interaction_grille()
            self._maj_etat_boutons()
            return

        # Tour suivant
        self.tour = J2 if self.tour == J1 else J1
        self._dessiner_grille()
        self._maj_interaction_grille()
        self._maj_etat_boutons()

    # ---------------- Rendu ---------------- #
    def _dessiner_grille(self):
        self.canvas.delete("all")
        # Trous / pions
        for l in range(NB_LIGNES):
            for c in range(NB_COLONNES):
                x = BORD_GRILLE + c*TAILLE_CASE + TAILLE_CASE//2
                y = BORD_GRILLE + l*TAILLE_CASE + TAILLE_CASE//2
                v = self.grille[l][c]
                rempl = COULEUR_TROU if v == VIDE else (COULEUR_J1 if v == J1 else COULEUR_J2)
                self.canvas.create_oval(x - RAYON, y - RAYON, x + RAYON, y + RAYON,
                                        outline="", fill=rempl)
        # Segments gagnants (toutes lignes)
        for (x1, y1, x2, y2) in self.segments_gagnants:
            self.canvas.create_line(x1, y1, x2, y2,
                                    fill=COULEUR_LIGNE_GAGNANTE,
                                    width=EPAISSEUR_LIGNE_GAGNANTE,
                                    capstyle=tk.ROUND)

    # ---------------- Souris ---------------- #
    def _mouvement_souris(self, _evt):
        self.souris_sur_canvas = True
        self._maj_interaction_grille()

    def _quitte_canvas(self, _evt):
        self.souris_sur_canvas = False
        self._maj_interaction_grille()

# ---------------- Lancement ---------------- #
def main():
    root = tk.Tk()
    app = Puissance4(root)
    root.mainloop()

if __name__ == "__main__":
    main()
