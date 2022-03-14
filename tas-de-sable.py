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
import numpy as np


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
G_auto = True
G_clique_grain = 0
G_aff_nombre = True
G_tps_avalanche = 100
G_voisins = 4
G_voisins_l = ((1, 0), (0, 1), (0, -1), (-1, 0))


# Fonction
def init():
    ''' Crée une grille aléatoire et l'affiche
        Vérification et création si besoin des grilles par défaut.
    '''
    global G_grille
    G_grille = [list(map(int, np.random.randint(11, size=N))) for _ in range(N)]
    dessine_grille()


def avalanche(grille):
    ''' Transmet en parallèle 1 grain de sable à
        chaque voisin adjacent de la grille
        pour chaque case ayant au moins 4 grains.
        Rrenvoie le nombre de grain de la case ayant le plus
        de grain dans la grille (int).'''

    grilletmp = marshal.loads(marshal.dumps(grille))

    for y in range(N):
        for x in range(N):
            if grille[y][x] >= G_voisins:
                grilletmp[y][x] -= G_voisins

                for p, q in G_voisins_l:
                    if y + p not in (-1, N) and x + q not in (-1, N):
                        grilletmp[y + p][x + q] += 1

    grille = marshal.loads(marshal.dumps(grilletmp))
    grain_max = np.max(grille)

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

    if grain_max >= G_voisins and not G_pause and G_auto:
        root.after(G_tps_avalanche, stabilise, grille)
    if grain_max < G_voisins:
        if not G_pause:
            change_pause()

    return grille, grain_max


def dessine_grille():
    ''' Dessine la grille sur le canvas avec des couleurs
        en fonction du nombre de grains par case.
    '''
    global G_grille, G_aff_nombre
    canvas.delete('all')
    for y in range(N):
        for x in range(N):
            canvas.create_rectangle(
                (W / N) * x,
                (H / N) * y,
                (W / N) + (W / N) * x,
                (H / N) + (H / N) * y,
                fill=COULEUR[G_grille[y][x] if G_grille[y][x] < 11 else 10],
                tags=((y, x)),
                width=0
            )
            if G_aff_nombre:
                canvas.create_text(
                    (W / N) / 2 + (W / N) * x,
                    (H / N) / 2 + (H / N) * y,
                    text=str(G_grille[y][x]),
                    tags=((y, x)),
                    width=50,
                    fill="black" if G_grille[y][x] < 10 else "white"
                )
    canvas.update()


def dessine_case(y, x):
    canvas.delete((y, x))
    canvas.create_rectangle(
        (W / N) * x,
        (H / N) * y,
        (W / N) + (W / N) * x,
        (H / N) + (H / N) * y,
        fill=COULEUR[G_grille[y][x] if G_grille[y][x] < 11 else 10],
        tags=((y, x)),
        width=0
    )
    if G_aff_nombre:
        canvas.create_text(
            (W / N) / 2 + (W / N) * x,
            (H / N) / 2 + (H / N) * y,
            text=str(G_grille[y][x]),
            tags=((y, x)),
            width=50,
            fill="black" if G_grille[y][x] < 10 else "white"
        )


def del_fen(fen):
    global fen_charge_conf, fen_change_opt
    if "fen_charge_conf" in globals():
        global entry_aleatoire_min, entry_aleatoire_max
        fen_charge_conf.destroy()
        del fen_charge_conf
        del entry_aleatoire_min
        del entry_aleatoire_max
    else:
        fen_change_opt.destroy()
        del fen_change_opt


def fenetre_config(action="replace", name="Fenêtre chargement config"):
    ''' Charge une grille à partir d'un fichier .tds spécifié par l'utilisateur
        Renvoie la grille (list[list]) charger si succès sinon None.
    '''

    # On crée une nouvelle fenetre pour choisir la config à charger
    global fen_charge_conf
    if "fen_charge_conf" in globals():
        if name == fen_charge_conf.title():
            fen_charge_conf.focus_force()
            return
        del_fen(fen_charge_conf)

    fen_charge_conf = tk.Tk()
    fen_charge_conf.protocol("WM_DELETE_WINDOW", lambda: del_fen(fen_charge_conf))
    fen_charge_conf.title(name)

    style_button = {
        "master": fen_charge_conf,
        "height": 1,
        "width": 15,
        "font": ('Ebrima', 12)
    }
    style_label = {
        "master": fen_charge_conf,
        "font": ('Ebrima', 12)
    }
    style_entry = {
        "master": fen_charge_conf,
        "font": ('Ebrima', 12),
        "width": 5
    }

    bouton_aleatoire = tk.Button(
        **style_button,
        text="Aléatoire",
        command=lambda: charger_config("aleatoire", action)
    )

    global label_min
    label_min = tk.Label(
        **style_label,
        text="min:"
    )

    global entry_aleatoire_min
    entry_aleatoire_min = tk.Entry(
        **style_entry
    )
    entry_aleatoire_min.insert(-1, "0")

    global label_max
    label_max = tk.Label(
        **style_label,
        text="max:"
    )

    global entry_aleatoire_max
    entry_aleatoire_max = tk.Entry(
        **style_entry
    )
    entry_aleatoire_max.insert(-1, "10")

    bouton_pile_centre = tk.Button(
        **style_button,
        text="Pile centrée",
        command=lambda: charger_config("pile_centree", action)
    )

    global label_pile_centre
    label_pile_centre = tk.Label(
        **style_label,
        text="grains:"
    )

    global entry_pile_centre
    entry_pile_centre = tk.Entry(
        **style_entry
    )
    entry_pile_centre.insert(-1, "100")

    bouton_max_stable = tk.Button(
        **style_button,
        text="Max stable",
        command=lambda: charger_config("max_stable", action)
    )

    bouton_double_max_stable = tk.Button(
        **style_button,
        text="Double max stable",
        command=lambda: charger_config("double_max_stable", action)
    )

    bouton_config_identity = tk.Button(
        **style_button,
        text="Identity",
        command=lambda: charger_config("identity", action)
    )

    bouton_charge_config = tk.Button(
        **style_button,
        text="Fichier",
        command=lambda: charger_config(None, action)
    )

    bouton_aleatoire.grid(row=0, column=0, pady=10)
    label_min.grid(row=0, column=1, pady=(0, 4))
    entry_aleatoire_min.grid(row=0, column=2, padx=(10, 35))
    label_max.grid(row=0, column=3, pady=(0, 4))
    entry_aleatoire_max.grid(row=0, column=4, padx=(10, 35))

    bouton_pile_centre.grid(row=1, column=0, pady=10)
    label_pile_centre.grid(row=1, column=1, pady=(0, 4))
    entry_pile_centre.grid(row=1, column=2, padx=(10, 35), pady=10)

    bouton_max_stable.grid(row=2, column=0, padx=35, pady=10)

    bouton_double_max_stable.grid(row=3, column=0, padx=35, pady=10)

    bouton_config_identity.grid(row=4, column=0, pady=10)

    bouton_charge_config.grid(row=5, column=0, pady=10)

    fen_charge_conf.mainloop()


def charger_config(conf=None, action="replace"):
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
        global entry_aleatoire_min, entry_aleatoire_max
        mini, maxi = 0, 11
        if "entry_aleatoire_min" in globals():
            if entry_aleatoire_min.get().isdecimal() and int(entry_aleatoire_min.get()) >= 0:
                mini = int(entry_aleatoire_min.get())
            if entry_aleatoire_max.get().isdecimal() and int(entry_aleatoire_max.get()) >= 0:
                maxi = int(entry_aleatoire_max.get()) + 1
            if maxi - 1 < mini:
                mini, maxi = maxi - 1, mini + 1
        config = [list(map(int, np.random.randint(mini, maxi, size=N))) for _ in range(N)]

    elif conf == "pile_centree":
        global entry_pile_centre
        grilletmp = [[0] * N for _ in range(N)]
        nb_grains = 10
        if entry_pile_centre.get().isdecimal():
            nb_grains = int(entry_pile_centre.get())
        if N % 2 == 0:
            grilletmp[(N // 2) - 1][(N // 2) - 1] = nb_grains
            grilletmp[(N // 2) - 1][N // 2] = nb_grains
            grilletmp[N // 2][(N // 2) - 1] = nb_grains
            grilletmp[N // 2][N // 2] = nb_grains
        else:
            grilletmp[N // 2][N // 2] = nb_grains
        config = grilletmp

    elif conf == "max_stable":
        g = G_voisins - 1
        config = [[g] * N for _ in range(N)]

    elif conf == "double_max_stable":
        g = (G_voisins - 1) * 2
        config = [[g] * N for _ in range(N)]

    elif conf == "identity":
        g1 = charger_config("double_max_stable", "return")

        g2, grain_max = avalanche(g1)
        while grain_max >= G_voisins:
            g2, grain_max = avalanche(g2)
        config = soustration_config(g1, g2)

        config, grain_max = avalanche(config)
        while grain_max >= G_voisins:
            config, grain_max = avalanche(config)

    if action == "replace":
        global G_grille
        G_grille = config
    elif action == "addition":
        addition_config(config)
    elif action == "soustraction":
        soustration_config(config)
    elif action == "return":
        return config

    dessine_grille()
    if not G_pause:
        change_pause()


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


def addition_config(g1, g2=None):
    ''' Modifie la grille actuelle avec une autre grille à
        partir d'un fichier .tds spécifié par l'utilisateur.
        Les cases des grilles sont additionné deux à deux.
    '''
    if g1 is not None and g2 is not None:  # addition des deux grilles
        for y in range(N):
            for x in range(N):
                g1[y][x] += g2[y][x]

        return g1

    global G_grille

    n = len(g1)
    if n != N:
        return

    for y in range(n):
        for x in range(n):
            G_grille[y][x] += g1[y][x]

    dessine_grille()


def soustration_config(g1, g2=None):
    ''' Modifie la grille actuelle avec une autre grille à
        partir d'un fichier .tds spécifié par l'utilisateur.
        Les cases de la grille spécifiée sont soutraite à celle de la grille.
    '''
    if g1 is not None and g2 is not None:  # addition des deux grilles
        for y in range(N):
            for x in range(N):
                g1[y][x] -= g2[y][x]
                if g1[y][x] < 0:
                    g1[y][x] = 0

        return g1

    global G_grille

    n = len(g1)
    if n != N:
        return

    for y in range(n):
        for x in range(n):
            G_grille[y][x] -= g1[y][x]
            if G_grille[y][x] < 0:
                G_grille[y][x] = 0
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
        Espace : manuel une avalanche par clique.
    '''
    global G_auto
    bouton_cinema['text'] = "Cinéma" if bouton_cinema['text'] == "Espace" else "Espace"
    G_auto = not G_auto
    if not G_pause:
        change_pause()


def applique_ch_opt():
    global fen_change_opt, v_aff_nombre, v_nb_voisins, G_aff_nombre, entry_taille, entry_clique_grain, entry_tps_avalanche, N, G_clique_grain, G_tps_avalanche, G_voisins_l, G_voisins

    G_aff_nombre = v_aff_nombre.get() == 1
    G_voisins = v_nb_voisins.get()
    try:
        if int(entry_taille.get()) != N and int(entry_taille.get()) > 0:
            N = int(entry_taille.get())
            charger_config("aleatoire")

        G_clique_grain = int(entry_clique_grain.get())

        if int(entry_taille.get()) >= 0:
            G_tps_avalanche = int(entry_tps_avalanche.get())

        if G_voisins == 8:
            G_voisins_l = ((1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1))
        else:
            G_voisins_l = ((1, 0), (0, 1), (0, -1), (-1, 0))

    except ValueError:
        pass

    dessine_grille()


def fenetre_options():
    global fen_change_opt
    if "fen_change_opt" in globals():
        fen_change_opt.focus_force()
        return

    fen_change_opt = tk.Tk()
    fen_change_opt.protocol("WM_DELETE_WINDOW", lambda: del_fen(fen_change_opt))
    fen_change_opt.title("Fenêtre d'options")

    global v_aff_nombre, entry_taille, entry_clique_grain, entry_tps_avalanche, v_nb_voisins
    v_aff_nombre = tk.IntVar(fen_change_opt)
    v_nb_voisins = tk.IntVar(fen_change_opt)

    style_label = {
        "master": fen_change_opt,
        "font": ('Ebrima', 12)
    }

    style_check = {
        "master": fen_change_opt,
        "width": 2
    }

    style_button = {
        "master": fen_change_opt,
        "font": ('Ebrima', 12)
    }

    style_entry = {
        "master": fen_change_opt,
        "width": 5,
        "font": ('Ebrima', 12)
    }

    style_radio = {
        "master": fen_change_opt,
        "width": 8,
        "font": ('Ebrima', 12),
        "variable": v_nb_voisins
    }

    label_taille = tk.Label(
        **style_label,
        text="Taille de la grille (eniter > 0) :"
    )
    entry_taille = tk.Entry(
        **style_entry
    )
    entry_taille.insert(-1, N)

    label_clique_grain = tk.Label(
        **style_label,
        text="Grain à ajouter lors d'un clique (entier) :"
    )
    entry_clique_grain = tk.Entry(
        **style_entry
    )
    entry_clique_grain.insert(-1, G_clique_grain)

    label_tps_avalanche = tk.Label(
        **style_label,
        text="Temps entre chaque avalanche (en ms) :"
    )
    entry_tps_avalanche = tk.Entry(
        **style_entry
    )
    entry_tps_avalanche.insert(-1, G_tps_avalanche)

    label_aff_nombre = tk.Label(
        **style_label,
        text="Afficher le nombres de grains dans les cases :"
    )
    check_aff_nombre = tk.Checkbutton(
        **style_check,
        variable=v_aff_nombre
    )
    if G_aff_nombre:
        check_aff_nombre.select()

    radio_4_voisins = tk.Radiobutton(
        **style_radio,
        text="4 voisins",
        value=4
    )
    radio_8_voisins = tk.Radiobutton(
        **style_radio,
        text="8 voisins",
        value=8
    )
    if G_voisins == 4:
        radio_4_voisins.select()
    else:
        radio_8_voisins.select()

    button_applique = tk.Button(
        **style_button,
        text="Appliquer les changements",
        command=applique_ch_opt
    )

    label_taille.grid(row=0, column=0, columnspan=2, padx=10, sticky="e")
    entry_taille.grid(row=0, column=2, padx=(0, 10))

    label_clique_grain.grid(row=1, column=0, columnspan=2, padx=10, sticky="e")
    entry_clique_grain.grid(row=1, column=2, padx=(0, 10))

    label_tps_avalanche.grid(row=2, column=0, columnspan=2, padx=10, sticky="e")
    entry_tps_avalanche.grid(row=2, column=2, padx=(0, 10))

    label_aff_nombre.grid(row=3, column=0, columnspan=2, padx=10, sticky="e")
    check_aff_nombre.grid(row=3, column=2, padx=(0, 10))

    radio_4_voisins.grid(row=4, column=0)
    radio_8_voisins.grid(row=4, column=1)

    button_applique.grid(row=5, column=0, columnspan=3, pady=10)
    fen_change_opt.mainloop()


def clique_grain(e):
    y, x = int(e.y // (H / N)), int(e.x // (W / N))

    if G_grille[y][x] + G_clique_grain >= 0:
        G_grille[y][x] += G_clique_grain
    else:
        G_grille[y][x] = 0

    dessine_case(y, x)


# Création widgets
root = tk.Tk()
root.title("Projet - tas de sable")

canvas = tk.Canvas(root, width=W, height=H, bg="white")
bouton_cinema = tk.Button(root, text="Cinéma", command=change_affichage)
bouton_pause = tk.Button(root, text="Reprendre", command=change_pause)
bouton_option = tk.Button(root, text="Options", command=fenetre_options)

bouton_sauvegarder_config = tk.Button(
    root,
    text="Sauvegarder config",
    command=sauvegarder_config
)

bouton_charger_config = tk.Button(
    root,
    text="Charger config",
    command=lambda: fenetre_config("replace")
)

bouton_addition_config = tk.Button(
    root,
    text="Addition config",
    command=lambda: fenetre_config("addition", "Fenêtre addition config")
)

bouton_soustraction_config = tk.Button(
    root,
    text="Soustraction_config",
    command=lambda: fenetre_config("soustraction", "Fenêtre soustraction config")
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
canvas.bind("<Button-1>", clique_grain)
# Boucle principale
init()
root.mainloop()
