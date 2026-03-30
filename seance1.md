Bonbon Beguin

agougougaga

## problèmes:
1. affichage
2. descente et génération aléatoire de bonbons (miam)
3. detection de trois ou plus
4. mangeage des bonbons
5. input user
6. permutation
7. lecture du fichier csv pour la première grille
8. detection mouvement possible





règles:
1. affiche la première grille
jusqu'à permutation plus possible:
2. demande 2 bonbons à permuter puis permutation
3. destruction des triplés jusqu'à plus de triplés

algorithme 




découpage fonctionnel:

fonction bonbon_beguin(fichier: str, nb_iter: int) :
    lis le fichier et le transcrit dans une grille 2D()
    # lance la boucle de jeu
    var nb_tours = 0
    afficher_grille()
    tant que nb_tours < nb_iter ET permutation pertinente possible :
        lire l'entrée de l'utilisateur()
        permutation()
        afficher grille()
        tant que trois ou plus alignés :
            reorganisation grille()
            afficher grille()
        


fonction lire l'entrée de l'utilisateur() :
    format "x, y"
    split
    int()
    return

fonction permutation() :
    la preuve est laissée au lecteur.




fonction afficher_grille (grille):
    pour toute ligne dans grille
        pour toute case dans ligne
            affiche case

fonction reorganisation(grille):
    detecte les trous dans la grille et fais descendre les bonsbons dans les trous et génère ceux qui sont à la première ligne




fonction lire_csv(fichier csv):
    ouvre le fichier csv et créer une liste 2D à partir de cette chose étrange qu'est le coma separated values (miam)