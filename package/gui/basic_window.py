from tkinter import *
from package.gui.properties import *


class BasicWindow(Tk):
    def __init__(self):
        from package.gui.menu_login import MenuLogin
        super().__init__()

        self.title("Alzheimer Password Program Solution")
        self.iconbitmap("img/icon-a.ico")
        self.resizable(False, False)
        self.state("zoomed")
        self.minsize(width=MIN_WIDTH, height=MIN_HEIGHT)
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

