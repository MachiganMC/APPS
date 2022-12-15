from tkinter import *
from package.gui.properties import BACKGROUND_COLOR, FONT_COLOR, TEXT_PROPERTIES
from PIL import Image, ImageTk


class MenuLogin:
    def __init__(self):

        self.__frame: Frame = Frame(bg=BACKGROUND_COLOR)
        self.__frame.pack(expand=1)
        self.__connect: Frame = Frame(self.__frame, bg=BACKGROUND_COLOR)
        self.__connect.pack(side="bottom")

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

        from package.MDP.profil import Profil
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

        if len(Profil.all_profil_str()) <= 5:
            image_plus: ImageTk = Image.open("package/img/+.png")
            image_plus = image_plus.resize((100, 100))
            image_plus_tk: ImageTk = ImageTk.PhotoImage(image_plus)
            new_profil: Button = Button(pp_frame, image=image_plus_tk,
                                        bg=BACKGROUND_COLOR, border=0,
                                        command=lambda: MenuLogin.new_profile())
            new_profil.image = image_plus_tk
            new_profil.grid(column=6, row=0)

        self.__label_hello = Label(self.__frame, **TEXT_PROPERTIES)
        self.__label_hello.pack()
        self.__formulaire = Frame(self.__frame, bg=BACKGROUND_COLOR)
        self.__error_login: Label = Label()
        self.__button_forgot_pw: Button = Button()

    def on_click(self, name_profile: str):
        text_properties: dict = TEXT_PROPERTIES | {"font": ("Impact", 20)}
        self.__label_hello["text"] = f"Bonjour {name_profile}"
        self.__formulaire.destroy()
        self.__formulaire = Frame(self.__frame, bg=BACKGROUND_COLOR)
        self.__formulaire.pack()

        label_password: Label = Label(self.__formulaire, text="Mot de passe :", **text_properties)
        label_password.grid(row=0, column=0, pady=10, padx=(10, 0))
        value_entry_pw: StringVar = StringVar()
        entry_password: Entry = Entry(self.__formulaire, textvariable=value_entry_pw, **text_properties, show='*')
        entry_password.grid(row=0, column=1, padx=10)
        button_check: Button = Button(self.__formulaire, text="Se connecter",
                                      **TEXT_PROPERTIES | {"font": ("Impact", 14)},
                                      command=lambda: self.try_login(name_profile, value_entry_pw.get()))
        button_check.grid(row=0, column=2, padx=(0, 10))

        self.__button_forgot_pw.destroy()
        self.__button_forgot_pw: Button = Button(self.__frame, text="J'ai oublié mon mot de passe",
                                                 **TEXT_PROPERTIES | {"font": ("Impact", 20)},
                                                 command=lambda: MenuLogin.change_password(name_profile))
        self.__button_forgot_pw.pack(pady=10)
        self.__error_login.destroy()
        self.__error_login = Label(self.__frame, ** TEXT_PROPERTIES | {"fg": "red"})
        self.__error_login.pack()

    @staticmethod
    def new_profile():
        import __main__
        from package.gui.menu_new_profile import MenuNewProfile
        __main__.bw.frame.destroy()
        __main__.bw.frame = MenuNewProfile().frame
        __main__.bw.frame.pack()

    @property
    def frame(self) -> Frame:
        return self.__frame

    def try_login(self, profile_name: str, pw: str) -> None:
        from package.gui.main_menu import MainMenu
        from package.MDP.profil import Profil
        from __main__ import bw
        if pw == "":
            self.__error_login["text"] = "Veuillez entrer votre mot de passe"
            return
        try:
            profil: Profil = Profil().get_from_password(profile_name, pw)
            bw.frame.destroy()
            bw.frame = MainMenu(profil).frame
            bw.frame.pack()
        except ValueError:
            self.__error_login["text"] = "Mot de pas incorrect"

    @staticmethod
    def change_password(name_profile: str):
        from __main__ import bw
        from package.gui.menu_reset_password import MenuResetPassword
        bw.frame.destroy()
        bw.frame = MenuResetPassword(name_profile).frame
        bw.frame.pack()
