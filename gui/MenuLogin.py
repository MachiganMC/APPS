from tkinter import *
from gui.Properties import BACKGROUND_COLOR, FONT_COLOR
from PIL import Image, ImageTk


class MenuLogin:
    def __init__(self):
        super().__init__()

        self.__frame: Frame = Frame(bg=BACKGROUND_COLOR)
        self.__frame.pack(expand=1)

        icon: ImageTk = Image.open("img/icon.png")
        icon_tk = ImageTk.PhotoImage(icon)
        icon_frame: Label = Label(self.__frame, image=icon_tk, bg=BACKGROUND_COLOR, fg=FONT_COLOR)
        icon_frame.image = icon_tk
        icon_frame.pack(expand=1)

        label: Label = Label(self.__frame, text="Qui est-ce ?", font=("Arial", 35, "bold"), fg="#C4C4C4",
                             bg=BACKGROUND_COLOR)
        label.pack(pady=50)

        pp_frame: Frame = Frame(self.__frame, bg=BACKGROUND_COLOR)
        pp_frame.pack()

        image: ImageTk = Image.open("img/id-card-512-3617266879.png")
        image = image.resize((100, 100))
        image_tk: ImageTk = ImageTk.PhotoImage(image)

        for i in range(5):
            pp_frame.columnconfigure(index=i, minsize=150)
            profil: Button = Button(pp_frame, text="A", font=("Impact", 40, "bold"), bg=BACKGROUND_COLOR,
                                    fg=BACKGROUND_COLOR, command=lambda j=i: MenuLogin.on_click(j), image=image_tk)
            profil.image = image_tk
            profil.grid(column=i, row=0)
            name: Label = Label(pp_frame, text=f"Profil {i}", fg=FONT_COLOR, bg=BACKGROUND_COLOR, font=("Impact", 15))
            name.grid(column=i, row=1)

        new_profil: Button = Button(pp_frame, text="+", font=("Impact", 40, "bold"), bg="#C4C4C4", fg=BACKGROUND_COLOR,
                                    command=lambda: MenuLogin.new_profile())
        new_profil.grid(column=6, row=0)

    @staticmethod
    def on_click(name_profile: int):
        pass

    @staticmethod
    def new_profile():
        import __main__
        from gui.MenuNewProfile import MenuNewProfile
        __main__.bw.frame.destroy()
        __main__.bw.frame = MenuNewProfile().frame
        __main__.bw.frame.pack()

    @property
    def frame(self) -> Frame:
        return self.__frame
