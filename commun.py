# -*- coding: utf-8 -*-
"""
########################################################################
#  Version du 30 juillet 2020 à 11 h 39
########################################################################
"""

from constantes import MODE_GRAPHIQUE, NB_COLONNES, NB_LIGNES, ALIGNEMENT
from mode_graphique import affiche_grille_fenetre, affiche_gagnant_fenetre, affiche_aucun_gagnant_fenetre, affiche_joueur_fenetre
import math




########################################################################
# AFFICHAGE DE LA GRILLE ET DES JETONS DANS LA CONSOLE
########################################################################

def affiche_grille_console(positions):
    """Affiche la grille dans la console"""
    i = NB_COLONNES*(NB_LIGNES-1)
    while i >= 0:
        print(positions[i:i+NB_COLONNES])
        i = i - NB_COLONNES
    print()

########################################################################




########################################################################
# AFFICHAGE DES MESSAGES DANS LA CONSOLE
########################################################################

def affiche_joueur_qui_commence_console(couleur):
    """Affichage du joueur qui commence dans la console"""
    if couleur == 'yellow':
        print('Les jaunes commencent')
    elif couleur == 'red':
        print('Les rouges commencent')

########################################################################

def affiche_joueur_console(couleur):
    """Affichage du joueur dans la console"""
    if couleur == 'yellow':
        print('Les jaunes jouent')
    elif couleur == 'red':
        print('Les rouges jouent')

########################################################################

def affiche_gagnant_console(couleur):
    """Affichage du gagnant dans la console"""
    if couleur == 'yellow':
        print('Les jaunes gagnent', end='')
    elif couleur == 'red':
        print('Les rouges gagnent', end='')

########################################################################

def affiche_aucun_gagnant_console():
    """Affichage aucun gagnant dans la console"""
    print('Aucun gagnant')

########################################################################

def affiche_victoires_console(victoires):
    """Affichage du nombre de victoires dans la console"""
    [jaunes, rouges, nulles] = victoires
    print('Jaunes : ' + str(jaunes))  # Victoires jaunes
    print('Rouges : ' + str(rouges))  # Victoires rouges
    print('Nulles : ' + str(nulles))  # Parties nulles
    print()

########################################################################




########################################################################
# MOTEUR DU JEU
########################################################################

def initialise_liste_positions():
    """Vide la grille"""
    return [0] * NB_COLONNES*NB_LIGNES

########################################################################

def alignement(somme, nbPions, couleur):
    """Analyse la somme dont il est question dans alignements_pleins() ou alignements_troues() pour détermminer si des pions sont alignés"""
    pionsAlignes = False
    if (couleur == 'yellow' and somme == nbPions) or (couleur == 'red' and somme == -nbPions):
        pionsAlignes = True
    return pionsAlignes

########################################################################

def alignements_pleins(positions, nbPions, couleur):
    """Teste les alignements pleins d'un nombre de pions donné et les retourne sous forme de liste"""
    """
    4 pions alignés : 1111
    3 pions alignés : 111
    2 pions alignés : 11
    1 pion "aligné" : 1
    """
    listeAlignementsPleins = []
    # Vérification des alignements horizontaux
    for j in range(NB_LIGNES):
        for i in range(NB_COLONNES-nbPions+1):
            somme = 0
            for k in range(nbPions):
                somme += positions[NB_COLONNES*j+i+k]
            if alignement(somme, nbPions, couleur):
                listeAlignementsPleins += [i+1,j+1,"H"]
    # Vérification des alignements verticaux
    for j in range(NB_LIGNES-nbPions+1):
        for i in range(NB_COLONNES):
            somme = 0
            for k in range(nbPions):
                somme += positions[NB_COLONNES*j+i+k*NB_COLONNES]
            if alignement(somme, nbPions, couleur):
                listeAlignementsPleins += [i+1,j+1,"V"]
    # Vérification des diagonales montantes
    for j in range(NB_LIGNES-nbPions+1):
        for i in range(NB_COLONNES-nbPions+1):
            somme = 0
            for k in range(nbPions):
                somme += positions[NB_COLONNES*j+i+k*NB_COLONNES+k]
            if alignement(somme, nbPions, couleur):
                listeAlignementsPleins += [i+1,j+1,"DM"]
    # Vérification des diagonales descendantes
    for j in range(nbPions-1, NB_LIGNES):
        for i in range(NB_COLONNES-nbPions+1):
            somme = 0
            for k in range(nbPions):
                somme += positions[NB_COLONNES*j+i-k*NB_COLONNES+k]
            if alignement(somme, nbPions, couleur):
                listeAlignementsPleins += [i+1,j+1,"DD"]
    if listeAlignementsPleins != []:
        listeAlignementsPleins = [nbPions] + listeAlignementsPleins
    return listeAlignementsPleins

########################################################################

def alignements_troues(positions, nbPions, couleur):
    """Teste les alignements troués d'un nombre de pions donné et les retourne sous forme de liste"""
    """
    3 pions alignés : 1110 / 1101 / 1011 / 0111
    2 pions alignés : 110 / 101 / 011
    1 pion "aligné" : 10 / 01
    """
    listeAlignementsTroues = []
    # Vérification des alignements horizontaux
    for j in range(NB_LIGNES):
        for i in range(NB_COLONNES-nbPions):
            somme = 0
            for k in range(nbPions+1):
                somme += positions[NB_COLONNES*j+i+k]
            if alignement(somme, nbPions, couleur):
                listeAlignementsTroues += [i+1,j+1,"H"]
    # Vérification des alignements verticaux
    for j in range(NB_LIGNES-nbPions):
        for i in range(NB_COLONNES):
            somme = 0
            for k in range(nbPions+1):
                somme += positions[NB_COLONNES*j+i+k*NB_COLONNES]
            if alignement(somme, nbPions, couleur):
                listeAlignementsTroues += [i+1,j+1,"V"]
    # Vérification des diagonales montantes
    for j in range(NB_LIGNES-nbPions):
        for i in range(NB_COLONNES-nbPions):
            somme = 0
            for k in range(nbPions+1):
                somme += positions[NB_COLONNES*j+i+k*NB_COLONNES+k]
            if alignement(somme, nbPions, couleur):
                listeAlignementsTroues += [i+1,j+1,"DM"]
    # Vérification des diagonales descendantes
    for j in range(nbPions, NB_LIGNES):
        for i in range(NB_COLONNES-nbPions):
            somme = 0
            for k in range(nbPions+1):
                somme += positions[NB_COLONNES*j+i-k*NB_COLONNES+k]
            if alignement(somme, nbPions, couleur):
                listeAlignementsTroues += [i+1,j+1,"DD"]
    if listeAlignementsTroues != []:
        listeAlignementsTroues = [nbPions] + listeAlignementsTroues
    return listeAlignementsTroues

########################################################################

def grille_pleine(positions):
    """Teste si la grille est pleine"""
    plein = True
    for i in range(NB_LIGNES*NB_COLONNES):
        if positions[i] == 0:
            plein = False
    return plein

########################################################################

def inverse(couleur):
    """ Inverse les couleurs"""
    if couleur == 'yellow':
        couleur = 'red'
    elif couleur == 'red':
        couleur = 'yellow'
    return couleur

########################################################################

def colonne_pleine(positions, colonne):
    """Teste si la colonne indiquée est pleine"""
    plein = True
    position = NB_COLONNES*(NB_LIGNES-1)+colonne-1
    if positions[position] == 0:
        plein = False
    return plein

########################################################################

def jouer(positions, couleur, colonne):
    """Moteur du jeu"""
    if not colonne_pleine(positions, colonne):
        # On remplit la liste des positions
        position = colonne - 1
        ligneSupport = 0
        while positions[position]:
            ligneSupport += 1
            position += NB_COLONNES
        if couleur == 'yellow':
            valeur = 1
        elif couleur == 'red':
            valeur = -1            
        positions[position] = valeur
    # On affiche la grille pour visualiser les positions
    affiche_grille_console(positions)                                   # Affichage Grille
    if MODE_GRAPHIQUE:
        affiche_grille_fenetre(colonne, ligneSupport, couleur)
    return positions

########################################################################

def fin_partie(positions, couleur, victoires):
    """ Test de fin de partie"""
    [jaunes, rouges, nulles] = victoires
    # On teste si la partie est finie
    fin = False
    if alignements_pleins(positions, ALIGNEMENT, couleur):
        fin = True
        if couleur == 'yellow':
            jaunes += 1
        elif couleur == 'red':
            rouges += 1
        # On affiche le gagnant
        affiche_gagnant_console(couleur)
        nbCoups = analyse_victoire(positions)
        print(" en", nbCoups, "coups")
        if MODE_GRAPHIQUE:
            affiche_gagnant_fenetre(couleur)
    elif grille_pleine(positions):
        fin = True
        nulles += 1
        # On affiche aucun gagnant
        affiche_aucun_gagnant_console()
        if MODE_GRAPHIQUE:
            affiche_aucun_gagnant_fenetre()
    else:
        couleur = inverse(couleur)
        # On affiche qui doit jouer
        affiche_joueur_console(couleur)
        if MODE_GRAPHIQUE:
            affiche_joueur_fenetre(couleur)
    victoires = [jaunes, rouges, nulles]
    return fin, couleur, victoires

########################################################################




########################################################################
# ANALYSE
########################################################################

def analyse_victoire(positions):
    """Analyse la victoire"""
    # Nombre de coups du gagnant
    nbPositionsPleines = NB_LIGNES*NB_COLONNES
    for i in range(NB_LIGNES*NB_COLONNES):
        if positions[i] == 0:
            nbPositionsPleines -= 1
    return math.ceil(nbPositionsPleines/2)  ## Arrondi à l'entier supérieur

########################################################################
