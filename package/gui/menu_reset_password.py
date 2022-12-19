import hashlib
from tkinter import *

from package.gui.properties import *
from package.functional.profil import Profil

text_properties: dict = TEXT_PROPERTIES | {"font": ("Impact", 15)}


class MenuResetPassword:
    def __init__(self, name_profile: str) -> None:
        self.__answer_conf = None
        self.__label_pw_conf = None
        self.__label_pw = None
        self.__name_profile: str = name_profile
        self.__frame: Frame = Frame(bg=BACKGROUND_COLOR)

        back_button: Button = Button(self.__frame, text="Retour au menu connexion", **text_properties,
                                     command=lambda: MenuResetPassword.return_menu_login())
        back_button.pack(side="top", anchor=W, pady=10)

        label: Label = Label(self.__frame, text=f"Réinitialiser le mot de passe de {name_profile} :", **TEXT_PROPERTIES)
        label.pack(expand=1)
        self.__label_info: Label = Label(self.__frame,
                                         text="Répondez à cette question pour réinitialiser le mot de passe :",
                                         **text_properties)
        self.__label_info.pack()

        question: str
        try:
            question = Profil.get_question_from_str(name_profile)
        except ValueError:
            from __main__ import bw
            from package.gui.menu_login import MenuLogin
            bw.frame.destroy()
            bw.frame = MenuLogin().frame
            bw.frame.pack()
            return

        self.__formulaire: Frame = Frame(self.__frame, bg=BACKGROUND_COLOR, highlightcolor="white",
                                         highlightthickness=2)
        self.__formulaire.pack()
        label_question: Label = Label(self.__formulaire, text=question, **text_properties)
        label_question.grid(row=0, column=0, padx=10, pady=10)
        self.__answer: StringVar = StringVar()
        entry_answer: Entry = Entry(self.__formulaire, **text_properties, textvariable=self.__answer, show='*')
        entry_answer.grid(row=0, column=1, pady=10)

        self.__button_validate: Button = Button(self.__formulaire, text="Valider",
                                                **text_properties | {"font": ("Impact", 10)},
                                                command=lambda: self.try_question())
        self.__button_validate.grid(row=0, column=2, padx=10)

        self.__response: Label = Label(self.__frame, **text_properties | {"fg": "red"})
        self.__response.pack()

    def try_question(self):
        answer: str = self.__answer.get()
        if answer == "":
            self.__response["text"] = "Veuillez répondre à la question"
            return

        profil: Profil
        try:
            profil = Profil.get_from_question(self.__name_profile, answer)
        except ValueError:
            self.__response["text"] = "Réponse incorrect"
            return

        self.__response["text"] = ""
        self.__label_info["text"] = "Choisissez votre nouveau mot de passe"
        self.__formulaire.destroy()
        self.__formulaire: Frame = Frame(self.__frame, bg=BACKGROUND_COLOR, highlightcolor="white",
                                         highlightthickness=2)
        self.__formulaire.pack()

        self.__label_pw = Label(self.__formulaire, text="Mot de passe :", **text_properties)
        self.__label_pw.grid(row=0, column=0, padx=10)
        self.__answer: StringVar = StringVar()
        entry_answer: Entry = Entry(self.__formulaire, **text_properties, textvariable=self.__answer, show='*')
        entry_answer.grid(row=0, column=1, pady=10)

        self.__label_pw_conf = Label(self.__formulaire, text="Confirmation :", **text_properties)
        self.__label_pw_conf.grid(row=1, column=0, padx=10, pady=10)
        self.__answer_conf: StringVar = StringVar()
        entry_answer_conf: Entry = Entry(self.__formulaire, **text_properties, textvariable=self.__answer_conf,
                                         show='*')
        entry_answer_conf.grid(row=1, column=1, pady=10, padx=10)

        self.__button_validate: Button = Button(self.__frame, text="Valider",
                                                **text_properties | {"font": ("Impact", 20)},
                                                command=lambda: self.reset_password(profil, answer))
        self.__button_validate.pack(pady=10)

    def reset_password(self, profil: Profil, answer: str):
        from __main__ import bw
        from package.gui.menu_login import MenuLogin
        if self.__answer.get() == "" or self.__answer_conf.get() == "":
            self.__response["text"] = "Tous les champs n'ont pas été remplis"
            return

        if not self.__answer.get() == self.__answer_conf.get():
            self.__response["text"] = "Ces mots de passe ne correspondent pas"
            return

        password_hash: str = hashlib.md5(self.__answer.get().encode()).hexdigest()
        answer_hash: str = hashlib.md5(answer.encode()).hexdigest()
        profil.save(password_hash, answer_hash)
        bw.frame.destroy()
        bw.frame = MenuLogin().frame
        bw.frame.pack(expand=1)

    @property
    def frame(self) -> Frame:
        return self.__frame

    @classmethod
    def return_menu_login(cls):
        from __main__ import bw
        from package.gui.menu_login import MenuLogin
        bw.frame.destroy()
        bw.frame = MenuLogin().frame
        bw.frame.pack()
