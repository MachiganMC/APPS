import hashlib
import os

from package.functional.data import Data
from package.functional.profil import hash_str
from package.functional.question import Question
from package.gui.basic_window import BasicWindow
from package.functional.profil import Profil

bw: BasicWindow = BasicWindow()
if __name__ == '__main__':
    try:
        os.makedirs("data")
    except FileExistsError:
        pass

    bw.mainloop()
    p2 = Profil.get_from_question("simon", "bleu")
    # for i in range(6):
    #     p2.entries.append(Account("Simon", f"mon mdp {i + 40}", f"Service {i + 41}"))
    # p2.entries.append(Entry("Simon", "mon_mdp", "Minecraft", "Un jeu de cube"))
    # p2.save(hash_str("test"), hash_str("bleu"))
    # print(p2.login)
