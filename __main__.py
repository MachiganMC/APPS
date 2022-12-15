import hashlib
import os

from package.MDP.question import Question
from package.gui.basic_window import BasicWindow
from package.MDP.profil import Profil

bw: BasicWindow = BasicWindow()
if __name__ == '__main__':
    try:
        os.makedirs("data")
    except FileExistsError:
        pass

    bw.mainloop()
    # p2 = Profil.get_from_question("simon", "moiu")
    # print(p2.login)
