from __future__ import annotations

import os

import cryptocode

from package.MDP.Question import Question
import hashlib
import json

from package.MDP.Entry import Entry


class Profil:
    __login: str
    __password_hash: str
    __answer_hash: str
    __question_index: int
    __entries: list[Entry]

    def __init__(self) -> None:
        pass

    @classmethod
    def new_profil(cls, login: str, password: str, question: Question) -> Profil:
        self = Profil()
        self.__login = login
        self.__question_index = question.index
        self.__password_hash = hashlib.md5(password.encode()).hexdigest()
        self.__answer_hash = hashlib.md5(question.answer.encode()).hexdigest()
        self.__entries = []
        return self

    @classmethod
    def get_from_dict(cls, j_data: dict) -> Profil:
        self = Profil()
        self.__login = j_data["login"]
        self.__question_index = j_data["question_index"]
        self.__entries = j_data["entries"]
        return self

    def encrypt(self) -> (str, str):
        data_dict: dict = {
            "login": self.__login,
            "entries": self.__entries,
            "question_index": self.__question_index
        }
        json_data: str = json.dumps(data_dict, ensure_ascii=False).__str__()
        crypt_pw: str = cryptocode.encrypt(json_data, self.__password_hash)
        crypt_question: str = cryptocode.encrypt(json_data, self.__answer_hash)
        return crypt_pw, crypt_question

    def save(self) -> None:
        with open(f"data/{self.__login}.alz", "w") as j_file:
            crypt: tuple[str, str] = self.encrypt()
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
            print(Question.all_questions[j_file[2]])
            try:
                decrypt: str | bool = cryptocode.decrypt(j_file[1], hashlib.md5(answer.encode()).hexdigest())
                if not decrypt:
                    raise ValueError("Invalid answer")
                j_data: dict = json.loads(decrypt)
            except TypeError:
                raise ValueError("Invalid answer")
            return Profil.get_from_dict(j_data)

    @property
    def login(self) -> str:
        return self.__login

    @property
    def password_hash(self) -> str:
        return self.__password_hash

    @property
    def answer_hash(self) -> str:
        return self.__answer_hash