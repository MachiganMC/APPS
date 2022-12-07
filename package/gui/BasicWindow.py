from tkinter import *
from package.gui.Properties import *


class BasicWindow(Tk):
    def __init__(self):
        from package.gui.MenuLogin import MenuLogin
        super().__init__()

        self.title("Alzheimer Password Program Solution")
        self.resizable(True, True)
        self.iconbitmap("package/img/icon-a.ico")
        self.minsize(width=MIN_WIDTH, height=MIN_HEIGHT)
        self.maxsize(width=MAX_WIDTH, height=MAX_HEIGHT)
        entry = Entry()
        self.config(bg=BACKGROUND_COLOR)

        self.__frame = MenuLogin().frame
        self.__frame.pack()

    @property
    def frame(self) -> Frame:
        return self.__frame

    @frame.setter
    def frame(self, frame: Frame):
        self.__frame = frame
