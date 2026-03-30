
def parse_fichier(fichier: str) -> list[list[int]] :
    with open("exemple_grille.csv", "r") as fichier:
        contenu = fichier.read()
    
    """
    lignes_txt = contenu.split("\n")
    grille = []
    for ligne_txt in lignes_txt :
        cases_txt = ligne_txt.split()
        ligne_int = []
        for case_txt in cases_txt :
            ligne_int.append(int(case_txt))
        grille.append(ligne_int)
    return grille
    """

    return [[int(c) for c in l] for l in map(lambda l : l.split(), contenu.split("\n"))]


def permutation_pertinente_possible(grille: list[list[int]]) -> bool :
    ...
    
def detecte_suite_horiz(grille: list[list[int]]) -> tuple :
    """
    sortie : tuple (peut être None) [format : ((x, y), n)]
             (x, y) : coo du début du triple
             n : nombre

    """
    for (y, ligne) in enumerate(grille) :
        dernier = None
        affilee = 0
        for (x, case) in enumerate(ligne) :
            ...
    

def lire_entree_utilisateur() -> tuple[int] :
    p1 = input("point1? (x1 y1, connard)")
    p2 = input("point2? (x2 y2, connard)")
    p1 = p1.split()
    p2 = p2.split()
    p1_1 = [int(p1[0]), int(p1[1])]
    p2_1 = [int(p2[0]), int(p2[1])]
    return p1_1, p2_1

def afficher_grille_terminal(grille: list[list[int]]) :
    header = "  "
    for i in range(0, len(grille[0])) :
        header += f"{i} "
    print(header)

    for (i, ligne) in enumerate(grille) :
        ligne_txt = f"{i} "
        for case in ligne :
            ligne_txt += f"{case} "
        print(ligne_txt)




def bonbon_beguin(fichier: str, nb_iter: int) :
    grille = parse_fichier(fichier)
    nb_iter_real = 0
    afficher_grille_terminal(grille)
    while nb_iter_real <= nb_iter and permutation_pertinente_possible(grille) :
        ...


if __name__ == "__main__" :
    bonbon_beguin("exemple_grille.csv", -1)








