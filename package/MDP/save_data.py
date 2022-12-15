import json
from package.MDP.entry import Entry


def save():
    print("Début de la sauvegarde ...")
    json_list: list[dict[str: str]] = []
    for entry in Entry.all():
        json_list.append(entry.to_dict())
    try:
        with open("save.json", "w") as file:
            file.write(json.dumps(json_list))
            print("Sauvegarde terminée !")

    except IOError:
        print("Erreur de sauvegarde ...")


def load():
    l: list[Entry] = []
    try:
        with open("save.json", "r") as file:
            j_file: list = json.load(file)
            for i in j_file:
                l.append(Entry.from_dict(i))

        Entry.set_all(l)
    except FileNotFoundError:
        print("Fichier introuvable ...")
    except IOError:
        print("Erreur interne, veuillez réessayer plus tard ...")
