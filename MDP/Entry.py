class Entry:

    """Une entrée possedant un couple username/password lié à un service (une app ou site)"""

    __password: str
    __username: str
    __service: str
    __all: list = []

    def __init__(self, password: str, username: str, service: str) -> None:
        self.__password = password
        self.__username = username
        self.__service = service
        Entry.__all.append(self)

    @property
    def password(self) -> str:
        return self.__password

    @property
    def username(self) -> str:
        return self.__username

    @property
    def service(self) -> str:
        return self.__service

    @password.setter
    def password(self, password: str) -> None:
        self.__password = password

    @username.setter
    def username(self, username: str) -> None:
        self.__username = username

    @service.setter
    def service(self, service: str) -> None:
        self.__service = service

    @staticmethod
    def all() -> list:
        """Représente une liste de toutes les entrées"""
        return Entry.__all

    @staticmethod
    def get_from_service(proposition: str) -> list:
        """Renvoie une liste des entrées filtrée par le service mis en paramètre"""
        entries_by_service: list[Entry] = []
        for i in Entry.__all:
            if i.service.lower() == proposition.lower():
                entries_by_service.append(i)

        return entries_by_service

    @staticmethod
    def get_from_username(proposition: str) -> list:
        """Renvoie une liste des entrées filtrée par un username mis en paramètre"""
        entries_by_username: list[Entry] = []
        for i in Entry.__all:
            if i.username.lower() == proposition.lower():
                entries_by_username.append(i)

        return entries_by_username

    @staticmethod
    def get_from_password(proposition: str) -> list:
        """Renvoie une liste des entrées filtrée par le password mis en paramètre"""
        entries_by_password: list[Entry] = []
        for i in Entry.__all:
            if i.password.lower() == proposition.lower():
                entries_by_password.append(i)

        return entries_by_password

    def __str__(self):
        return f"{self.username} : {self.password} -> {self.service}"

