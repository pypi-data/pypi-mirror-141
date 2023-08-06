def test_pyfrench():
    afficher('Salut')
    afficher(couleur(70, 45, 85, 'Salut'))

    erreur('Salut')
    attention('Salut')
    succes('Salut')

    maths("2-2*2+2/2")

from pyfrench import afficher, erreur, attention, succes, maths, couleur