from pyfrench.pyfrench import *

def test_pyfrench():
    cls()

    afficher('Salut')
    afficher(couleur(70, 45, 85, 'Salut'))

    erreur('Salut')
    attention('Salut')
    succes('Salut')

    maths("2-2*2+2/2")