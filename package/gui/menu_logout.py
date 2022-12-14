import logging
from tkinter import *

from package.functional.profil import Profil
from package.functional.question import Question
from package.gui.properties import *


class MenuLogout:
    def __init__(self, profil: Profil):
        self.__profil = profil
        self.__frame = Frame(bg=BACKGROUND_COLOR)
        text_formulaire_properties: dict = TEXT_PROPERTIES | {"font": ("Impact", 20)}
        Label(self.__frame, text="Se déconnecter :", **TEXT_PROPERTIES).pack(expand=True)
        Label(self.__frame, text="Pour pouvoir sauvegarder vos modifications, indiquez les informations suivantes :",
              **text_formulaire_properties).pack(expand=True)
        frame_formulaire: Frame = Frame(self.__frame, bg=BACKGROUND_COLOR, highlightcolor='white', highlightthickness=2)
        frame_formulaire.pack(expand=True)

        Label(frame_formulaire, text="Mot de passe :", **text_formulaire_properties) \
            .grid(row=0, column=0, pady=5, padx=5)
        self.__formulaire_pw: StringVar = StringVar()
        Entry(frame_formulaire, show='*', textvariable=self.__formulaire_pw, **text_formulaire_properties) \
            .grid(row=0, column=1, padx=5, pady=5)
        Label(frame_formulaire, text=Question.all_questions[profil.question_index], **text_formulaire_properties) \
            .grid(row=1, column=0, pady=5, padx=5)
        self.__formulaire_answer: StringVar = StringVar()
        Entry(frame_formulaire, textvariable=self.__formulaire_answer, **text_formulaire_properties) \
            .grid(row=1, column=1, pady=5, padx=5)

        Button(self.__frame, text="Sauvegarder", **text_formulaire_properties, command=lambda: self.logout()) \
            .pack(expand=True, pady=15)

        self.__label_result: Label = Label(self.__frame, **TEXT_PROPERTIES)
        self.__label_result.pack(expand=True)

    def logout(self):
        if self.__formulaire_answer.get() == "" or self.__formulaire_pw.get() == "":
            self.__label_result.config(fg='red', text="Toutes les informations n'ont pas été remplies")
            return

        try:
            Profil.get_from_password(self.__profil.name, self.__formulaire_pw.get())
        except ValueError:
            self.__label_result.config(fg='red', text="Mot de passe incorrect")
            return

        try:
            Profil.get_from_question(self.__profil.name, self.__formulaire_answer.get())
        except ValueError:
            self.__label_result.config(fg='red', text="Réponse à la question incorrect")
            return

        from package.functional.profil import hash_str
        from __main__ import bw
        from package.gui.main_menu import MainMenu
        from package.utils.log_handler import setup_log
        self.__profil.save(hash_str(self.__formulaire_pw.get()), hash_str(self.__formulaire_answer.get()))
        bw.frame.destroy()
        bw.frame = MainMenu(self.__profil).frame
        bw.frame.pack(fill='both')
        MenuLogoutConfirm()

        setup_log()
        logger: logging.Logger = logging.getLogger("APPS")
        logger.setLevel(logging.INFO)
        logger.info(f"Le profil {self.__profil.name} a sauvegardé ses changements")

    @property
    def frame(self) -> Frame:
        return self.__frame


class MenuLogoutConfirm(Tk):
    def __init__(self):
        super().__init__()
        self.title("Alzheimer Password Program Solution Sauvegarde")
        self.iconbitmap("img/icon-a.ico")
        self.resizable(False, False)
        self.minsize(width=480, height=135)
        self.maxsize(width=480, height=135)
        self.config(bg=BACKGROUND_COLOR)

        Label(self, text="Profil sauvegardé avec succès !", **TEXT_PROPERTIES | {"font": ("Impact", 25)})\
            .pack(expand=True)
        mainloop()
