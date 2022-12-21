from tkinter import *
from package.gui.properties import *
import logging


class BasicWindow(Tk):
    def __init__(self):
        """
        Auteur : Corentin Koninckx
        Dernière modification : 19 décembre 2022

        Permet de créer une nouvelle fenêtre avec certaines propriétés :
            - titre = Alzheimer Password Program Solution,
            - icône = à l'image se trouvant dans "img/icon-a.ico",
            - taille non ajustable,
            - taille fenêtre maximum = valeur de properties.py

        POST :
            - lance une FileNotFoundError si l'icône n'est pas trouvée
            - un nouvel objet BasicWindow est instancié
        """
        from package.gui.menu_login import MenuLogin
        super().__init__()

        self.title("Alzheimer Password Program Solution")
        self.iconbitmap("img/icon-a.ico")
        self.resizable(False, False)
        self.state("zoomed")
        self.minsize(width=MAX_WIDTH, height=MAX_HEIGHT)
        self.maxsize(width=MAX_WIDTH, height=MAX_HEIGHT)
        self.config(bg=BACKGROUND_COLOR)

        self.__frame = MenuLogin().frame
        self.__frame.pack()

    @property
    def frame(self) -> Frame:
        return self.__frame

    @frame.setter
    def frame(self, frame: Frame):
        self.__frame = frame
