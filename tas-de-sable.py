# INFORMATION GROUPE
# GROUPE MI TD 03
# Mathis ALLOUCHE
# jennifer said
# xavier koubonou
# https://github.com/uvsq22104691/tas-de-sable


# Import
import tkinter.filedialog as tk_filedialog
import tkinter as tk
import copy
import numpy as np
import os
from random import randint


# Constante

# Largeur du canvas
W = 600
# Hauteur du canvas
H = 600
# liste de couleurs
COULEUR = [
    "#000000",  # 0 - blanc
    "#FF0000",  # 1 - rouge
    "#00FF00",  # 2 - vert
    "#0000FF",  # 3 - bleu
    "#FFFF00",  # 4 - cyan
    "#00FFFF",  # 5 - jaune
    "#FF00FF",  # 6 - magenta
    "#FFFFFF"   # 7 - noir
]

# Variable globale
grille = [[randint(0, 6) for _ in range(3)] for _ in range(3)]

grille = [
    [1, 1, 1],
    [2, 2, 2],
    [3, 3, 3]
]


# Fonction
def init():
    pass


def avalanche():
    '''
        Transmet en parallèle 1 grain de sable à
        chaque voisin adjacent de la grille
        pour chaque case ayant au moins 4 grains.
        Ne prend pas de paramètre
        Rrenvoie le nombre de grain de la case ayant le plus
        de grain dans la grille.
    '''
    global grille
    n = len(grille)
    grilletmp = copy.deepcopy(grille)
    grain_max = 0
    voisins = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for i in range(len(grille)):
        for j in range(len(grille[0])):
            if grille[i][j] >= 4:
                # soustraction des grains à la case traitée
                grilletmp[i][j] = grilletmp[i][j] - 4

                # addition de 1 grain par voisin
                for p, q in voisins:
                    if 0 <= i + p < n and 0 <= j + q < n:
                        grilletmp[i + p][j + q] += 1

    grille = copy.deepcopy(grilletmp)
    grain_max = np.max(grille)
    return grain_max


def dessine_grille():
    '''
        Dessine la grille sur le canvas avec des couleurs
        en fonction du nombre de grains par case.
        Ne prend pas de paramètre.
        Ne renvoie rien.
    '''
    pass


def charger_config():
    ''' Charge une grille à partir d'un fichier .tds spécifié par l'utilisateur
        Ne prend pas de paramètre.
        Renvoie la grille charger si succès sinon None.
    '''
    f = tk_filedialog.askopenfile(
        initialdir=os.getcwd()+"/config/",
        title="charger une config",
        filetypes=(("fichier - tas de sable", "*.tds"),)
    )
    if f is None:
        return None

    grille2 = eval(f.readline())

    return grille2


def sauvegarder_config():
    '''
        Sauvegarde la grille actuelle dans un fichier .tds
        spécifié par l'utilisateur.
        Ne prend pas de paramètre.
        Ne renvoie rien.
    '''
    fichier = tk_filedialog.asksaveasfilename(
        initialdir=os.getcwd()+"/config/",
        title="Sauvergarder une config",
        defaultextension=(".tds"),
        filetypes=(("fichier - tas de sable", "*.tds"),)
    )

    if not fichier:
        return

    chemin = fichier.split('.')
    if len(chemin) != 2:
        return

    chemin, ext = chemin[:]
    if ext != 'tds':
        return

    with open(fichier, "w") as f:
        f.write(str(grille))
        f.close()


def addition_config():
    '''
        Modifie la grille actuelle avec une autre grille à
        partir d'un fichier .tds spécifié par l'utilisateur.
        Les cases des grilles sont additionné deux à deux.
        Ne prend pas de paramètre.
        Ne renvoie rien.
    '''
    global grille
    grille2 = charger_config()

    n = len(grille)
    n2 = len(grille2)
    if n != n2:
        return

    for i in range(n):
        for j in range(n):
            grille[i][j] += grille2[i][j]


def soustration_config():
    '''
        Modifie la grille actuelle avec une autre grille à
        partir d'un fichier .tds spécifié par l'utilisateur.
        Les cases de la grille spécifiée sont soutraite à celle de la grille.
        Ne prend pas de paramètre.
        Ne renvoie rien.
    '''
    global grille
    grille2 = charger_config()

    n = len(grille)
    n2 = len(grille2)
    if n != n2:
        return

    for i in range(n):
        for j in range(n):
            grille[i][j] -= grille2[i][j]
            if grille[i][j] < 0:
                grille[i][j] = 0


# Création widgets
root = tk.Tk()
root.title("Projet - tas de sable")

canvas = tk.Canvas(root, width=W, height=H, bg="blue")

bouton_aléatoire = tk.Button(root, text="Config aléatoire")
bouton_pile_centre = tk.Button(root, text="Config pile centrée")

# Placement widgets
canvas.grid(row=0, column=1, rowspan=8)

bouton_aléatoire.grid(row=0, column=0)
bouton_pile_centre.grid(row=1, column=0)


# Evenements widgets


# Boucle principale
print(*grille, sep="\n", end="\n\n")
while 1:
    grain_max = avalanche()
    print(*grille, sep="\n", end="\n\n")
    if grain_max < 4:
        break

root.mainloop()
