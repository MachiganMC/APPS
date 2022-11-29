from tkinter import *
import gui.Properties as Properties


class BasicWindow(Tk):
    def __init__(self):
        from gui.MenuLogin import MenuLogin
        super().__init__()

        self.title("Alzheimer Password Program Solution")
        self.resizable(True, True)
        self.iconbitmap("img/icon-a.ico")
        self.minsize(width=Properties.MIN_WIDTH, height=Properties.MIN_HEIGHT)
        self.maxsize(width=Properties.MAX_WIDTH, height=Properties.MAX_HEIGHT)
        entry = Entry()
        self.config(bg=Properties.BACKGROUND_COLOR)
        # self.state("zoom")

        self.__frame = MenuLogin().frame
        self.__frame.pack()

    @property
    def frame(self) -> Frame:
        return self.__frame

    @frame.setter
    def frame(self, frame: Frame):
        self.__frame = frame
