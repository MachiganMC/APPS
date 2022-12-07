from tkinter import *
from package.gui.Properties import *


class MenuNewProfile:
    def __init__(self):
        super().__init__()

        self.__frame = Frame(bg=BACKGROUND_COLOR)
        button: Button = Button(self.__frame)
        button.pack()

    @property
    def frame(self) -> Frame:
        return self.__frame
