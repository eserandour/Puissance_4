# -*- coding: utf-8 -*-
"""
########################################################################
#  Version du 13 octobre 2019 à 15 h 43
########################################################################
"""

from constantes import NB_COLONNES, NB_LIGNES, TEMPS_CHUTE
import tkinter
import time




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

########################################################################

def hauteur_grille(r):
    """Hauteur de la grille en fonction du rayon r des trous"""
    return 2*NB_LIGNES*r + (NB_LIGNES + 1)*ESPACEMENT

########################################################################

def rayon():
    """ Rayon des trous de la grille et des pions"""
    return (LARGEUR_GRILLE - (NB_COLONNES + 1)*ESPACEMENT) / (2*NB_COLONNES)

########################################################################

def creation_disque(x, y, r, c, tag):
    """Création d'un disque tag (trou ou jeton), de rayon r et de couleur c à la position (x,y)"""
    identifiant = grille.create_oval(x-r, y-r, x+r, y+r, fill=c, width=0, tags=tag)
    return identifiant

########################################################################

def creation_grille(r):
    """Création de la grille avec des trous de rayon r"""
    ligne = 1
    while ligne <= NB_LIGNES:
        colonne = 1
        while colonne <= NB_COLONNES:
            creation_disque(ESPACEMENT + r + (colonne-1)*(ESPACEMENT + 2*r),
                            ESPACEMENT + r + (ligne-1)*(ESPACEMENT + 2*r),
                            r, 'white', 'trou')
            colonne += 1
        ligne += 1

########################################################################

def creation_jeton(colonne, ligne, c, r):  # Dépend de la grille
    """Création d'un jeton de couleur c et de rayon r à la colonne et à la ligne indiquée"""
    identifiant = creation_disque(colonne*(ESPACEMENT+2*r)-r,
                                  (NB_LIGNES-ligne+1)*(ESPACEMENT+2*r)-r,
                                  r, c, 'jeton')
    return identifiant

########################################################################

def mouvement_jeton(identifiant, r):
    """Mouvement d'un jeton de rayon r"""
    grille.move(identifiant, 0, ESPACEMENT+2*r)

########################################################################

def affiche_grille_fenetre(colonne, ligneSupport, couleur):
    """Affichage du coup joué (avec chute du pion)"""
    ligne = NB_LIGNES
    r = rayon()
    identifiant = creation_jeton(colonne, ligne, couleur, r)
    while ligne > ligneSupport:
        if ligne < NB_LIGNES:
            mouvement_jeton(identifiant, r)
        fenetreJeu.update()
        time.sleep(TEMPS_CHUTE)
        ligne = ligne - 1

########################################################################

def destruction_jetons():
    """Destruction de tous les jetons"""
    grille.delete('jeton')

########################################################################
# Création des widgets "enfants" : grille (Canvas)
########################################################################

grille = tkinter.Canvas(fenetreJeu, width=LARGEUR_GRILLE, height=hauteur_grille(rayon()), background='blue')
creation_grille(rayon())
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
# AFFICHAGE DES MESSAGES DANS LA FENETRE
########################################################################

def affiche_joueur_qui_commence_fenetre(couleur):
    """Affichage du joueur qui commence dans la fenêtre Tkinter"""
    if couleur == 'yellow':
        message['text'] = 'Les jaunes commencent'
    elif couleur == 'red':
        message['text'] = 'Les rouges commencent'

########################################################################

def affiche_joueur_fenetre(couleur):
    """Affichage du joueur dans la fenêtre Tkinter"""
    if couleur == 'yellow':
        message['text'] = 'Les jaunes jouent'
    elif couleur == 'red':
        message['text'] = 'Les rouges jouent'

########################################################################

def affiche_gagnant_fenetre(couleur):
    """Affichage du gagnant dans la fenêtre Tkinter"""
    if couleur == 'yellow':
        message['text'] = 'Les jaunes gagnent'
    elif couleur == 'red':
        message['text'] = 'Les rouges gagnent'

########################################################################

def affiche_aucun_gagnant_fenetre():
    """Affichage aucun gagnant dans la fenêtre Tkinter"""
    message['text'] = 'Aucun gagnant'

########################################################################

def affiche_statistiques_fenetre(victoiresJaunes, victoiresRouges, partiesNulles):
    """Affichage des statistiques dans la fenêtre Tkinter"""
    scoreJaunes['text'] = 'Jaunes : ' + str(victoiresJaunes)
    scoreRouges['text'] = 'Rouges : ' + str(victoiresRouges)

########################################################################

def efface_message_fenetre():
    """Efface le label message dans la fenêtre Tkinter"""
    message['text'] = ''

########################################################################

def initialise_fenetre(nbParties):
    """ """
    TEMPS_PAUSE = 1
    fenetreJeu.update()
    # Pause en secondes
    time.sleep(TEMPS_PAUSE)
    if nbParties == 2:
        time.sleep(TEMPS_PAUSE*9)  # Pour pouvoir faire une copie écran
    # Dans la fenêtre graphique
    destruction_jetons()
    efface_message_fenetre()
    fenetreJeu.update()
    # Pause en secondes
    time.sleep(TEMPS_PAUSE)

########################################################################
