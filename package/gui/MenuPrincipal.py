from tkinter import *
from package.gui.Properties import *

class MenuPrincipal:
    def __init__(self):
        text_propreties_Bold: dict[str] = {"bg": BACKGROUND_COLOR, "fg": FONT_COLOR, "font": ("Impact", 20, "bold")}
        text_propreties_normal: dict[str] = {"bg": BACKGROUND_COLOR, "fg": FONT_COLOR, "font": ("Impact", 15)}

        self.__frame = Frame(bg = BACKGROUND_COLOR)




