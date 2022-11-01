from MDP.Entry import Entry
import MDP.Fonctionalities as fct


def accueil():
    print("Bienvenue dans votre gestionnaire de mot de passe :")
    entries: list[Entry] = Entry.all()
    if len(entries) > 0:
        for i in range(0, len(entries)):
            print(f"\t{i + 1}) {entries[i]}")
    else:
        print("Il n'y pas encore d'entrées dans le gestionnaire ...")

    print("")
    print("Veuillez choisir ce que vous voulez faire :")
    print("\t1. Ajouter une entrée")
    if len(entries) > 0:
        print("\t2. Filtrer les entrée")

    choice: int = int(input(""))
    if choice == 1:
        fct.add_entry()
    if choice == 2:
        entry: Entry = fct.select_entry()
        if entry is None:
            print("Aucune entrée n'a été trouvée ...")
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




