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
import marshal
import os
from random import randint


# Constante
# Largeur du canvas
W = 600

# Hauteur du canvas
H = 600

# Largeur de la grille
N = 31

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
G_auto = True


# Fonction
def init():
    ''' Crée une grille aléatoire et l'affiche
        Vérification et création si besoin des grilles par défaut.
    '''
    global G_grille
    G_grille = [[randint(0, 8) for _ in range(N)] for _ in range(N)]
    dessine_grille()


def avalanche(grille):
    ''' Transmet en parallèle 1 grain de sable à
        chaque voisin adjacent de la grille
        pour chaque case ayant au moins 4 grains.
        Rrenvoie le nombre de grain de la case ayant le plus
        de grain dans la grille (int).
    '''
    grilletmp = marshal.loads(marshal.dumps(grille))
    voisins = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for i in range(N):
        for j in range(N):
            if grille[i][j] >= 4:
                # soustraction des grains à la case traitée
                grilletmp[i][j] = grilletmp[i][j] - 4

                # addition de 1 grain par voisin
                for p, q in voisins:
                    try:
                        if i + p == -1 or j + q == -1:
                            continue
                        grilletmp[i + p][j + q] += 1
                    except IndexError:
                        pass

    grille = marshal.loads(marshal.dumps(grilletmp))
    grain_max = 0
    for i in grille:
        if grain_max < max(i):
            grain_max = max(i)

    return (grille, grain_max)


def stabilise(grille=None, clicked=False):
    if clicked and (G_pause or G_auto):
        return
    global G_grille
    dessine = False

    if grille is None or grille is G_grille:
        grille = G_grille
        dessine = True

    grille, grain_max = avalanche(grille)
    if dessine:
        G_grille = grille
        dessine_grille()

    if grain_max >= 4 and not G_pause and G_auto:
        root.after(100, stabilise, grille)
    if grain_max < 4:
        if not G_pause:
            change_pause()

    return grille, grain_max


def dessine_grille():
    ''' Dessine la grille sur le canvas avec des couleurs
        en fonction du nombre de grains par case.
    '''
    global G_grille
    canvas.delete('all')
    for i in range(N):
        for j in range(N):
            canvas.create_rectangle(
                (W / N) * j,
                (H / N) * i,
                (W / N) + (W / N) * j,
                (H / N) + (H / N) * i,
                fill=COULEUR[G_grille[i][j] if G_grille[i][j] < 11 else 10],
                width=0
            )
            # canvas.create_text(
            #     (W / N) / 2 + (W / N) * j,
            #     (H / N) / 2 + (H / N) * i,
            #     text=str(G_grille[i][j]),
            #     width=50,
            #     fill="black" if G_grille[i][j] < 10 else "white"
            # )
    canvas.update()


def fenetre_charger_config():
    ''' Charge une grille à partir d'un fichier .tds spécifié par l'utilisateur
        Renvoie la grille (list[list]) charger si succès sinon None.
    '''

    # On crée une nouvelle fenetre pour choisir la config à charger

    fen_charge_conf = tk.Tk()
    fen_charge_conf.title("Fenêtre chargement config")

    bouton_aléatoire = tk.Button(
        fen_charge_conf,
        text="Aléatoire",
        command=lambda: charger_config("aleatoire", True)
    )

    bouton_pile_centre = tk.Button(
        fen_charge_conf,
        text="Pile centrée",
        command=lambda: charger_config("pile_centree", True)
    )

    entry_pile_centre = tk.Entry(
        fen_charge_conf
    )

    bouton_max_stable = tk.Button(
        fen_charge_conf,
        text="Max stable",
        command=lambda: charger_config("max_stable", True)
    )

    bouton_max_stable = tk.Button(
        fen_charge_conf,
        text="Double max stable",
        command=lambda: charger_config("double_max_stable", True)
    )

    bouton_config_identity = tk.Button(
        fen_charge_conf,
        text="Identity",
        command=lambda: charger_config("identity", True)
    )

    bouton_charge_config = tk.Button(
        fen_charge_conf,
        text="Fichier",
        command=lambda: charger_config(None, True)
    )

    bouton_aléatoire.grid(row=0, column=0, pady=20)
    bouton_pile_centre.grid(row=1, column=0, pady=20)
    entry_pile_centre.grid(row=1, column=1, padx=35, pady=20)
    bouton_max_stable.grid(row=2, column=0, padx=35, pady=20)
    bouton_config_identity.grid(row=3, column=0, pady=20)
    bouton_charge_config.grid(row=5, column=0, pady=20)

    fen_charge_conf.mainloop()


def charger_config(conf=None, replace_G_grille=False):
    if conf is None:
        f = fd.askopenfile(
            initialdir=os.getcwd() + "/config/",
            title="charger une config",
            filetypes=(("fichier - tas de sable", "*.tds"),)
        )

        if f is None:
            return None
        global N
        g = eval(f.readline())
        N = len(g)
        config = g

    elif conf == "aleatoire":
        config = [[randint(0, 10) for _ in range(N)] for _ in range(N)]

    elif conf == "pile_centree":
        grilletmp = [[0] * N for _ in range(N)]
        nb_grains = 10
        if N % 2 == 0:
            grilletmp[(N // 2) - 1][(N // 2) - 1] = nb_grains
            grilletmp[(N // 2) - 1][N // 2] = nb_grains
            grilletmp[N // 2][(N // 2) - 1] = nb_grains
            grilletmp[N // 2][N // 2] = nb_grains
        else:
            grilletmp[N // 2][N // 2] = nb_grains
        config = grilletmp

    elif conf == "max_stable":
        config = [[3] * N for _ in range(N)]

    elif conf == "double_max_stable":
        config = [[6] * N for _ in range(N)]

    elif conf == "identity":
        g1 = charger_config("double_max_stable")

        g2, grain_max = avalanche(g1)
        while grain_max >= 4:
            g2, grain_max = avalanche(g2)
        config = soustration_config(g1, g2)

        config, grain_max = avalanche(config)
        while grain_max >= 4:
            config, grain_max = avalanche(config)

    if replace_G_grille:
        global G_grille
        G_grille = config
        dessine_grille()
        if not G_pause:
            change_pause()
    return config


def sauvegarder_config():
    ''' Sauvegarde la grille actuelle dans un fichier .tds
        spécifié par l'utilisateur.
    '''
    fichier = fd.asksaveasfilename(
        initialdir=os.getcwd() + "/config/",
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
        f.write(str(G_grille).replace(' ', ''))
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

    global G_grille
    grille2 = charger_config()

    n = len(grille2)
    if n != N:
        return

    for i in range(n):
        for j in range(n):
            G_grille[i][j] += grille2[i][j]

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

    global G_grille
    grille2 = charger_config()

    n = len(grille2)
    if n != N:
        return

    for i in range(n):
        for j in range(n):
            G_grille[i][j] -= grille2[i][j]
            if G_grille[i][j] < 0:
                G_grille[i][j] = 0
    dessine_grille()


def change_pause():
    ''' Met en pause ou reprend les avalanches.'''
    global G_pause
    bouton_pause['text'] = "Pause" if bouton_pause['text'] == "Reprendre" else "Reprendre"
    G_pause = not G_pause
    if not G_pause and G_auto:
        stabilise(G_grille)


def change_affichage():
    ''' Change la façon dont les avalanches sont appelé.
        cinéma : auto avec x secondes d'intervalles.
        clique : manuel une avalanche par clique.
    '''
    global G_auto
    bouton_cinema['text'] = "Cinéma" if bouton_cinema['text'] == "Clique" else "Clique"
    G_auto = not G_auto
    if not G_pause:
        change_pause()


def change_options():
    fen_change_opt = tk.Tk()
    fen_change_opt.title("Fenêtre d'options")

    bouton_aléatoire = tk.Button(
        fen_change_opt,
        text="Aléatoire",
        command=lambda: charger_config("aleatoire", True)
    )

    bouton_pile_centre = tk.Button(
        fen_change_opt,
        text="Pile centrée",
        command=lambda: charger_config("pile_centree", True)
    )

    bouton_max_stable = tk.Button(
        fen_change_opt,
        text="Max stable",
        command=lambda: charger_config("max_stable", True)
    )

    bouton_max_stable = tk.Button(
        fen_change_opt,
        text="Double max stable",
        command=lambda: charger_config("double_max_stable", True)
    )

    bouton_config_identity = tk.Button(
        fen_change_opt,
        text="Identity",
        command=lambda: charger_config("identity", True)
    )

    bouton_charge_config = tk.Button(
        fen_change_opt,
        text="Fichier",
        command=lambda: charger_config(None, True)
    )

    bouton_aléatoire.grid(row=0, column=0, pady=20)
    bouton_pile_centre.grid(row=1, column=0, pady=20)
    bouton_max_stable.grid(row=2, column=0, padx=35, pady=20)
    bouton_config_identity.grid(row=3, column=0, pady=20)
    bouton_charge_config.grid(row=5, column=0, pady=20)

    fen_change_opt.mainloop()


# Création widgets
root = tk.Tk()
root.title("Projet - tas de sable")

canvas = tk.Canvas(root, width=W, height=H, bg="white")
bouton_cinema = tk.Button(root, text="Cinéma", command=change_affichage)
bouton_pause = tk.Button(root, text="Reprendre", command=change_pause)
bouton_option = tk.Button(root, text="Options", command=change_options)

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
bouton_soustraction_config.grid(row=6, column=0, padx=20)


# Evenements widgets
root.bind('<space>', lambda e: stabilise(None, True))

# Boucle principale
init()
root.mainloop()
