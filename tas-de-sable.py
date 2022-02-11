# INFORMATION GROUPE
# GROUPE MI TD 03
# Mathis ALLOUCHE
# jennifer said
# xavier koubonou
# https://github.com/uvsq22104691/tas-de-sable


# Import
import tkinter as tk
import copy
import numpy as np
from random import randint


# Constante

# Largeur du canvas
W = 600
# Hauteur du canvas
H = 600
# Dictionnaire de couleur
COULEUR = {
    "noir": "000000",
    "rouge": "#FF0000",
    "vert": "#00FF00",
    "bleu": "#0000FF",
    "cyan": "#FFFF00",
    "jaune": "#00FFFF",
    "magenta": "#FF00FF",
    "blanc": "#FFFFFF",
}

# Variable globale
grille = [[randint(0, 6) for _ in range(3)] for _ in range(3)]

grille = [
    [1, 0, 4],
    [0, 1, 4],
    [0, 1, 2]
]


# Fonction
def avalanche():
    ''' avalanche() est une fonction qui transmet en parallèle
        1 grain de sable à chaque voisin de la grille en croix
        pour chaque case ayant au moins 4 grains.
        Elle renvoie le nombre de grain de la case ayant le plus
        de grain dans la grille
    '''
    global grille
    n = len(grille)
    grilletmp = copy.deepcopy(grille)
    grain_max = 0

    for i in range(len(grille)):
        for j in range(len(grille[0])):
            if grille[i][j] >= 4:
                grilletmp[i][j] = grilletmp[i][j] - 4
                for p, q in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    if 0 <= i + p < n and 0 <= j + q < n:
                        grilletmp[i + p][j + q] += 1

    grille = copy.deepcopy(grilletmp)
    grain_max = np.max(grille)
    return grain_max


def dessine_grille():
    pass


def charger_grille():
    pass


def sauvegarder_grille():
    pass


def addition_config():
    pass


def soustration_config():
    pass


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
