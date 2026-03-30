import random
import sys
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseEvent
import pygame
import math


def charger_grille(nom_fichier: str) -> list[list[int]]:
    """
    Lit un fichier csv et transforme les données en une liste 2D d'entiers.
    
    entrée :
        - nom_fichier (str) : Le nom du fichier
    
    sortie :
        - grille (list[list[int]]) 
    """
    grille = []
    with open(nom_fichier) as f :
        for ligne in f:
            ligne_propre = ligne.strip()
            liste_nb = ligne_propre.split()
            valeurs = []
            for x in liste_nb:
                nombre = int(x)
                valeurs.append(nombre)
            if len(valeurs) != 0:
                grille.append(valeurs)
                
    return grille


def affichage_grille_terminal(grille: list[list[int]]):
    """
    Affiche la grille dans la console pour le debug.
    entrée :
        - grille (list[list[int]]) 
    sortie :
        - None 
    """
    print("   ", end="")
    for c in range(len(grille[0])): 
        print(f"{c} ", end="")

    print() 
    print("   " + "--" * len(grille[0]))
    
    for i in range(len(grille)):
        print(f"{i} |", end=" ")
        
        for j in range(len(grille[i])):
            case = grille[i][j]
            if case == -1:
                print(". ", end="")
            else:
                print(f"{case} ", end="")
        print()
    print()
    plt.pause(0.3)

def affichage_grille_matplotlib(grille: list[list[int]], points: int, tours: int) :
    """
    Affiche la grille en utilisant matplotlib
    entrée :
        - grille (list[list[int]]) 
    sortie :
        - None 
    """

    plt.clf()
    fig = plt.gcf()
    ax = fig.gca()
    
    fig.patch.set_facecolor('white') # fond blanc
    ax.set_facecolor('black')        # carré noir
    
    nb_lignes, nb_colonnes = len(grille), len(grille[0])
    couleurs = ['red', 'green', 'blue', 'yellow', 'magenta', 'cyan', 'orange']
    
    # def des bonbons(cercles)
    for ligne in range(nb_lignes):
        for colonne in range(nb_colonnes):
            valeur = grille[ligne][colonne]
            if valeur != -1:
                couleur = couleurs[valeur]
                # placement au centre de la case sinon ça part en couille
                cercle = plt.Circle((colonne, nb_lignes - 1 - ligne), 0.4, color=couleur)
                ax.add_patch(cercle)
    
    ax.set_xticks(range(nb_colonnes))
    ax.set_yticks(range(nb_lignes))
    
    ax.set_xticklabels(range(nb_colonnes), color='black', fontsize=10)
    #inversion pour les lignes pour 0 en haut
    ax.set_yticklabels(range(nb_lignes-1, -1, -1), color='black', fontsize=10)
    
    # placement des lignes de grille entre les numéros (tous les .5)
    ax.set_xticks([x - 0.5 for x in range(nb_colonnes + 1)], minor=True)
    ax.set_yticks([y - 0.5 for y in range(nb_lignes + 1)], minor=True)
    ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.5, zorder=0)
    
    # apparence carré (sinon ça fait des ovales bizarre)
    ax.set_xlim(-0.5, nb_colonnes - 0.5)
    ax.set_ylim(-0.5, nb_lignes - 0.5)
    ax.set_aspect('equal')
    
    plt.title(f"Bonbon Beguin de Gabriel² \nPoints : {points}\nTours restants : {tours}", color='purple', pad=20)
    
    if points >= 50:
        plt.title(f"GAGNÉ!!! \nScore : {points}\nTours restants : {tours}", color='red', fontsize=20, fontweight='bold')
    elif tours <= 0:
        plt.title(f"GAME OVER\nScore Final : {points}", color='black', fontsize=20)
    
    plt.draw()
    plt.pause(0.4)
    


def echanger_bonbons(grille: list[list[int]], l1: int, c1: int, l2: int, c2: int):
    """
    Intervertit les positions de deux bonbons ciblés dans la grille.
    entrée : 
        - grille (list[list[int]]) 
        - l1 (int)
        - c1 (int)
        - l2 (int)
        - c2 (int)
    """
    grille[l1][c1], grille[l2][c2] = grille[l2][c2], grille[l1][c1]


def detecter_alignements(grille: list[list[int]]) -> set[tuple[int]] : # decouverte des ensembles c'est une dinguerie
    """
    Détecte les alignements horizontaux et verticaux de 3 bonbons ou plus, en ligne ou en colonne.
    entrée :
        - grille (list[list[int]]) : la grille
    sortie :
        - a_supprimer (set[tuple[int]]) : coord des bonbons à supprimer
    """
    a_supprimer = set()
    nb_lignes = len(grille)
    nb_colonnes = len(grille[0])

    # horizontal
    for y in range(0, nb_lignes) :
        for x in range(0, nb_colonnes-2) :
            if grille[y][x] == grille[y][x+1] == grille[y][x+2] :
                a_supprimer |= chunk_meme_couleur(grille, (y, x))
    
    # vertical
    for x in range(0, nb_colonnes) :
        for y in range(0, nb_lignes-2) :
            if grille[y][x] == grille[y+1][x] == grille[y+2][x] :
                a_supprimer |= chunk_meme_couleur(grille, (y, x))

    return a_supprimer


def chunk_meme_couleur(grille: list[list[int]], case: tuple[int]) -> set[tuple[int]] :
    """
    Trouve et renvoie les coordonnées de toutes les cases de mêmes couleurs adjacentes entre elles

    entrée :
        - grille : (list[list[int]])
        - case (tuple[int]) : la case à partir de laquelle partir
    sortie :
        - chunk : (set[tuple[int]]) : Les coord du bloc
    """
    chunk = set()
    a_check = set()
    a_check.add(case)
    couleur = grille[case[0]][case[1]]
    nouveau_a_trouver = True
    while nouveau_a_trouver :
        new_a_check = set()
        nouveau_a_trouver = False
        for el in a_check :
            if grille[el[0]][el[1]] == couleur and el not in chunk :
                nouveau_a_trouver = True
                chunk.add(el)
                for (y, x) in [[1, 0], [-1, 0], [0, 1], [0, -1]] :
                    y += el[0]; x += el[1]
                    if x >= 0 and y >= 0 and x < len(grille[0]) and y < len(grille) :
                        new_a_check.add((y, x))
                a_check = new_a_check
    return chunk
        

def faire_tomber_bonbons(grille: list[list[int]]):
    """
    Fais descendre les bonbons.
    entrée : 
        - grille (list[list[int]]) 
    sortie :
        - None
    """
    # la gravité fonctionne dans l'autre sens. désolé Newton.
    nb_lignes, nb_colonnes = len(grille), len(grille[0])
    for colonne in range(nb_colonnes):
        pos_vide = nb_lignes - 1
        for ligne in range(nb_lignes - 1, -1, -1):
            if grille[ligne][colonne] != -1:
                grille[pos_vide][colonne] = grille[ligne][colonne]
                if pos_vide != ligne:
                    grille[ligne][colonne] = -1
                pos_vide -= 1

def populer_cases_vides(grille, nb_types) :
    """
    Génère aléatoirement de nouveaux bonbons aux cases vides

    entrées :
        - grille (list[list[int]]) : la grille
        - nb_types (int) : nombre de différents types de bonbons
    """
    nb_lignes, nb_colonnes = len(grille), len(grille[0])
    for colonne in range(nb_colonnes) :
        for ligne in range(nb_lignes) :
            if grille[ligne][colonne] == -1:
                grille[ligne][colonne] = random.randint(0, nb_types - 1)


def max_de_grille(grille: list[list[int]]) -> int :
    """
    Retourne le maximum dans grille
    entrée :
        - grille (list[list[int]]) : la grille
    sortie :
        - maximum (int) : le maximum
    """
    maximum = 0
    for ligne in grille:
        for case in ligne:
            if case > maximum:
                maximum = case
    return maximum


def entree_utilisateur() -> tuple[int] :
    """
    Retourne l'entrée de l'utilisateur 

    sortie :
        - l1 (int) : ligne de la première case
        - c1 (int) : colonne de la première case
        - l2 (int) : ligne de la seconde case
        - c2 (int) : colonne de la seconde case
    """
    while True :
        try :
            (l1, c1) = map(int, input("Bonbon 1 (x y) : ").split())
            (l2, c2) = map(int, input("Bonbon 1 (x y) : ").split())
        except KeyboardInterrupt :
            print("Au revoir !")
            exit()
        except :
            print("Entrée non valide, veuillez réessayer")
            continue
        return l1, c1, l2, c2



def bonbon_beguin_terminal(nom_fichier: str, nb_iter: int):
    """
    Fonction principale pilotant les tours de jeu, les saisies et les cascades sur le terminal
    entrée :
        - nom_ficher (str) : nom du fichier à ouvrir
        - nb_iter (int) : nombre d'itérations à effectuer
    sortie :
        - None
    """
    grille = charger_grille(nom_fichier)
    
    # sécu (arrah):
    if not grille:
        print("Ah bah non en fait")
        return 


    case_debut_sel = (0, 0)
    case_fin_sel = (0, 0)
   

    #comme ça on peut s'adapter pour n'importe quel fichier csv
    nb_types = max_de_grille(grille) + 1

    
    for t in range(nb_iter):
        affichage_grille_terminal(grille)
        print("\n--- TOUR", t + 1, "/", nb_iter, "---")
        
        #commentaire qui sert pas mais juste pour dire que c'est propre putain je passe une aprem de merde
        l1, c1, l2, c2 = entree_utilisateur()
        
        echanger_bonbons(grille, l1, c1, l2, c2)
        
        #regarde s'il y a des alignements après l'échange
        alignements = detecter_alignements(grille)
        
        if len(alignements) > 0:
            #ça part en vrille (cascade)
            while len(alignements) > 0:
                for coord in alignements:
                    (ligne, colonne) = coord
                    grille[ligne][colonne] = -1
                
                # animation parce que bg stylé (à améliorer mais c'est chiant)
                affichage_grille_terminal(grille)
                
                faire_tomber_bonbons(grille)
                affichage_grille_terminal(grille)

                populer_cases_vides(grille, nb_types)
                affichage_grille_terminal(grille)
                alignements = detecter_alignements(grille)
        else:
            print("Coup inutile, T con !")
            echanger_bonbons(grille, l1, c1, l2, c2)

    plt.ioff()
    plt.show()


def echange_correct(l1, c1, l2, c2):
    """
    Vérifie si les entrées de l'utilisateur sont correctes et que l'échange peut être réalisé
    Entrées :
        - l1 (int) : ligne de la première case
        - c1 (int) : colonne de la première case
        - l2 (int) : ligne de la seconde case
        - c2 (int) : colonne de la seconde case
    Sortie :
        - booléen 
    """
    if l1-l2 == 0 and c1-c2 == 0 :
        return False
    return math.sqrt((l1-l2)**2+(c1-c2)**2) <= 1    


def supprimer_bonbons_alignes(grille: list[list[int]], alignements: set[tuple[int]]) :
    """
    Entrées :
        - grille (list[list[int]]) : la grille de jeu
        - alignements (set[tuple[int]]) : coordonnées des cases à supprimer
    """
    for coord in alignements:
        (ligne, colonne) = coord
        grille[ligne][colonne] = -1


def bonbon_beguin_matplotlib(nom_fichier: str, nb_tours: int):
    """
    Fonction principale pilotant les tours de jeu, les saisies et les cascades avec une interface matplotlib
    entrée :
        - nom_ficher (str) : nom du fichier à ouvrir
        - nb_iter (int) : nombre d'itérations à effectuer
    sortie :
        - None
    """

    # Audio pour les règles
    pygame.mixer.init()
    pygame.mixer.music.load("manumaregle1.mp3")
    pygame.mixer.music.play()

    grille = charger_grille(nom_fichier)
    points = 0
    tours_restants = nb_tours
    case_debut_sel = [0, 0]
    nb_types = max_de_grille(grille) + 1 # type de mines différentes dans le csv  

    plt.ion() # mode interactif pour l'affichage graphique sinon ça freeze et poof ça marche pas (la doc encore)

    def sur_presse_clique(event: MouseEvent) :
        nonlocal case_debut_sel
        case_debut_sel = (len(grille) - 1 - round(event.ydata), round(event.xdata))

    def sur_lachee_clique(event: MouseEvent) :
        nonlocal points, grille, tours_restants
        if event.inaxes is None :
            print("Dans la grille stp")
            return
        case_fin_sel = (len(grille) - 1 - round(event.ydata), round(event.xdata))

        if tours_restants == 0 :
            print("Plus de tours restants !")
            return

        if not echange_correct(case_debut_sel[0], case_debut_sel[1], case_fin_sel[0], case_fin_sel[1]) :
            print("Cet échange ne peut pas avoir lieu")
            return

        echanger_bonbons(grille, case_debut_sel[0], case_debut_sel[1], case_fin_sel[0], case_fin_sel[1])

        affichage_grille_matplotlib(grille, points, tours_restants)        
        alignements = detecter_alignements(grille) #regarde s'il y a des alignements après l'échange
        
        if len(alignements) == 0 :
            print("Coup inutile, ça ne sert à rien.")
            echanger_bonbons(grille, case_debut_sel[0], case_debut_sel[1], case_fin_sel[0], case_fin_sel[1])
            affichage_grille_matplotlib(grille, points, tours_restants)
            return

        tours_restants -= 1
        
        while len(alignements) > 0:
            points += len(alignements)

            supprimer_bonbons_alignes(grille, alignements)
            affichage_grille_matplotlib(grille, points, tours_restants)                
                
            faire_tomber_bonbons(grille)
            affichage_grille_matplotlib(grille, points, tours_restants)            

            populer_cases_vides(grille, nb_types)
            affichage_grille_matplotlib(grille, points, tours_restants)
                
            alignements = detecter_alignements(grille)
            


    fig = plt.gcf()
    fig.canvas.mpl_connect("button_press_event", sur_presse_clique)
    fig.canvas.mpl_connect("button_release_event", sur_lachee_clique)

    affichage_grille_matplotlib(grille, points, tours_restants)
        
    plt.ioff()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] in ["term", "terminal", "tui", "cli"] :
        bonbon_beguin_terminal("exemple_grille.csv", 10)
    else :
        bonbon_beguin_matplotlib("exemple_grille.csv", 10)
    
