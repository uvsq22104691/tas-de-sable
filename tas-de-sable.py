# coding: utf-8

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
import os
from random import randint


# Constante


# Largeur du canvas
W = 600

# Hauteur du canvas
H = 600

# Largeur de la grille
N = 10

# liste de couleurs
COULEUR = [
    "#FFFFFF",  # 0 - blanc
    "#FFFF80",  # 1 - jaune clair
    "#FFFF00",  # 2 - jaune
    "#E1E116",  # 3 - jaune foncé
    "#FFD780",  # 4 - orange clair
    "#FFAF00",  # 5 - orange
    "#B27A00",  # 6 - orange foncé
    "#F93838",  # 7 - rouge clair
    "#FF0000",  # 8 - rouge
    "#8F0000",  # 9 - rouge foncé
    "#000000"   # 10 - noir
]


# Fonction
def init():
    ''' Crée une grille aléatoire et l'affiche
        Vérification et création si besoin des grilles par défaut.
    '''
    global grille
    grille = [[randint(0, 10) for _ in range(N)] for _ in range(N)]

    if not os.path.exists(f"{os.getcwd()}/aleatoire"):
        pass
    if not os.path.exists(f"{os.getcwd()}/pile_centree"):
        pass
    if not os.path.exists(f"{os.getcwd()}/max_stable"):
        pass
    if not os.path.exists(f"{os.getcwd()}/identity"):
        pass


def avalanche():
    ''' Transmet en parallèle 1 grain de sable à
        chaque voisin adjacent de la grille
        pour chaque case ayant au moins 4 grains.
        Rrenvoie le nombre de grain de la case ayant le plus
        de grain dans la grille (int).
    '''
    global grille
    grilletmp = copy.deepcopy(grille)
    voisins = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for i in range(N):
        for j in range(N):
            if grille[i][j] >= 4:
                # soustraction des grains à la case traitée
                grilletmp[i][j] = grilletmp[i][j] - 4

                # addition de 1 grain par voisin
                for p, q in voisins:
                    if 0 <= i + p < N and 0 <= j + q < N:
                        grilletmp[i + p][j + q] += 1

    grille = copy.deepcopy(grilletmp)
    grain_max = 0
    for i in grille:
        if grain_max < max(i):
            grain_max = max(i)

    dessine_grille()
    return grain_max


def dessine_grille():
    ''' Dessine la grille sur le canvas avec des couleurs
        en fonction du nombre de grains par case.
    '''
    canvas.delete('all')
    for i in range(N):
        for j in range(N):
            canvas.create_rectangle(
                (W/N) * i,
                (H/N) * j,
                (W/N) + (W/N) * i,
                (H/N) + (H/N) * j,
                fill=COULEUR[grille[i][j] if grille[i][j] < 11 else 10],
                width=0
            )
            # canvas.create_text(
            #     (W/N)/2 + (W/N) * i,
            #     (H/N)/2 + (H/N) * j,
            #     text=str(grille[i][j]),
            #     width=50
            # )
    canvas.update()


def charger_config(action=None):
    ''' Charge une grille à partir d'un fichier .tds spécifié par l'utilisateur
        Renvoie la grille (list[list]) charger si succès sinon None.
    '''

    # On charge une config précise
    if action is not None:
        f = f"{action}.tds"
        with open(f, "r") as file:
            grille2 = eval(file.readline())
            file.close()
        return grille2

    # On charge une config en utilisant un explorateur de fichier
    f = tk_filedialog.askopenfile(
        initialdir=os.getcwd()+"/config/",
        title="charger une config",
        filetypes=(("fichier - tas de sable", "*.tds"),)
    )

    if f is None:
        return None

    return eval(f.readline())


def sauvegarder_config():
    ''' Sauvegarde la grille actuelle dans un fichier .tds
        spécifié par l'utilisateur.
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
    ''' Modifie la grille actuelle avec une autre grille à
        partir d'un fichier .tds spécifié par l'utilisateur.
        Les cases des grilles sont additionné deux à deux.
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
    ''' Modifie la grille actuelle avec une autre grille à
        partir d'un fichier .tds spécifié par l'utilisateur.
        Les cases de la grille spécifiée sont soutraite à celle de la grille.
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


def change_pause():
    ''' Met en pause ou reprend les avalanches.'''
    pass


def change_affichage():
    ''' Change la façon dont les avalanches sont appelé.
        ciné : auto avec x secondes d'intervalles.
        clique : manuel une avalanche par clique.
        '''
    pass


# Création widgets
root = tk.Tk()
root.title("Projet - tas de sable")

canvas = tk.Canvas(root, width=W, height=H, bg="blue")
bouton_cinema = tk.Button(root, text="cinéma", command=change_affichage)
bouton_pause = tk.Button(root, text="pause", command=change_pause)

bouton_aléatoire = tk.Button(
    root,
    text="Config aléatoire",
    command=lambda: charger_config("aleatoire")
)

bouton_pile_centre = tk.Button(
    root,
    text="Config pile centrée",
    command=lambda: charger_config("pile_centree")
)

bouton_max_stable = tk.Button(
    root,
    text="Config max stable",
    command=lambda: charger_config("max_stable")
)

bouton_config_identity = tk.Button(
    root,
    text="Config indentity",
    command=lambda: charger_config("identity")
)

bouton_sauvegarder_config = tk.Button(
    root,
    text="Sauvegarder config",
    command=sauvegarder_config
)

bouton_charger_config = tk.Button(
    root,
    text="Charger config",
    command=charger_config
)

bouton_addition_config = tk.Button(
    root,
    text="Addition config",
    command=addition_config
)

bouton_soustraction_config = tk.Button(
    root,
    text="Soustraction_config",
    command=soustration_config
)


# Placement widgets
canvas.grid(row=0, column=1, rowspan=10)
bouton_cinema.grid(row=0, column=0)
bouton_pause.grid(row=1, column=0)
bouton_aléatoire.grid(row=2, column=0)
bouton_pile_centre.grid(row=3, column=0)
bouton_max_stable.grid(row=4, column=0)
bouton_config_identity.grid(row=5, column=0)
bouton_sauvegarder_config.grid(row=6, column=0)
bouton_charger_config.grid(row=7, column=0)
bouton_addition_config.grid(row=8, column=0)
bouton_soustraction_config.grid(row=9, column=0)


# Evenements widgets


# Boucle principale
init()

dessine_grille()

while 1:
    grain_max = avalanche()
    if grain_max < 4:
        break

root.mainloop()
