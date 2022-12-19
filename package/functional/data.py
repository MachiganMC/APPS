from __future__ import annotations


class Data:
    """Une entrée possédant un couple username/password lié à un service (une app ou site)"""

    __password: str
    __username: str
    __service: str
    __comment: str

    def __init__(self, username: str, password: str, service: str, comment="") -> None:
        self.__username = username
        self.__password = password
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
    def from_dict(entry_dict: dict[str: str]) -> Data:
        return Data(
            entry_dict["username"],
            entry_dict["password"],
            entry_dict["service"],
            entry_dict["comment"]
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
