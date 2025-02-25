#   |--------------------------------------------|   #
#   |--------Gestion de Budget (avec IHM)--------|   #
#   |--Groupe 2 (MOUSSA, ASSEMAT, JIN, ZAMOURI)--|   #
#   |--------------------------------------------|   #
# --Imports-- #
import datetime

# --Constantes-- #
CLE_CRYPTAGE = 23


# --Fonctions-- #
def import_idents(chemin_fichier: str, cle: int = CLE_CRYPTAGE) -> dict:
    """
    Importe le contenu du fichier ident.txt et renvoie une liste qui contient :
    l'identifiant, le mot de passe, le nom et la clé de cryptage du fichier de l'utilisateur.

    Args:
        chemin_fichier: le chemin relatif du fichier ident.txt
        cle: clé de cryptage du fichier (en dur)

    Returns:
        le dictionnaire des identifiants (et informations associées dans une liste)
    """
    # Ouverture du fichier et initialisation des variables nécessaires
    dict_ident = dict()
    with open(file=chemin_fichier, mode='r', encoding="utf-8") as idents:
        ligne = idents.readline()
        ligne = decryptage(ligne)
        while ligne != '':
            liste_intm = ligne.split('*')
            dict_ident[liste_intm[0]] = liste_intm[1:]
            dict_ident[liste_intm[0]][-1] = int(dict_ident[liste_intm[0]][-1])
            ligne = idents.readline()
            ligne = decryptage(ligne)
    return dict_ident


def import_comptes(chemin_fichier: str, cle: int = CLE_CRYPTAGE) -> list:
    """
    Importe le contenu relatif aux comptes du fichier id.txt et renvoie la liste des comptes.

    Args:
        chemin_fichier: le chemin relatif du fichier id.txt
        cle: clé de cryptage du fichier (en dur)

    Returns:
        la liste contenant les différents comptes de l'utilisateur
    """
    with open(file=chemin_fichier, mode='r', encoding="utf-8") as fichier:
        liste_comptes = []
        ligne = fichier.readline()
        ligne = decryptage(ligne)
        while ligne != '' and ligne[0] == 'C':
            liste_intm = ligne.strip('\n').split('*')
            liste_comptes.append(liste_intm[1])
            ligne = fichier.readline()
            ligne = decryptage(ligne)
    return liste_comptes


def import_operations(chemin_fichier: str, cle: int = CLE_CRYPTAGE) -> list:
    """
    Importe le contenu relatif aux opérations du fichier id.txt et renvoie une liste de tuples qui contient :
      - Une date (str),
      - Un libellé de l'opération (str),
      - Le compte concerné (str),
      - Le montant de l'opération (float),
      - Le mode de paiement (str),
      - Un booléen indiquant si l'opération est effective (bool),
      - Le budget concerné (str).

    Args:
        chemin_fichier: le chemin relatif du fichier id.txt
        cle: clé de cryptage du fichier (en dur)

    Returns:
        la liste des tuples contenant les différentes informations concernant chaque opération
    """
    with open(file=chemin_fichier, mode='r', encoding="utf-8") as fichier:
        liste_ope = []
        ligne = fichier.readline()
        ligne = decryptage(ligne)
        while ligne != '':
            if ligne[0] == 'O':
                liste_intm = ligne.strip('\n').split('*')
                liste_intm.pop(0)
                liste_intm[0] = datetime.date(year=int(liste_intm[0][6:]),
                                             month=int(liste_intm[0][3:5]),
                                             day=int(liste_intm[0][0:2]))
                liste_intm[3] = float(liste_intm[3])
                liste_intm[5] = bool(liste_intm[5])
                liste_ope.append(tuple(liste_intm))
            ligne = fichier.readline()
            ligne = decryptage(ligne)
    return liste_ope


def import_budgets(chemin_fichier: str, cle: int = CLE_CRYPTAGE) -> list:
    """
    Importe le contenu relatif aux budgets du fichier id.txt et renvoie une liste de listes qui contient :
      - La catégorie de dépenses (str),
      - Le montant alloué (float),
      - Le compte associé (str).

    Args:
        chemin_fichier: le chemin relatif du fichier id.txt
        cle: clé de cryptage du fichier (en dur)

    Returns:
        la liste des tuples contenant les différentes informations de chaque budget
    """
    with open(file=chemin_fichier, mode='r', encoding="utf-8") as fichier:
        liste_bud = []
        ligne = fichier.readline()
        ligne = decryptage(ligne)
        while ligne != '':
            if ligne[0] == 'B':
                liste_intm = ligne.strip('\n').split('*')
                liste_intm.pop(0)
                liste_intm[1] = float(liste_intm[1])
                liste_bud.append(liste_intm)
            ligne = fichier.readline()
            ligne = decryptage(ligne)
    return liste_bud


def cryptage(chaine: str, cle: int = CLE_CRYPTAGE) -> str:
    """
    Fonction, avec 2 options en paramètres, qui renvoie une chaîne de caractères cryptée
    avec la méthode César, selon la clé fournie.

    Args:
        chaine: texte à crypter
        cle: clé qui sera utilisée pour le cryptage

    Returns:
        la chaine cryptée
    """
    crypte = ''
    for char in chaine:
        if char == '\n' or char == '*':
            crypte += char
        else:
            crypte += chr(ord(char) + cle)
    return crypte


def decryptage(chaine: str, cle: int = CLE_CRYPTAGE) -> str:
    """
    Fonction, avec 2 options en paramètres, qui renvoie une chaîne de caractères décryptée
    avec la méthode César, selon la clé fournie.

    Args:
        chaine: texte à décrypter
        cle: clé qui sera utilisée pour le décryptage

    Returns:
        str: la chaine décryptée
    """
    decrypte = ''
    for char in chaine:
        if char == '\n' or char == '*':
            decrypte += char
        else:
            decrypte += chr(ord(char) - cle)
    return decrypte


def login(dictionnaire_id: dict) -> tuple[bool, str] | bool:
    """
    Permet à l'utilisateur de saisir ses identifiants de connexion et renvoie un tuple booléen-identifiant.

    Args:
        dictionnaire_id: Le fichier ident.txt qui joue le role de base de données

    Returns:
        un tuple avec True si l'identifiant et le mot de passe sont corrects ainsi que l'identifiant, False sinon.
    """
    nb_essais = 0
    trouve = False
    while not trouve:
        identifiant = input('Veuillez saisir votre identifiant : ')
        if len(identifiant) != 8:
            print('L\'identifiant doit faire 8 caractères.')
        elif identifiant not in dictionnaire_id.keys():
            print('Identifiant introuvable.')
        else:
            trouve = True

    while nb_essais < 5:
        mdp = input('Veuillez saisir votre mot de passe : ')
        if len(mdp) != 6:
            print('Le mot de passe doit faire 6 caractères.')
        elif mdp != dictionnaire_id[identifiant][0]:
            nb_essais += 1
            print(f"Mot de passe incorrect. Vous avez {5 - nb_essais} essais restants.")
        else:
            return True, identifiant

    return False


def calcul_solde(lst_op: list) -> float:
    """
    Calcule le solde d'un utilisateur grâce à la liste des opérations associées au compte.

    Args:
        lst_op: liste des opérations

    Returns:
        le montant présent sur le compte
    """
    solde = 0
    for i in range(len(lst_op)):
        solde += lst_op[i][3]
    return solde

def identification():
    """
    Fonction qui gère le comportement du logiciel, en fonction des entrées de l'utilisateur.

    Returns:

    """
    dict_ident = import_idents(chemin_fichier='./ident.txt')
    login_state = login(dictionnaire_id=dict_ident)
    identifiant = login_state[1]
    if login_state[0]:
        lst_cpt = import_comptes(chemin_fichier=f'../users/{identifiant}.txt')
        lst_op = import_operations(chemin_fichier=f'../users/{identifiant}.txt')
        lst_bud = import_budgets(chemin_fichier=f'../users/{identifiant}.txt')
        solde = calcul_solde(lst_op)
        print(lst_bud)

        print(f"\n|-----Tableau de bord-----|\n"
              f"| Bonjour {dict_ident[identifiant][1]} |\n"
              f"| Vous avez {solde}€ sur votre compte |")



# --Programme principal-- #
identification()
