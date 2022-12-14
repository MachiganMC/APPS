from tkinter import *

from package.MDP.Profil import Profil
from package.gui.Properties import *


class MainMenu:

    def __init__(self, profil: Profil) -> None:
        self.__frame: Frame = Frame(bg=BACKGROUND_COLOR)

        label: Label = Label(self.__frame, text="Menu des mdp", **TEXT_PROPERTIES)
        label.pack()

    @property
    def frame(self) -> Frame:
        return self.__frame
