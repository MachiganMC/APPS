from package.MDP.data import Data
import package.MDP.functionalities as fct


def accueil():
    print("Bienvenue dans votre gestionnaire de mot de passe !\nVoici la liste des entrées:\n")
    entries: list[Data] = Data.all()
    if len(entries) > 0:
        for i in range(0, len(entries)):
            print(f"\t{i + 1}) {entries[i]}")
    else:
        print("Il n'y pas encore d'entrées dans le gestionnaire ...")

    print("")
    print("Veuillez choisir ce que vous voulez faire :")
    print("\t0. Fermer l'application")
    print("\t1. Ajouter une entrée")
    if len(entries) > 0:
        print("\t2. Filtrer les entrée")

    choice: int = int(input(""))
    if choice == 0:
        fct.close()
    if choice == 1:
        fct.add_entry()
    if choice == 2 and len(Data.all()) > 0:
        print("Sélectionner le champ sur lequel vous voulez filtrer :")
        print("\t1. Le service")
        print("\t2. Le username")
        print("\t3. Le mot de passe")
        choice_attribute: int = int(input(""))
        entry: Data = fct.select_entry(choice_attribute)
        if entry is None:
            print("Aucune entrée n'a été trouvée ...\n")
            accueil()
            return
        print(f"Que voulez vous faire ?")
        print("\t1. Le modifier")
        print("\t2. Le supprimer")
        choice: int = int(input(""))
        if choice == 1:
            fct.modify_entry(entry)
        elif choice == 2:
            fct.remove_entry(entry)
        else:
            print("Aucun choix trouvé ...")
        accueil()

    else:
        print("Entrée erronée ...\nVeuillez choisir une commande disponible\n")
        accueil()
