from tkinter import *

from package.MDP.profil import Profil
from package.gui.properties import *


class MainMenu:

    def __init__(self, profil: Profil) -> None:
        self.__frame: Frame = Frame(bg=BACKGROUND_COLOR)

        label: Label = Label(self.__frame, text="Menu des mdp", **TEXT_PROPERTIES)
        label.pack()

        frame_info: Frame = Frame(self.__frame, bg=BACKGROUND_COLOR)
        frame_info.pack(side='top')


    @property
    def frame(self) -> Frame:
        return self.__frame
