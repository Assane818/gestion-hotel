from const import *
from fonctions import *
from views import *
while True:
    rep = "OUI"
    commend = []
    all_chambre = getFileContent(CHAMBRE_F)
    chambre_dispo = getAvailable(all_chambre)
    printProduct(chambre_dispo)
    getMyCommande(commend,chambre_dispo)
    #menu
    choix = inputChoix("123")
    if choix == "1":
        valideCommend(COMMEND_F,commend,all_chambre,CHAMBRE_F,VENTE_F)
        print("Votre commande a ete valider!")
    elif choix == "2":
        printCommend(commend)
        choix_delete = inputDeleteChoix()
        deleteChambreInCommand(choix_delete,commend)
        printCommend(commend)
        valideCommend(COMMEND_F,commend,all_chambre,CHAMBRE_F,VENTE_F)
    else:
        if choix == "3":
            deleteCommand(commend)
        else:
            break