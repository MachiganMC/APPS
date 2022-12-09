from tkinter import *
from package.gui.Properties import BACKGROUND_COLOR, FONT_COLOR, TEXT_PROPERTIES
from PIL import Image, ImageTk


class MenuLogin:
    def __init__(self):
        super().__init__()

        self.__frame: Frame = Frame(bg=BACKGROUND_COLOR)
        self.__frame.pack(expand=1)
        self.__formulaire: Frame = Frame(self.__frame, bg=BACKGROUND_COLOR)
        self.__formulaire.pack(side="left")

        icon: ImageTk = Image.open("package/img/icon.png")
        icon_tk = ImageTk.PhotoImage(icon)
        icon_frame: Label = Label(self.__frame, image=icon_tk, bg=BACKGROUND_COLOR, fg=FONT_COLOR)
        icon_frame.image = icon_tk
        icon_frame.pack(expand=1)

        label: Label = Label(self.__frame, text="Qui est-ce ?", **TEXT_PROPERTIES)
        label.pack(pady=50)

        pp_frame: Frame = Frame(self.__frame, bg=BACKGROUND_COLOR)
        pp_frame.pack()

        image: ImageTk = Image.open("package/img/id-card-512-3617266879.png")
        image = image.resize((100, 100))
        image_tk: ImageTk = ImageTk.PhotoImage(image)

        from package.MDP.Profil import Profil
        all_profil: list[str] = Profil.all_profil_str()
        for profil_name in all_profil:
            index: int = all_profil.index(profil_name)
            pp_frame.columnconfigure(index=index, minsize=150)
            profil_button: Button = Button(pp_frame, text="A", font=("Impact", 40, "bold"), bg=BACKGROUND_COLOR,
                                           fg=BACKGROUND_COLOR, command=lambda j=profil_name: self.on_click(j),
                                           image=image_tk,
                                           border=0)
            profil_button.image = image_tk
            profil_button.grid(column=index, row=0)
            name: Label = Label(pp_frame, text=profil_name, fg=FONT_COLOR, bg=BACKGROUND_COLOR,
                                font=("Impact", 15))
            name.grid(column=index, row=1)

        new_profil: Button = Button(pp_frame, text="+", font=("Impact", 40, "bold"), bg="#C4C4C4", fg=BACKGROUND_COLOR,
                                    command=lambda: MenuLogin.new_profile())
        new_profil.grid(column=6, row=0)

    @staticmethod
    def on_click(name_profile: int):
        pass

    @staticmethod
    def new_profile():
        import __main__
        from package.gui.MenuNewProfile import MenuNewProfile
        __main__.bw.frame.destroy()
        __main__.bw.frame = MenuNewProfile().frame
        __main__.bw.frame.pack()

    @property
    def frame(self) -> Frame:
        return self.__frame
