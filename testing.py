import unittest
from unittest.mock import mock_open, patch
from bonbon_beguin import (
    echanger_bonbons, 
    detecter_alignements, 
    faire_tomber_bonbons, 
    echange_correct,
    charger_grille,
    max_de_grille,
    populer_cases_vides,
    supprimer_bonbons_alignes,
    chunk_meme_couleur
)

class TestBonbonBeguin(unittest.TestCase):

    def setUp(self):
        """Initialisation de grilles types pour les tests."""
        self.grille_simple = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8]
        ]

    ## --- Tests sur l'échange ---
    
    def test_echanger_bonbons(self):
        """Vérifie que deux cases sont bien interverties."""
        grille = [[1, 2], [3, 4]]
        echanger_bonbons(grille, 0, 0, 1, 1) # Échange (0,0) et (1,1)
        self.assertEqual(grille[0][0], 4)
        self.assertEqual(grille[1][1], 1)

    def test_echange_correct_valide(self):
        """Vérifie la détection de proximité pour l'échange."""
        # Adjacents
        self.assertTrue(echange_correct(0, 0, 0, 1))
        # Adjacents
        self.assertTrue(echange_correct(4, 1, 4, 0))
        # Trop loin
        self.assertFalse(echange_correct(0, 0, 0, 2))
        # Même case
        self.assertFalse(echange_correct(1, 1, 1, 1))

    ## --- Tests sur la détection d'alignements ---

    def test_detecter_alignements_horizontal(self):
        """Vérifie la détection de 3 bonbons identiques en ligne."""
        grille = [
            [0, 0, 0, 1],
            [2, 3, 4, 5]
        ]
        alignements = detecter_alignements(grille)
        # On attend les coordonnées (0,0), (0,1), (0,2)
        self.assertIn((0, 0), alignements)
        self.assertIn((0, 1), alignements)
        self.assertIn((0, 2), alignements)
        self.assertEqual(len(alignements), 3)

    def test_detecter_alignements_vertical(self):
        """Vérifie la détection de 3 bonbons identiques en colonne."""
        grille = [
            [0, 5],
            [0, 6],
            [0, 7]
        ]
        alignements = detecter_alignements(grille)
        self.assertEqual(len(alignements), 3)
        self.assertTrue(all(coord[1] == 0 for coord in alignements))

    ## --- Tests sur la gravité (La physique selon Newton/Gabriel) ---

    def test_faire_tomber_bonbons(self):
        """Vérifie que les bonbons tombent pour combler les trous (-1)."""
        # Grille avec des trous (-1)
        # 1 . 2
        # . . .
        # 3 4 5
        grille = [
            [1, -1, 2],
            [-1, -1, -1],
            [3, 4, 5]
        ]
        faire_tomber_bonbons(grille)
        
        # Après chute, la ligne du bas doit être pleine, 
        # et les éléments du haut doivent avoir glissé vers le bas.
        # Colonne 0 : le '1' doit être en ligne 1 (au-dessus du 3)
        self.assertEqual(grille[2][0], 3)
        self.assertEqual(grille[1][0], 1)
        self.assertEqual(grille[0][0], -1)
        
        # Colonne 2 : le '2' doit être en ligne 1 (au-dessus du 5)
        self.assertEqual(grille[2][2], 5)
        self.assertEqual(grille[1][2], 2)

    ## --- Test de robustesse ---

    def test_alignement_complexe(self):
        """Test un alignement en L (horizontal + vertical simultané)."""
        grille = [
            [1, 2, 3],
            [1, 5, 6],
            [1, 1, 1]
        ]
        # Ici le '1' forme un L. chunk_meme_couleur devrait tout prendre.
        alignements = detecter_alignements(grille)
        # Il y a 5 cases contenant des '1' connectés
        self.assertEqual(len(alignements), 5)


    ## --- Tests sur le chargement et les données ---

    def test_charger_grille_valide(self):
        """Vérifie que le parseur transforme bien le texte en liste d'entiers."""
        # Simulation d'un fichier CSV avec des espaces (ton split() utilise l'espace par défaut)
        contenu_simule = "0 1 2\n3 4 5\n"
        with patch("builtins.open", mock_open(read_data=contenu_simule)):
            grille = charger_grille("test.csv")
            self.assertEqual(grille, [[0, 1, 2], [3, 4, 5]])
            self.assertIsInstance(grille[0][0], int)

    def test_max_de_grille(self):
        """Vérifie que l'on trouve bien l'ID de bonbon le plus élevé."""
        grille = [[0, 1], [5, 2]]
        self.assertEqual(max_de_grille(grille), 5)
        # Test avec grille vide ou zéros
        self.assertEqual(max_de_grille([[0, 0]]), 0)

    ## --- Tests sur la modification de la grille ---

    def test_supprimer_bonbons_alignes(self):
        """Vérifie que les coordonnées fournies passent bien à -1."""
        grille = [[1, 1, 1], [2, 2, 2]]
        alignements = {(0, 0), (0, 1), (0, 2)}
        supprimer_bonbons_alignes(grille, alignements)
        
        self.assertEqual(grille[0], [-1, -1, -1]) # Ligne 0 vidée
        self.assertEqual(grille[1], [2, 2, 2])    # Ligne 1 intacte

    def test_populer_cases_vides(self):
        """Vérifie que les cases -1 sont remplacées par des entiers valides."""
        # Grille totalement vide
        grille = [[-1, -1], [-1, -1]]
        nb_types = 3 # Bonbons de 0 à 2
        populer_cases_vides(grille, nb_types)
        
        for ligne in grille:
            for case in ligne:
                self.assertGreaterEqual(case, 0)
                self.assertLess(case, nb_types)
                self.assertNotEqual(case, -1)

    ## --- Test de logique combinée (Le "Cascade") ---

    def test_cascade_logique_simple(self):
        """
        Simule une séquence : suppression -> chute.
        C'est le cœur du gameplay.
        """
        # Grille de départ : le '2' est au sommet d'une colonne qui va disparaître
        grille = [
            [2, 0, 0],
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0]
        ]
        # 1. Détection des '1' verticaux
        alignements = {(1, 0), (2, 0), (3, 0)}
        supprimer_bonbons_alignes(grille, alignements)
        
        # 2. Chute
        faire_tomber_bonbons(grille)
        
        # Le '2' qui était en (0,0) doit maintenant être tout en bas en (3,0)
        self.assertEqual(grille[3][0], 2)
        # Les cases au-dessus doivent être vides (-1)
        self.assertEqual(grille[0][0], -1)
        self.assertEqual(grille[1][0], -1)

    def test_alignement_en_T(self):
        """
        Vérifie qu'un alignement en forme de T est entièrement détecté.
        Le '1' est présent en ligne et en colonne se croisant.
        """
        # Grille :
        # 1 1 1
        # 0 1 0
        # 0 1 0
        grille = [
            [1, 1, 1],
            [0, 1, 0],
            [0, 1, 0]
        ]
        alignements = detecter_alignements(grille)
        
        # Le T contient 5 bonbons de type '1'
        self.assertEqual(len(alignements), 5)
        self.assertIn((0, 1), alignements) # Le centre du T
        self.assertIn((2, 1), alignements) # Le pied du T

    def test_double_alignement_parallele(self):
        """Vérifie que deux lignes de 3 identiques sont détectées simultanément."""
        grille = [
            [1, 1, 1],
            [0, 2, 0],
            [3, 3, 3]
        ]
        alignements = detecter_alignements(grille)
        self.assertEqual(len(alignements), 6)

    def test_gravite_complexe_colonnes_vides(self):
        """
        Teste la chute quand une colonne est presque vide et l'autre pleine.
        Vérifie que les bonbons ne "sautent" pas d'une colonne à l'autre.
        """
        # . 2 .
        # . . .
        # 1 . 3
        grille = [
            [-1,  2, -1],
            [-1, -1, -1],
            [ 1, -1,  3]
        ]
        faire_tomber_bonbons(grille)
        
        # Colonne 1 : le 2 doit être tombé tout en bas (ligne 2)
        self.assertEqual(grille[2][1], 2)
        self.assertEqual(grille[0][1], -1)
        # Colonne 0 et 2 : les bonbons 1 et 3 ne bougent pas (déjà en bas)
        self.assertEqual(grille[2][0], 1)
        self.assertEqual(grille[2][2], 3)

    def test_echange_interdit_trop_loin(self):
        """Vérifie que le jeu refuse un échange à plus d'une case de distance."""
        # Test saut de cheval ou grand écart
        self.assertFalse(echange_correct(0, 0, 2, 0))
        self.assertFalse(echange_correct(0, 0, 2, 2))

    def test_coherence_chunk_recursion(self):
        """Vérifie que chunk_meme_couleur ne boucle pas à l'infini sur un gros bloc."""
        # Un carré 3x3 de même couleur
        grille = [[1]*3 for _ in range(3)]
        chunk = chunk_meme_couleur(grille, (1, 1))
        
        # Doit trouver les 9 cases
        self.assertEqual(len(chunk), 9)

    def test_alignement_long(self):
        """Vérifie qu'une ligne de 5 bonbons est bien traitée comme un seul bloc."""
        grille = [[2, 2, 2, 2, 2]]
        alignements = detecter_alignements(grille)
        self.assertEqual(len(alignements), 5)

if __name__ == '__main__':
    unittest.main()
