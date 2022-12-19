import hashlib
from tkinter import *
from tkinter import ttk

from package.functional.profil import Profil
from package.functional.question import Question
from package.gui.properties import *


class MenuNewProfile:
    def __init__(self):
        text_properties: dict[str] = {"bg": BACKGROUND_COLOR, "fg": FONT_COLOR, "font": ("Impact", 15)}

        self.__frame = Frame(bg=BACKGROUND_COLOR)

        self.__back_button: Button = Button(self.__frame, text="Retour menu connexion", **text_properties,
                                            command=lambda: MenuNewProfile.back())
        self.__back_button.pack(side=TOP, anchor=NW)

        self.__welcome_label: Label = Label(self.__frame, text="Créer un nouveau profil", **TEXT_PROPERTIES)
        self.__welcome_label.pack(expand=1)

        self.__formulaire: Frame = Frame(self.__frame, bg=BACKGROUND_COLOR, highlightbackground="white",
                                         highlightthickness=3, pady=20, padx=20)
        self.__formulaire.pack(expand=1)
        self.__formulaire.rowconfigure(index="all", pad=20)

        self.__name_label: Label = Label(self.__formulaire, text="Nom de profil :", **text_properties)
        self.__name_label.grid(row=0, column=0)
        self.__name_entry: Entry = Entry(self.__formulaire, **text_properties)
        self.__name_entry.grid(row=0, column=1)

        self.__pw_label: Label = Label(self.__formulaire, text="Mot de passe :", **text_properties)
        self.__pw_label.grid(row=1, column=0)
        self.__pw_entry: Entry = Entry(self.__formulaire, show='*', **text_properties)
        self.__pw_entry.grid(row=1, column=1)

        self.__show_pw: Button = Button(self.__formulaire, text="Afficher", command=lambda: self.show_password(),
                                        **text_properties | {"font": ("Impact", 10)})
        self.__show_pw.grid(row=1, column=2, padx=10)

        self.__pw_label2: Label = Label(self.__formulaire, text="Confirmation :", **text_properties)
        self.__pw_label2.grid(row=2, column=0)
        self.__pw_entry2: Entry = Entry(self.__formulaire, show='*', **text_properties)
        self.__pw_entry2.grid(row=2, column=1)

        self.__label_question: Label = Label(self.__formulaire, text="Question de récupération :",
                                             **text_properties)
        self.__label_question.grid(row=3, column=0)
        self.__question_value: StringVar = StringVar()

        self.__chosen = StringVar()
        self.__question = ttk.Combobox(self.__formulaire, textvariable=self.__chosen, state="readonly",
                                       values=Question.all_questions, width=50)
        self.__question.grid(row=3, column=1, padx=10)

        self.__label_answer: Label = Label(self.__formulaire, text="La réponse :", **text_properties)
        self.__label_answer.grid(row=4, column=0)
        self.__entry_answer: Entry = Entry(self.__formulaire, **text_properties)
        self.__entry_answer.grid(row=4, column=1)

        self.__label_answer2: Label = Label(self.__formulaire, text="Confirmation :", **text_properties)
        self.__label_answer2.grid(row=5, column=0)
        self.__entry_answer2: Entry = Entry(self.__formulaire, **text_properties)
        self.__entry_answer2.grid(row=5, column=1)

        self.__check_button: Button = Button(self.__frame, text="Valider", command=lambda: self.validate(),
                                             **text_properties | {"font": ("Impact", 30)})
        self.__check_button.pack(pady=30)

        self.__result: Label = Label(self.__frame, **text_properties | {"font": ("Impact", 30), "fg": "red"})
        self.__result.pack()

    def show_password(self):
        if self.__show_pw["text"] == "Afficher":
            self.__show_pw.config(text="Cacher")
            self.__pw_entry.config(show='')
            self.__pw_entry2.config(show='')
        elif self.__show_pw["text"] == "Cacher":
            self.__show_pw.config(text="Afficher")
            self.__pw_entry.config(show='*')
            self.__pw_entry2.config(show='*')

    def validate(self):
        if self.__name_entry.get() == "" or self.__pw_entry == "" or self.__pw_entry2 == "" \
                or self.__entry_answer == "" or self.__entry_answer2 == "":
            self.__result["text"] = "Veuillez compléter tous les champs"
            return
        try:
            question_index: int = Question.all_questions.index(self.__chosen.get())
        except ValueError:
            self.__result["text"] = "Veuillez sélectionner une question de récupération"
            return

        if self.__name_entry.get() == Profil.all_profil_str():
            self.__result["text"] = "Ce nom de profil existe déjà"
            return

        if not self.__pw_entry.get() == self.__pw_entry2.get():
            self.__result["text"] = "Mots de passe non identiques"
            return

        if not self.__entry_answer.get() == self.__entry_answer2.get():
            self.__result["text"] = "Réponses non identiques"
            return

        name: str = self.__name_entry.get()
        if "." in name or " " in name:
            self.__result["text"] = "Le nom ne peut pas contenir de point ou d'espace"
            return

        Profil.new_profil(name, self.__pw_entry.get(), Question(question_index, self.__entry_answer.get())).save(
            hashlib.md5(self.__pw_entry.get().encode()).hexdigest(),
            hashlib.md5(self.__entry_answer.get().encode()).hexdigest()
        )
        self.__result["fg"] = "green"
        self.__result["text"] = "Profil créé avec succès"

        empty_str: StringVar = StringVar()
        self.__name_entry["textvariable"] = empty_str
        self.__pw_entry["textvariable"] = empty_str
        self.__pw_entry2["textvariable"] = empty_str
        self.__entry_answer["textvariable"] = empty_str
        self.__entry_answer2["textvariable"] = empty_str
        empty_str.set("")

    @classmethod
    def back(cls):
        from __main__ import bw
        from package.gui.menu_login import MenuLogin
        bw.frame.destroy()
        bw.frame = MenuLogin().frame
        bw.frame.pack()

    @property
    def frame(self) -> Frame:
        return self.__frame
