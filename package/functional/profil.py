from __future__ import annotations

import os

import cryptocode

from package.functional.question import Question
import hashlib
import json

from package.functional.data import Data


class Profil:
    __name: str
    __question_index: int
    __entries: list[Data]

    def __init__(self) -> None:
        pass

    @classmethod
    def new_profil(cls, name: str, question: Question) -> Profil:
        """
        Auteur : Simon Maes
        Dernière modification : 19 décembre 2022
        Permet d'instancier un nouvel objet Profil.
        PRE :
            - login : ne doit pas être une chaîne de caractère vide et ne doit pas être déjà
            présent dans Profil#all_profil_str()
            - question : ne doit pas être None

        POST :
            - Instancie un nouvel objet Profil
            - Lance une ValueError si les préconditions ne sont pas respectées.
        """
        if name is None or name == "":
            raise ValueError("Nom de profil invalide")
        if name in Profil.all_profil_str():
            raise ValueError(f"Le nom de profil {name} existe déjà")
        self = Profil()
        self.__name = name
        self.__question_index = question.index
        self.__entries = []
        return self

    @classmethod
    def get_from_dict(cls, j_data: dict) -> Profil:
        """
        Auteur : Simon Maes
        Dernière modification : 19 décembre 2022
        Permet d'instancier un nouvel objet Profil sur base d'un dictionnaire précis.
        PRE :
            - Le dictionnaire doit contenir les clés suivantes :
                - name,
                - question_index,
                - entries
                
        POST : 
            - Retourne une nouvelle instance d'un objet Profil
            - Lance une IndexError, si les Préconditions ne sont pas respectées.
        """
        self = Profil()
        self.__name = j_data["name"]
        self.__question_index = j_data["question_index"]
        self.__entries = []
        for entry_dict in j_data["data"]:
            self.__entries.append(Data.from_dict(entry_dict))
        return self

    def encrypt(self, password_hash, answer_hash) -> (str, str):
        """
        Auteur : Antoine Moens Pennewaert
        Dernière modification : 19 décembre 2022

        → Crypte le fichier du profil en question en deux versions,
        l'une crypté avec le password hashé comme clé de cryptage,
        l'autre crypté avec la réponse hashée comme clé de cryptage.

        PRE :
            - password_hash et answer_ash ne doivent pas être vide.
        POST :
            - return crypt_pw, la chaine contenant le résultat du criptage graçe au password hashé.
            - return crypt_question, la chaine contenant le résultat du criptage
            graçe à la réponse à la question hashée.
            - Raise ValueError lorsque password_hash ou answer_hash sont vides.
        """
        if password_hash == "":
            raise ValueError("Mot de passe vide")
        if answer_hash == "":
            raise ValueError("Réponse à la question vide")

        entries: list[dict[str: str]] = []
        for entry in self.__entries:
            entries.append(entry.to_dict())

        data_dict: dict = {
            "name": self.__name,
            "data": entries,
            "question_index": self.__question_index
        }
        json_data: str = json.dumps(data_dict, ensure_ascii=False).__str__()
        crypt_pw: str = cryptocode.encrypt(json_data, password_hash)
        crypt_question: str = cryptocode.encrypt(json_data, answer_hash)
        return crypt_pw, crypt_question

    def save(self, password_hash, answer_hash) -> None:
        """
        Auteur : Corentin Koninckx
        Dernière modification : 19 décembre 2022
        
        Permet de créer/remplacer un fichier json portant le nom du login et d'extension ".alz"
        création d'un tuple ayant comme éléments :
            - profil crypté avec password_hash et profil crypté avec answer_hash
        dans le fichier json, on injecte une liste ayant comme éléments :
            - le contenu du tuple (password_hash et answer_hash) et question_index

        PRE :
            - password_hash doit être défini
            - answer_hash doit être défini
        POST :
            - création/remplacement d'un fichier json "login.alz"
            - Ne s'occupe pas de gérer les IOErrors
        """
        with open(f"data/{self.__name}.alz", "w") as j_file:
            crypt: tuple[str, str] = self.encrypt(password_hash, answer_hash)
            j_file.write(json.dumps([crypt[0], crypt[1], self.__question_index]))

    @classmethod
    def all_profil_str(cls) -> list[str]:
        """
        Auteur : Corentin Koninckx
        Dernière modification : 19 décembre 2022

        Permet de récupérer une liste de tous les noms de profil, la fonction boucle dans tous les fichiers contenus
        dans la directory et regroupe ceux ayant comme extension ".alz" (fichiers de profil), découpe le nom des
        fichiers pour enlever leur extension et les injecte dans une liste all_profil qui sera retournée

        PRE :
            - pas de prérequis
        POST :
            - retourne une liste ayant comme éléments les noms de profil
        """
        all_profil: list[str] = []
        try:
            for file in os.listdir(path=f"{os.getcwd()}\\data"):
                if file.endswith(".alz"):
                    all_profil.append(file.split(".alz")[0])
        except FileNotFoundError:
            pass
        return all_profil

    @classmethod
    def get_from_password(cls, name_profil: str, pw: str) -> Profil:
        """
        Auteur : Antoine Moens Pennewaert
        Dernière modification : 19 décembre 2022

        → Va décrypter la partie du fichier du profil crypter avec le password hashé et

        PRE :
            - le profil a dû avoir déjà crypté son fichier.
        POST :
            - return Profil.get_from_dict(j_data), une redéfinition du profil avec les données décryptée utilisable pour
            la suite du code.
            - Raise ValueError si le password donner n'a pas permis de correctement décrypter ou que le profil
            renseigner est inexistant.
        """
        try:
            with open(f"data/{name_profil}.alz", "r") as file:
                j_file: json = json.load(file)
                try:
                    decrypt: str | bool = cryptocode.decrypt(j_file[0], hashlib.md5(pw.encode()).hexdigest())
                    if not decrypt:
                        raise ValueError("Invalid password")
                    j_data: dict = json.loads(decrypt)
                except TypeError:
                    raise ValueError("Invalid password")
                return Profil.get_from_dict(j_data)
        except FileNotFoundError:
            raise ValueError("Profil inexistant")

    @classmethod
    def get_from_question(cls, name_profil: str, answer: str) -> Profil:
        """
        Auteur : Corentin Koninckx
        Dernière modification : 19 décembre 2022

        Permet d'ouvrir en lecture un fichier "name_profil.alz", dans une variable decrypt sera contenu le profil crypté
        avec le answer_hash qui sera décrypté avec la clé de décryptage, si le décryptage ne se fait pas, decrypt
        vaudra false et provoquera une ValueError, si une TypeError survient alors cela provoquera aussi une ValueError.
        La fonction retournera le profil concerné

        PRE :
            - name_profil doit être défini
            - answer doit être défini
        POST :
            - renvoie un profil
            - renvoie ValueError si la réponse du profil crypté est invalide

        """
        with open(f"data/{name_profil}.alz", "r") as file:
            j_file: json = json.load(file)
            try:
                decrypt: str | bool = cryptocode.decrypt(j_file[1], hashlib.md5(answer.encode()).hexdigest())
                if not decrypt:
                    raise ValueError("Réponse invalide")
                j_data: dict = json.loads(decrypt)
            except TypeError:
                raise ValueError("Réponse invalide")
            return Profil.get_from_dict(j_data)


    @classmethod
    def get_question_from_str(cls, name_profile: str) -> str:
        """
        Auteur : Antoine Moens Pennewaert
        Dernière modification : 19 décembre 2022
        
        → Permet de trouver la question de récupération choisie du profil

        PRE :
            - le profil doit avoir choisi une question de récupération.
        POST :
            - return Question.all_questions[j_file[2]], l'index de la question dans la liste des questions de
            récupération disponible.
            - Raise ValueError si le profil est inexistant.
        """
        try:
            with open(f"data/{name_profile}.alz", "r") as file:
                j_file: json = json.load(file)
                return Question.all_questions[j_file[2]]
        except FileNotFoundError:
            raise ValueError(f"Profile {name_profile} inexistant")

    @property
    def name(self) -> str:
        return self.__name

    @property
    def entries(self) -> list[Data]:
        return self.__entries

    @property
    def question_index(self) -> int:
        return self.__question_index


def hash_str(to_hash: str) -> str:
    return hashlib.md5(to_hash.encode()).hexdigest()
