from tkinter import *

from PIL import Image
from PIL import ImageTk

from package.functional.profil import Profil
from package.functional.data import Data
from package.gui.properties import *

ELEMENT_PER_PAGE: int = 10
text_properties: dict = TEXT_PROPERTIES | {"font": ("Impact", 25)}
highlight_properties: dict = {"highlightcolor": "white", "highlightthickness": 2}


class MainMenu:

    def __init__(self, profil: Profil) -> None:
        self.__has_to_logout = True
        self.__page = None
        self.__profil = profil
        self.__frame: Frame = Frame(bg=BACKGROUND_COLOR)

        frame_info: Frame = Frame(self.__frame, bg=BACKGROUND_COLOR, **highlight_properties)
        frame_info.pack(side='top', fill='x')
        self.__button_logout: Button = Button(frame_info, text="Déconnexion",
                                              **TEXT_PROPERTIES | {"font": ("Impact", 20)},
                                              command=lambda: self.logout())
        self.__button_logout.pack(side='left', ipadx=50)
        Label(frame_info, text=profil.name, **text_properties | highlight_properties) \
            .pack(side='right', fill='y', ipadx=50)
        Label(frame_info, text="A.P.P.S", **text_properties | highlight_properties) \
            .pack(fill='y', expand=True, ipadx=100)

        self.__frame_entries_parent: Frame = Frame(self.__frame, bg=BACKGROUND_COLOR)
        self.__frame_entries_parent.pack()
        self.show_entries(0)

        Frame(self.__frame, **highlight_properties).pack(fill='x', pady=(15, 0))

        text_formulaire_properties: dict = TEXT_PROPERTIES | {"font": ("Impact", 17)}
        Label(self.__frame, text="Ajouter une entrée :", **TEXT_PROPERTIES).pack(pady=(30, 0))
        frame_formulaire: Frame = Frame(self.__frame, bg=BACKGROUND_COLOR, **highlight_properties)
        frame_formulaire.pack(pady=10)
        Label(frame_formulaire, text="Nom d'utilisateur :", **text_formulaire_properties) \
            .grid(row=0, column=0, pady=5, padx=(10, 0))
        self.__formulaire_user: StringVar = StringVar()
        self.__entry_user: Entry = Entry(frame_formulaire, textvariable=self.__formulaire_user,
                                         **text_formulaire_properties)
        self.__entry_user.grid(row=0, column=1, padx=(0, 10))
        Label(frame_formulaire, text="Mot de passe :", **text_formulaire_properties) \
            .grid(row=1, column=0, pady=5, padx=(10, 0))
        self.__formulaire_pw: StringVar = StringVar()
        self.__entry_pw: Entry = Entry(frame_formulaire, textvariable=self.__formulaire_pw,
                                       **text_formulaire_properties)
        self.__entry_pw.grid(row=1, column=1, padx=(0, 10))
        Label(frame_formulaire, text="Service :", **text_formulaire_properties) \
            .grid(row=2, column=0, pady=5, padx=(10, 0))
        self.__formulaire_service: StringVar = StringVar()
        self.__entry_service: Entry = Entry(frame_formulaire, textvariable=self.__formulaire_service,
                                            **text_formulaire_properties)
        self.__entry_service.grid(row=2, column=1, padx=(0, 10))
        Label(frame_formulaire, text="Commentaire :", **text_formulaire_properties) \
            .grid(row=3, column=0, pady=5, padx=(10, 0))
        self.__formulaire_comment: StringVar = StringVar()
        self.__entry_comment: Entry = Entry(frame_formulaire, textvariable=self.__formulaire_comment,
                                            **text_formulaire_properties)
        self.__entry_comment.grid(row=3, column=1, padx=(0, 10))

        Button(self.__frame, text="Ajouter", **text_formulaire_properties, command=lambda: self.add_data()) \
            .pack(ipadx=15)
        self.__result_add: Label = Label(self.__frame, **TEXT_PROPERTIES | {"font": ("Impact", 20)})
        self.__result_add.pack()

    def show_entries(self, page: int) -> None:
        """
        Auteur : Simon Maes
        Dernière modification : 19 décembre 2022
        Permet d'update le contenu de self.__frame_entries_parent avec les nouvelles valeurs de la liste des
        data de self.__profil.
        PRE :
            - page doit être positif et plus petit ou égal à self.max_page() - 1

        POST :
            - réécrit tous les éléments de self.__frame_entries_parent
            - lance une ValueError si les préconditions ne sont pas respectées.
        """
        if page < 0:
            raise ValueError("Pas invalide (négative)")
        if page > self.max_page() + 1:
            raise ValueError(f"Pas invalide (trop grande max {self.max_page() - 1}")

        self.__page = page
        for widget in self.__frame_entries_parent.winfo_children():
            widget.destroy()

        if len(self.__profil.entries) == 0:
            Label(self.__frame_entries_parent, text="Aucune entrée enregistrée", **TEXT_PROPERTIES).pack(pady=5)
            return

        label_page: Label = Label(self.__frame_entries_parent, **text_properties)
        label_page.pack(pady=5)
        frame_entries_button: Frame = Frame(self.__frame_entries_parent, bg=BACKGROUND_COLOR)
        frame_entries_button.pack(expand=True)
        button_precedent: Button = Button(frame_entries_button, text="◀", **TEXT_PROPERTIES | {"font": ("Impact", 20)})
        if page == 0:
            button_precedent.config(state='disabled')
        else:
            button_precedent.config(command=lambda: self.show_entries(self.__page - 1))
        button_precedent.grid(row=0, column=0, padx=10, pady=(5, 0))
        button_next: Button = Button(frame_entries_button, text="▶", **TEXT_PROPERTIES | {"font": ("Impact", 20)})
        if page == self.max_page() - 1:
            button_next.config(state='disabled')
        else:
            button_next.config(command=lambda: self.show_entries(self.__page + 1))
        button_next.grid(row=0, column=1, padx=10, pady=(5, 0))

        highlight_entries_properties: dict = {"highlightcolor": "#8A8A8A", "highlightthickness": 1}
        text_entries_properties: dict = TEXT_PROPERTIES | {"font": ("Impact", 15)}

        frame_entries: Frame = Frame(self.__frame_entries_parent, bg=BACKGROUND_COLOR, **highlight_properties)
        frame_entries.pack(expand=True, pady=(30, 0), padx=10)
        Label(frame_entries, text="Nom d'utilisateur",
              **text_properties | highlight_properties).grid(row=0, column=1, ipadx=50)
        Label(frame_entries, text="Mot de passe", **text_properties | highlight_properties) \
            .grid(row=0, column=2, ipadx=50)
        Label(frame_entries, text="Service", **text_properties | highlight_properties) \
            .grid(row=0, column=3, ipadx=50)
        Label(frame_entries, text="Commentaire", **text_properties | highlight_properties) \
            .grid(row=0, column=4, ipadx=150)

        image_trash: ImageTk = Image.open("img/trash.png")
        image_trash = image_trash.resize((25, 25))
        image_trash_tk: ImageTk = ImageTk.PhotoImage(image_trash)
        for i in range(ELEMENT_PER_PAGE * page, ELEMENT_PER_PAGE * (page + 1)):
            entry: Data
            try:
                entry = self.__profil.entries[i]
            except IndexError:
                break

            index: int = self.__profil.entries.index(entry) + 1
            Label(frame_entries, text=f"{i + 1}", **text_entries_properties, **highlight_entries_properties) \
                .grid(row=index, column=0, sticky='NSWE')
            Label(frame_entries, text=entry.username, **text_entries_properties, **highlight_entries_properties) \
                .grid(row=index, column=1, sticky='NSWE')
            Label(frame_entries, text=entry.password, **text_entries_properties, **highlight_entries_properties) \
                .grid(row=index, column=2, sticky='NSWE')
            Label(frame_entries, text=entry.service, **text_entries_properties, **highlight_entries_properties) \
                .grid(row=index, column=3, sticky='NSWE')
            if entry.comment == "":
                Label(frame_entries, text="/", **TEXT_PROPERTIES | {"font": ("Impact", 15, "italic"),
                                                                    "fg": "#8A8A8A"}) \
                    .grid(row=index, column=4, sticky='NSWE')
            else:
                Label(frame_entries, text=entry.comment, **text_entries_properties, **highlight_entries_properties) \
                    .grid(row=index, column=4, sticky='NSWE')

            button_delete: Button = Button(frame_entries, image=image_trash_tk, bg=BACKGROUND_COLOR)
            button_delete.config(
                command=lambda row=index, a=entry, b=button_delete: self.click_delete(row, a, frame_entries, b))
            button_delete.image = image_trash_tk
            button_delete.grid(row=index, column=5, sticky='NSWE')

        label_page.config(text=f"Page {self.__page + 1}")

    def max_page(self):
        size: int = len(self.__profil.entries)
        if size == 0:
            return 1
        if size % ELEMENT_PER_PAGE == 0:
            return int(size / ELEMENT_PER_PAGE)
        return int(size / ELEMENT_PER_PAGE) + 1

    def logout(self):
        from __main__ import bw
        from package.gui.menu_logout import MenuLogout
        if self.__has_to_logout:
            from package.gui.menu_login import MenuLogin
            bw.frame.destroy()
            bw.frame = MenuLogin().frame
            bw.frame.pack()
        else:
            from package.gui.menu_login import MenuLogin
            bw.frame.destroy()
            bw.frame = MenuLogout(self.__profil).frame
            bw.frame.pack()

    def click_delete(self, row: int, data: Data, frame_entries: Frame, old_button: Button) -> None:
        """
        Auteur : Antoine Moens Pennewaert
        Dernière modification : 20 décembre 2022

        → Supprimer une entrée en cliquant sur un bouton en forme de poubelle,
            - row -> la ligne de l'entrée.
            - data -> l'objet qui va être supprimée
            - old_button -> le bouton qui va être remplacé par une autre image de bouton.
            - frame_entries : la frame qui contient le tableau widget de toutes les data.
        PRE :
            - row doit être positif ou égal à 0
            - data ne doit pas être None
            - frame_entries ne doit pas être None
            - old_button ne doit pas être None
        POST :
            - lance une FileNotFoundError si l'image "img/trash_confirm.png" n'est pas trouvée
            - l'entrée est supprimée.
        """

        if row < 0:
            raise ValueError("Row doit être positif")
        if data is None:
            raise ValueError("Account ne doit pas être égal à None")
        if frame_entries is None:
            raise ValueError("frame_entries ne doit pas être égal à None")
        if old_button is None:
            raise ValueError("old_button ne doit pas être égal à None")

        image_trash_confirm: ImageTk = Image.open("img/trash_confirm.png")
        image_trash_confirm = image_trash_confirm.resize((25, 25))
        image_trash_confirm_tk: ImageTk = ImageTk.PhotoImage(image_trash_confirm)
        button: Button = Button(frame_entries, bg=BACKGROUND_COLOR, image=image_trash_confirm_tk,
                                command=lambda: self.delete(data))
        old_button.image = image_trash_confirm_tk
        button.grid(row=row, column=5)

    def delete(self, account: Data):
        self.__profil.entries.remove(account)
        self.__has_to_logout = False
        self.__button_logout.config(text="Sauvegarder")
        self.show_entries(self.__page)

    def add_data(self) -> None:
        if self.__formulaire_user.get() == "" or self.__formulaire_pw.get() == "" or \
                self.__formulaire_service.get() == "":
            self.__result_add.config(text="Veuillez remplir toutes les entrées", fg="red")
            return

        self.__profil.entries.append(Data(self.__formulaire_user.get(), self.__formulaire_pw.get(),
                                          self.__formulaire_service.get(), self.__formulaire_comment.get()))
        self.__result_add.config(text=f"L'entrée N° {len(self.__profil.entries)} a éjé ajoutée", fg="green")

        self.__formulaire_user = StringVar()
        self.__entry_user.config(textvariable=self.__formulaire_user)
        self.__formulaire_pw = StringVar()
        self.__entry_pw.config(textvariable=self.__formulaire_pw)
        self.__formulaire_service = StringVar()
        self.__entry_service.config(textvariable=self.__formulaire_service)
        self.__formulaire_comment = StringVar()
        self.__entry_comment.config(textvariable=self.__formulaire_comment)
        self.__has_to_logout = False
        self.__button_logout.config(text="Sauvegarder")
        self.show_entries(self.__page)

    @property
    def frame(self) -> Frame:
        return self.__frame
