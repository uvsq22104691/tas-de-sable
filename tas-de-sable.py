# INFORMATION GROUPE
# GROUPE MI TD 03
# Mathis ALLOUCHE
# jennifer said
# xavier koubonou
# https://github.com/uvsq22104691/tas-de-sable


# Import
import tkinter as tk
# from random import randint


# Constante

# largeur du canvas
W = 600
# hauteur du canvas
H = 600


# Variable globale
grille = [
    [4, 5, 2],
    [4, 3, 0],
    [1, 5, 4]
]

# grille = [[randint(0, 6) for _ in range(3)] for _ in range(3)]


# Fonction
def avalanche():
    global grille
    n = len(grille)
    grilletmp = [[v for v in row] for row in grille]

    for i in range(len(grille)):
        for j in range(len(grille[0])):
            if grille[i][j] >= 4:
                grilletmp[i][j] = grilletmp[i][j] - 4
                for p, q in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    if 0 <= i + p < n and 0 <= j + q < n:
                        grilletmp[i + p][j + q] += 1
                print(*grilletmp, sep="\n", end="\n\n")
    grille = grilletmp.copy()


# Création widgets
root = tk.Tk()
root.title("Projet - tas de sable")

canvas = tk.Canvas(root, width=W, height=H, bg="blue")


# Placement widgets
canvas.grid(row=0, column=0)


# Evenements widgets


# Boucle principale
print(*grille, sep="\n", end="\n\n")
avalanche()
avalanche()
print(*grille, sep="\n", end="\n\n")
root.mainloop()
