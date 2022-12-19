from __future__ import annotations


class Data:
    """Une entrée possédant un couple username/password lié à un service (une app ou site)"""

    __password: str
    __username: str
    __service: str
    __comment: str

    def __init__(self, username: str, password: str, service: str, comment="") -> None:
        """
        Auteur : Simon Maes
        Dernière modification : 19 décembre 2022
        PRE :
            - username ne doit pas être un string vide
            - service ne doit pas être un string vide
            - password ne doit pas être un string vide
        POST :
            - Un objet data est instancié
            - Lance une ValueError est lancée en cas de non-respects des Préconditions
        """
        if username == "" or username is None:
            raise ValueError("L'username ne peut pas être vide")
        self.__username = username

        if password == "" or password is None:
            raise ValueError("Le password ne peut pas être vide")
        self.__password = password

        if service == "" or service is None:
            raise ValueError("Le service ne peut pas être vide")
        self.__service = service

        self.__comment = comment

    def to_dict(self) -> dict[str: str]:
        return {
            "username": self.__username,
            "password": self.__password,
            "service": self.__service,
            "comment": self.__comment
        }

    @staticmethod
    def from_dict(data_dict: dict[str: str]) -> Data:
        """
        Auteur : Simon Maes
        Dernière modification : 19 décembre 2022
        Permet d'instancier un nouvel objet Data sur base d'un dictionnaire précis.
        PRE :
            - Le dictionnaire doit contenir les clés suivantes :
                - username
                - password
                - service
                - comment

        POST :
            - Instancie un nouvel objet Data avec comme informations les éléments du dictionnaire
            - Lance une KeyError si les préconditions ne sont pas respectées.
        """

        return Data(
            data_dict["username"],
            data_dict["password"],
            data_dict["service"],
            data_dict["comment"]
        )

    @property
    def password(self) -> str:
        return self.__password

    @property
    def username(self) -> str:
        return self.__username

    @property
    def service(self) -> str:
        return self.__service

    @property
    def comment(self) -> str:
        return self.__comment

    @password.setter
    def password(self, password: str) -> None:
        self.__password = password

    @username.setter
    def username(self, username: str) -> None:
        self.__username = username

    @service.setter
    def service(self, service: str) -> None:
        self.__service = service

    def __str__(self):
        return f"Username: {self.username} | MDP: {self.password} | Service: {self.service}"
