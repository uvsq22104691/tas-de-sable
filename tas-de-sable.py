# coding: utf-8

# INFORMATION GROUPE
# GROUPE MI TD 03
# Mathis ALLOUCHE
# jennifer said
# xavier koubonou
# https://github.com/uvsq22104691/tas-de-sable


# Import
import tkinter.filedialog as fd
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
N = 20

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

# Variable globale
G_grille = []
G_pause = True


# Fonction
def init():
    ''' Crée une grille aléatoire et l'affiche
        Vérification et création si besoin des grilles par défaut.
    '''
    global grille
    grille = [[randint(0, 8) for _ in range(N)] for _ in range(N)]


def avalanche(grille):
    ''' Transmet en parallèle 1 grain de sable à
        chaque voisin adjacent de la grille
        pour chaque case ayant au moins 4 grains.
        Rrenvoie le nombre de grain de la case ayant le plus
        de grain dans la grille (int).
    '''
    grilletmp = copy.deepcopy(grille)
    voisins = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for i in range(N):
        for j in range(N):
            if grille[i][j] >= 4:
                # soustraction des grains à la case traitée
                grilletmp[i][j] = grilletmp[i][j] - 4

                # addition de 1 grain par voisin
                for p, q in voisins:
                    try:
                        grilletmp[i + p][j + q] += 1
                    except IndexError:
                        pass

    grille = copy.deepcopy(grilletmp)
    grain_max = 0
    for i in grille:
        if grain_max < max(i):
            grain_max = max(i)

    return (grille, grain_max)


def stabilise(grille):
    if grille is None:
        global G_grille
        grille = G_grille

    while 1:
        grille, grain_max = avalanche(grille)
        if grille is G_grille:
            dessine_grille()

        if grain_max < 4:
            break
    return grille


def dessine_grille():
    ''' Dessine la grille sur le canvas avec des couleurs
        en fonction du nombre de grains par case.
    '''
    global G_grille
    canvas.delete('all')
    for i in range(N):
        for j in range(N):
            canvas.create_rectangle(
                (W/N) * j,
                (H/N) * i,
                (W/N) + (W/N) * j,
                (H/N) + (H/N) * i,
                fill=COULEUR[G_grille[i][j] if G_grille[i][j] < 11 else 10],
                width=0
            )
            canvas.create_text(
                (W/N)/2 + (W/N) * j,
                (H/N)/2 + (H/N) * i,
                text=str(G_grille[i][j]),
                width=50,
                fill="black" if G_grille[i][j] < 10 else "white"
            )
    canvas.update()


def fenetre_charger_config():
    ''' Charge une grille à partir d'un fichier .tds spécifié par l'utilisateur
        Renvoie la grille (list[list]) charger si succès sinon None.
    '''

    # On crée une nouvelle fenetre pour choisir la config à charger

    fen_option = tk.Tk()
    fen_option.title = "Fenêtre d'option"

    bouton_aléatoire = tk.Button(
        fen_option,
        text="Config aléatoire",
        command=lambda: charger_config("aleatoire")
    )

    bouton_pile_centre = tk.Button(
        fen_option,
        text="Config pile centrée",
        command=lambda: charger_config("pile_centree")
    )

    bouton_max_stable = tk.Button(
        fen_option,
        text="Config max stable",
        command=lambda: charger_config("max_stable")
    )

    bouton_max_stable = tk.Button(
        fen_option,
        text="Config max stable",
        command=lambda: charger_config("double_max_stable")
    )

    bouton_config_identity = tk.Button(
        fen_option,
        text="Config indentity",
        command=lambda: charger_config("identity")
    )

    bouton_charge_config = tk.Button(
        fen_option,
        text="Config indentity",
        command=lambda: charger_config("identity")
    )

    bouton_aléatoire.grid(row=0, column=0)
    bouton_pile_centre.grid(row=1, column=0)
    bouton_max_stable.grid(row=2, column=0)
    bouton_config_identity.grid(row=3, column=0)
    bouton_charge_config.grid(row=5, column=0)

    fen_option.mainloop()


def charger_config(conf=None):
    if conf is None:
        f = fd.askopenfile(
            initialdir=os.getcwd()+"/config/",
            title="charger une config",
            filetypes=(("fichier - tas de sable", "*.tds"),)
        )

        if f is None:
            return None
        return eval(f.readline())

    if conf == "aleatoire":
        return [[randint(0, 10) for _ in range(N)] for _ in range(N)]

    elif conf == "pile_centree":
        grilletmp = [[0] * N for _ in range(N)]
        nb_grains = 10
        grilletmp[N//2][N//2] = nb_grains
        return grilletmp

    elif conf == "max_stable":
        return [[3] * N for _ in range(N)]

    elif conf == "double_max_stable":
        return [[6] * N for _ in range(N)]

    elif conf == "identity":
        g1 = charger_config("double_max_stable")
        g1 = stabilise(g1)

        # return soustration_config(g1, )


def sauvegarder_config():
    ''' Sauvegarde la grille actuelle dans un fichier .tds
        spécifié par l'utilisateur.
    '''
    fichier = fd.asksaveasfilename(
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
        f.write(str(grille).replace(' ', ''))
        f.close()


def addition_config(g1=None, g2=None):
    ''' Modifie la grille actuelle avec une autre grille à
        partir d'un fichier .tds spécifié par l'utilisateur.
        Les cases des grilles sont additionné deux à deux.
    '''
    if g1 is not None and g2 is not None:  # addition des deux grilles
        for i in range(N):
            for j in range(N):
                g1[i][j] += g2[i][j]

        return g1

    global grille
    grille2 = charger_config()

    n = len(grille2)
    if n != N:
        return

    for i in range(n):
        for j in range(n):
            grille[i][j] += grille2[i][j]

    dessine_grille()


def soustration_config(g1=None, g2=None):
    ''' Modifie la grille actuelle avec une autre grille à
        partir d'un fichier .tds spécifié par l'utilisateur.
        Les cases de la grille spécifiée sont soutraite à celle de la grille.
    '''
    if g1 is not None and g2 is not None:  # addition des deux grilles
        for i in range(N):
            for j in range(N):
                g1[i][j] -= g2[i][j]
                if g1[i][j] < 0:
                    g1[i][j] = 0

        return g1

    global grille
    grille2 = charger_config()

    n = len(grille2)
    if n != N:
        return

    for i in range(n):
        for j in range(n):
            grille[i][j] -= grille2[i][j]
            if grille[i][j] < 0:
                grille[i][j] = 0


def change_pause():
    ''' Met en pause ou reprend les avalanches.'''
    # bouton_pause["text"]


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
bouton_option = tk.Button(root, text="option")

bouton_sauvegarder_config = tk.Button(
    root,
    text="Sauvegarder config",
    command=sauvegarder_config
)

bouton_charger_config = tk.Button(
    root,
    text="Charger config",
    command=fenetre_charger_config
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
canvas.grid(row=0, column=1, rowspan=7)
bouton_cinema.grid(row=0, column=0)
bouton_pause.grid(row=1, column=0)
bouton_option.grid(row=2, column=0)
bouton_sauvegarder_config.grid(row=3, column=0)
bouton_charger_config.grid(row=4, column=0)
bouton_addition_config.grid(row=5, column=0)
bouton_soustraction_config.grid(row=6, column=0)


# Evenements widgets


# Boucle principale
init()

grille = charger_config()
dessine_grille()


while 1:
    grille, grain_max = avalanche(grille)
    dessine_grille()
    if grain_max < 4:
        break

root.mainloop()
