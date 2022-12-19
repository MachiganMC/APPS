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
    def new_profil(cls, login: str, password: str, question: Question) -> Profil:
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

    @classmethod
    def get_from_question(cls, name_profil: str, answer: str) -> Profil:
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
        try:
            with open(f"data/{name_profile}.alz", "r") as file:
                j_file: json = json.load(file)
                return Question.all_questions[j_file[2]]
        except FileNotFoundError:
            raise ValueError(f"Profile {name_profile} inexistant")

    @property
    def login(self) -> str:
        return self.__name

    @property
    def entries(self) -> list[Data]:
        return self.__entries


def hash_str(to_hash: str) -> str:
    return hashlib.md5(to_hash.encode()).hexdigest()

