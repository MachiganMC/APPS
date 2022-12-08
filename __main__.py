import hashlib
import os

from package.MDP.Question import Question
from package.gui.BasicWindow import BasicWindow
from package.MDP.Profil import Profil

bw: BasicWindow = BasicWindow()
if __name__ == '__main__':
    try:
        os.makedirs("data")
    except FileExistsError:
        pass

    bw.mainloop()
    # p: Profil = Profil.new_profil("simon", "tets", Question(0, "moiu"))
    # p.save()
    # p2 = Profil.get_from_question("simon", "moiu")
    # print(p2.login)
