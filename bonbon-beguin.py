import random
import matplotlib.pyplot as plt


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
        - grille : (list[list[int]]) 
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
    

def affichage_grille_matplot(grille: list[list[int]]) :
    """
    Affiche la grille en utilisant matplotlib
    entrée :
        - grille : (list[list[int]]) 
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
    
    plt.title("Bonbon Beguin de Gabriel²", color='purple', pad=20)
    plt.pause(0.1)
    plt.draw()
    


def echanger_bonbons(grille: list[list[int]], l1: int, c1: int, l2: int, c2: int):
    """
    Intervertit les positions de deux bonbons ciblés dans la grille.
    entrée : 
        - grille : (list[list[int]]) 
        - l1 : int
        - c1 : int
        - l2 : int
        - c2 : int
    """
    grille[l1][c1], grille[l2][c2] = grille[l2][c2], grille[l1][c1]


def detecter_alignements(grille: list[list[int]]): # decouverte des ensembles c'est une dinguerie
    """
    Détecte les alignements horizontaux et verticaux de 3 bonbons ou plus, en ligne ou en colonne.
    entrée :
        - grille : (list[list[int]]) 
    sortie :
        - a_supprimer : (set[tuple[int]])
    """
    a_supprimer = set()
    nb_lignes = len(grille)
    nb_colonnes = len(grille[0])

    # horizontal
    for l in range(nb_lignes):
        c = 0
        while c < nb_colonnes:
            valeur_actuelle = grille[l][c]
            if valeur_actuelle != -1:
                debut = c
                while c < nb_colonnes and grille[l][c] == valeur_actuelle:
                    c += 1
                longueur = c - debut
                if longueur >= 3:
                    for i in range(debut, c):
                        a_supprimer.add((l, i))
            else:
                c += 1

    # vertical
    for j in range(nb_colonnes):
        l = 0
        while l < nb_lignes:
            valeur_actuelle = grille[l][j]
            if valeur_actuelle != -1:
                debut = l
                while l < nb_lignes and grille[l][j] == valeur_actuelle:
                    l += 1
                
                longueur = l - debut
                if longueur >= 3:
                    for i in range(debut, l):
                        a_supprimer.add((i, j))
            else:
                l += 1

    return a_supprimer

def faire_tomber_bonbons(grille: list[list[int]]):
    """
    Fais descendre les bonbons.
    entrée : 
        - grille : (list[list[int]]) 
        - nb_types : int
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



def bonbon_beguin(nom_fichier: str, nb_iter: int):
    """
    Fonction principale pilotant les tours de jeu, les saisies et les cascades.
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

    plt.ion() #mode interactif pour l'affichage graphique sinon ça freeze et poof ça marche pas (la doc encore)
    

    #comme ça on peut s'adapter pour n'importe quel fichier csv
    nb_types = max_de_grille(grille) + 1
    
    for t in range(nb_iter):
        affichage_grille_terminal(grille)
        affichage_grille_matplot(grille)
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
                affichage_grille_matplot(grille)
                plt.pause(0.3)
                
                faire_tomber_bonbons(grille)
                affichage_grille_terminal(grille)
                affichage_grille_matplot(grille)
                plt.pause(0.3)

                populer_cases_vides(grille, nb_types)
                affichage_grille_terminal(grille)
                affichage_grille_matplot(grille)
                alignements = detecter_alignements(grille)
        else:
            print("Coup inutile, T con !")
            echanger_bonbons(grille, l1, c1, l2, c2)

    plt.ioff()
    plt.show()

if __name__ == "__main__":
    bonbon_beguin("exemple_grille.csv", 10)
    
