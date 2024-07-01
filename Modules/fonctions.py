import os
from datetime import datetime,timedelta
from views import *
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors


def getFileContent(path:str):
    with open(path,"r") as f:
        return f.read().splitlines()
    
def getAvailable(chambres:list) -> list :
    list_chambre_dispo = []
    for chambre in chambres[1:]:
        if str(chambre.split(",")[4]) == "oui":
            list_chambre_dispo.append(chambre)
    return list_chambre_dispo

def getChambreByNumero(chambres:list,num_chambre:int) -> list|None:
    for chambre in chambres:
        if int(chambre.split(",")[0]) == num_chambre:
            return chambre.split(",")[:-1]
    return None

def getAllNumero(chambre_dispo:list) -> list:
    list_numeros = []
    for chambre in chambre_dispo:
        list_numeros.append(str(chambre.split(",")[0]))
    return list_numeros

def getChambreAlreadyChosen(chambre_dispo:list) -> list:
    list_numeros = []
    for chambre in chambre_dispo:
        list_numeros.append(str(chambre[0]))
    return list_numeros


def chooceChambreByNumero(chambre_dispo:list,commend:list) -> int:
    numero = ""
    while not (numero.isdigit() and (numero in getAllNumero(chambre_dispo) or numero == "0") and numero not in getChambreAlreadyChosen(commend)):
        printProduct(chambre_dispo)
        numero = input("Entrer le numero de la chambre:\n")
    return int(numero)

def getDateNow() -> str:
    date_now = datetime.now()
    return date_now.strftime("%d-%m-%Y")

def controlDateStayIsInt() -> int:
    sejour = input("Le nombre de jour que vous voulez sejourner dans notre hotel:\n")
    while not sejour.isdigit() or int(sejour) < 0:
        os.system("cls")
        sejour = input("Le nombre de jour que vous voulez sejourner dans notre hotel:\n")
    return int(sejour)

def getStay( sejour) -> str:
    date_now = datetime.strptime(getDateNow(), "%d-%m-%Y")
    date_sejour = date_now + timedelta(days = sejour)
    return date_sejour.strftime("%d-%m-%Y")

def inputDeleteChoix() -> int:
    numero = ""
    while not (numero.isdigit()):
        numero = input("Ecrire le nurero du chambre a supprime:\n")
    return int(numero)

def deleteChambreInCommand(num_chambre:int,commend:list):
    for chambre in commend:
        if int(chambre[0]) == num_chambre:
            commend.remove(chambre)
            print(f"La chambre numero {num_chambre} a ete supprime de vos commende\n")
            return
    print(f"La chambre numero {num_chambre} ne se trouve pas dans vos commende\n")

def deleteCommand(commend:list) -> list:
    commend = commend[:1]
    return commend

def header(titres:list,motif = "*",width = 100):
    print(motif*width)
    for titre in titres:
        print("{:^100}".format(titre))
    print(motif*width)

def getMyCommande(commend:list,chambre_dispo:list,somme:int = 0):
    while True:
        os.system("cls")
        header(entete)
        print("****Bienvenue dans notre hotel****")
        num_chambre = chooceChambreByNumero(chambre_dispo,commend)
        chambre_loue = getChambreByNumero(chambre_dispo,num_chambre)
        if not chambre_loue is None:
            nbr_jour = controlDateStayIsInt()
            date_depart = getStay( nbr_jour)
            payment = nbr_jour * int(chambre_loue[3])
            commend.append([num_chambre,chambre_loue[1],chambre_loue[2],chambre_loue[3],date_depart,payment])
            somme += payment
            print("Chambre ajouter a la commende")
            rep = input("Voulez vous commender une autre chambre [OUI/NON]:\n")
            if rep.upper() == "NON":
                return commend
            
def getNumeroCommend() -> str:
    return datetime.now().strftime("%d%m%y%H%M%S")

def saveCommend(file:str,data:list):
    with open(file,"a") as f:
        for item in data:
            str_item = [str(i) for i in item]
            f.write(",".join(str_item) + '\n')

def modifyFileChambres(file: str, numero: int, chambres: list) -> None:
    for i, chambre in enumerate(chambres[1:]):
        if int(chambre.split(",")[0]) == numero:
            chambres[i+1] = chambre.rsplit(",", 1)[0] + ",non"

    with open(file, "w") as f:
        for chambre in chambres:
            f.write(chambre + "\n")

def inputChoix(data: str) -> str:
    while True:
        print("Veullez choisir un numero")
        print("1 ---> Pour valider la commende")
        print("2 ---> Pour modifie et puis valider la commende")
        print("3 ---> Pour annuler la commende")
        choix = input("---> ")
        if choix not in data:
            continue
        else:
            return choix
        
def saveChambreLoue(vente_file:str,num_commend:str,commend:list):
    with open(vente_file,'a') as f:
        for item in commend:
            str_item = [str(i) for i in item]
            f.write(f"{num_commend},{','.join(str_item)}\n")

def generer_facture(num_commend:str,commend:list):
    somme = 0
    for item in commend:
        if item:
            somme += int(item[5])

    if somme != 0:
        with open(f"{num_commend}.txt", "w") as facture:
            for item in commend:
                if item:
                    item.pop(2)
                    str_item = [str(i) for i in item]
                    facture.write(f"{','.join(str_item)}\n")
                    somme_str = ["-", "-", "-", "Total", str(somme)]
            facture.write(f"{','.join(somme_str)}")

def getName() -> str:
    name = "0"
    while name.isdigit() or name == "0":
        name = input("ecrire votre nom et Prenom:\n")
    return name

def getAddress() ->str:
    address = ""
    while address == "":
        address = input("ecrire votre address:\n")
    return address
def valideCommend(file_commend:str,commend:list,chambres:list,file_chambre:str,vente_file: str):
    num_commend = getNumeroCommend()
    date_now = getDateNow()
    saveCommend(file_commend,commend)
    for chambre in commend:
        num = chambre[0]
        modifyFileChambres(file_chambre,num,chambres)
    saveChambreLoue(vente_file,num_commend,commend)
    generer_facture(num_commend,commend)
    data = getFileFacture(f"{num_commend}.txt")
    commender = getDataFacture(data)
    name = getName()
    address = getAddress()
    genererRecusPdf(num_commend, commender,name,date_now,address)


    
def getFileFacture(path):
    with open(path, "r") as f:
        data = f.read().splitlines()
        return data

def getDataFacture(data):
    return [chambre.split(",") for chambre in data]

def genererRecusPdf(num_command:str, data:list,name:str,datenow:str,address:str):
    pdf_filename = f"{num_command}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.drawString(20, 760, "SUPERFLY PALACE")
    c.drawString(20, 740, "Address: Corniche Ouest")
    c.drawString(20, 720, "Email: www.superfly.com")
    c.drawString(20, 700, "BP: 00000")
    c.drawString(470, 750, f"Date: {datenow}")
    c.drawString(470, 730, name)
    c.drawString(470, 710, address)

    # Données pour les en-têtes du tableau
    titreFacture = [["Numero", "Type", "Prix/nuit", "Date de depart", "Total"]]

    # Création du tableau pour les reçus
    table = Table(titreFacture + data, colWidths=[120, 60, 60, 60, 140])

    # Style du tableau
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.green),  # Couleur de fond pour la première ligne
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Couleur de texte pour la première ligne
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.green),  # Bordures
    ])

    table.setStyle(style)

    # Dessin du tableau sur le canvas
    table.wrapOn(c, 600, 400)
    table.drawOn(c, 50, 600)

    # Enregistrement du PDF et finalisation
    c.save()
    print(f"Reçus générés : {pdf_filename}")