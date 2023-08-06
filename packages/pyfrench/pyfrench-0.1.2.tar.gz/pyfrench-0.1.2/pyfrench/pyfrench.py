from os import *

# Console
def couleur(rouge: int, vert: int, bleu: int, texte: str):
    return "\033[38;2;{};{};{}m{}".format(rouge, vert, bleu, texte)
def txt(nombre: str):
    return int(nombre)
def num(nombre: int):
    return str(nombre)
def afficher(texte: str):
    return print(texte + couleur(203, 203, 203, ''))
def demander(question: str):
    return input('{}\n'.format(question) + couleur(203, 203, 203, ''))
def erreur(erreur: str):
    return print(couleur(255, 0, 0, 'ERREUR: {}'.format(erreur)) + couleur(203, 203, 203, ''))
def attention(texte: str):
    return print(couleur(235, 192, 52, 'ATTENTION: {}'.format(texte)) + couleur(203, 203, 203, ''))
def succes(texte: str):
    return print(couleur(45, 166, 49, 'SUCCÈS: {}'.format(texte)) + couleur(203, 203, 203, ''))
def maths(calcul: str):
    return print(int(eval(calcul)))
def cls():
    if name == "nt":
        system("cls")
    else:
        system("clear")

# Fichier
def ouvrir(fichier: str):
    return open(file=fichier)

# Vrai/Faux
def Vrai():
    return True
def Faux():
    return False