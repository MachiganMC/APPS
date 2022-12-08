from tkinter import *
from package.gui.Properties import *


class MenuNewProfile:
    def __init__(self):
        super().__init__()
        text_properties: dict[str] = {"bg": BACKGROUND_COLOR, "fg": FONT_COLOR, "font": ("Impact", 15)}

        self.__frame = Frame(bg=BACKGROUND_COLOR)

        self.__welcome_label: Label = Label(self.__frame, text="Créer un nouveau profil", **TEXT_PROPERTIES)
        self.__welcome_label.pack(expand=1)

        self.__formulaire: Frame = Frame(self.__frame, bg=BACKGROUND_COLOR, highlightbackground="white",
                                         highlightthickness=3, pady=20, padx=20)
        self.__formulaire.pack(expand=1)
        self.__formulaire.rowconfigure(index=0, pad=20)

        self.__name_label: Label = Label(self.__formulaire, text="Nom de profil :", **text_properties)
        self.__name_label.grid(row=0, column=0)
        self.__name_entry: Entry = Entry(self.__formulaire, **text_properties)
        self.__name_entry.grid(row=0, column=1)

        self.__pw_label: Label = Label(self.__formulaire, text="Mot de passe :", **text_properties)
        self.__pw_label.grid(row=1, column=0)
        self.__pw_entry: Entry = Entry(self.__formulaire, show='*', **text_properties)
        self.__pw_entry.grid(row=1, column=1)
        self.__pw_label_checkbox: Label = Label(self.__formulaire, text="Afficher", **text_properties)
        self.__pw_label_checkbox.grid(row=1, column=2)
        self.__is_show_pw: IntVar = IntVar()
        self.__pw_checkbox: Checkbutton = Checkbutton(self.__formulaire, **text_properties,
                                                      command=lambda: self.on_check_button(),
                                                      variable=self.__is_show_pw)
        self.__pw_checkbox.grid(row=1, column=3)

    def on_check_button(self):
        if self.__is_show_pw.get():
            self.__pw_label_checkbox.config(text="Cacher")
            self.__pw_entry.config(show='')
        else:
            self.__pw_label_checkbox.config(text="Monter")
            self.__pw_entry.config(show='*')

    @property
    def frame(self) -> Frame:
        return self.__frame
