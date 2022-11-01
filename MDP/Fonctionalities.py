from MDP.Entry import Entry
import MDP.Menu as Menu


def add_username() -> str:
    return input("Veuillez entrer l'username :")


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


def select_entry(param="service") -> Entry | None:
    entries: list[Entry] = []
    value: str = ""
    if param == "service":
        value = input("Veuillez indiquer le service à sélectionner")
        entries = Entry.get_from_service(value)
    elif param == "password":
        value = input("Veuillez indiquer le password à sélectionner")
        entries = Entry.get_from_password(value)
    elif param == "username":
        value = input("Veuillez indiquer le username à sélectionner")
        entries = Entry.get_from_username(value)

    if len(entries) == 0:
        return None
    if len(entries) == 1:
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
    Entry.all().remove(entry)
    print(f"L'entrée suivante \n\t{entry}\na été supprimée")


def modify_entry(entry: Entry) -> str:
    pass


def again(message="Voulez-vous continuer ? [y/n]") -> bool:
    while True:
        choice: str = input(message).lower()
        if choice == "y":
            return True
        if choice == "n":
            return False
