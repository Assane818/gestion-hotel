from tabulate import tabulate
from const import *

def printProduct(chambres_dispo:list) -> list:
    tab_chambre = []
    for chambre in chambres_dispo:
        tab_chambre.append(chambre.split(","))
    print(tabulate(tab_chambre,headers=titre,tablefmt="rounded_grid"))

def printCommend(commend:list) -> list:
    tab_commend = []
    for chambre in commend:
        tab_commend.append(chambre)
    print(tabulate(tab_commend,headers=titreCommed,tablefmt="rounded_grid"))