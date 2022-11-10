from MDP.Entry import Entry
import MDP.Menu as Menu
import MDP.SaveData as Save


def add_username() -> str:
    return input("Veuillez entrer le username :")


def add_password() -> str:
    return input("Veuillez entrer un mot de passe :")


def add_service() -> str:
    return input("Veuillez entrer le service :")


def add_entry() -> None:
    entry: Entry = Entry(
        add_password(),
        add_username(),
        add_service()
    )
    print(f"L'entrée suivante vient d'être ajoutée :\n\t{entry}")
    if again():
        add_entry()
    else:
        Menu.accueil()


def select_entry(param) -> Entry | None:
    entries: list[Entry] = []
    value: str = ""
    if param == 1:
        value = input("Veuillez indiquer le service à sélectionner ")
        entries = Entry.get_from_service(value)
    elif param == 2:
        value = input("Veuillez indiquer le username à sélectionner ")
        entries = Entry.get_from_username(value)
    elif param == 3:
        value = input("Veuillez indiquer le password à sélectionner ")
        entries = Entry.get_from_password(value)

    if len(entries) == 0:
        return None
    if len(entries) == 1:
        print(f"Une seule entrée possède cette valeur: \"{entries[0]}\", elle a donc été automatiquement sélectionnée.")
        return entries[0]

    message_choice: str = f"Veuillez sélectionner l'entrée [1 - {len(entries)}] :\n"
    message: str = ""
    for i in range(0, len(entries)):
        message += f"{i + 1}. {entries[i]}\n"

    print(message)

    choice: int = int(input(message_choice))
    while choice > len(entries) or choice < 1:
        print("Entrée hors d'atteinte ...")
        choice = int(input(message_choice))
    print(f"Vous avez choisi l\'entrée:\n {entries[choice - 1]}")
    return entries[choice - 1]


def remove_entry(entry: Entry):
    if again(message="Êtes-vous sûr de vouloir supprimer cette entrée ? [y/n]"):
        Entry.all().remove(entry)
        print(f"L'entrée suivante \"{entry}\" a été supprimée")
        return
    Menu.accueil()


def modify_entry(entry: Entry) -> None:
    print(f"Quelle donnée de l'entrée \"{entry}\" voulez-vous modifier ?")
    print("\t1. Le service")
    print("\t2. Le username")
    print("\t3. Le mot de passe")
    choice: int = int(input(""))
    if choice == 1:
        value: str = input("Donnez le nouveau nom de service :")
        if again(f"Voulez-vous remplacer le service \"{entry.service}\" par \"{value}\" [y/n]"):
            entry.service = value
    elif choice == 2:
        value: str = input("Donnez le nouveau username :")
        if again(f"Voulez-vous remplacer le username \"{entry.username}\" par {value} [y/n]"):
            entry.username = value
    elif choice == 3:
        value: str = input("Donnez le nouveau mot de passe :")
        if again(f"Voulez-vous remplacer le mot de passe \"{entry.password}\" par \"{value}\" [y/n]"):
            entry.password = value
    else:
        print("Entrée invalide ...")
        modify_entry(entry)

    if again():
        modify_entry(entry)
    Menu.accueil()


def close():
    if again(message="Voulez vous sauvegarder ? [y/n]"):
        Save.save()
    exit(0)


def again(message="Voulez-vous continuer ? [y/n]\n\n") -> bool:
    choice: str = ""
    while choice != "y" and choice != "n":
        choice = input(message).lower()

    return choice == "y"



